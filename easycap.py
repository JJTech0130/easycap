#!/usr/bin/env python3
# Copyright (c) 2013 Federico Ruiz Ugalde
# Copyright (c) 2014 Kevin Kwok
# Copyright (c) 2022 JJTech0130
#
# Author: Federico Ruiz-Ugalde <memeruiz at gmail dot com>
# Author: Kevin Kwok <antimatter15@gmail.com>
# Author: JJTech0130 <jjtech@jjtech.dev>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import usb1 as usb
import threading

#from protocol import *
import protocol


EASYCAP_VID = 0x1B71
EASYCAP_PID = 0x3002

EASYCAP_INTERFACE = 0

EASYCAP_VIDEO_WIDTH = 720
EASYCAP_VIDEO_HEIGHT = 480
EASYCAP_FRAME_SIZE = EASYCAP_VIDEO_WIDTH * EASYCAP_VIDEO_HEIGHT * 2  # 2 bytes per pixel


class EasyCAP:
    def __init__(self):
        # This will select the device to use immidately,
        # but we don't want to claim it until the user uses the with
        # statement (__enter__) to guarantee that the device is released
        # properly

        self.usb_context = usb.USBContext()

        self.device = None

        for device in self.usb_context.getDeviceList():
            if (
                device.getVendorID() == EASYCAP_VID
                and device.getProductID() == EASYCAP_PID
            ):
                print("Found EasyCap")
                self.device = device
                break

        if not self.device:
            raise Exception("No EasyCap found")

        self.iso = []
        self.framebuffer = bytearray(EASYCAP_FRAME_SIZE)

        self.ready = False

        # This function is called when a new frame is ready
        self.frame_handler = None

        self.frame_counter = 0

    def __enter__(self):
        self.device_handle = self.device.open()

        self.device_handle.claimInterface(EASYCAP_INTERFACE)

        protocol.begin_capture(self.device_handle)
        protocol.set_standard(self.device_handle, "NTSC")
        protocol.set_input(self.device_handle, "Composite")

        # Enable the Alternative Mode (Used for streaming?)
        self.device_handle.setInterfaceAltSetting(EASYCAP_INTERFACE, 1)

        threading.Thread(target=self.kickoff).start()

        self.ready = True
        return self

    def __exit__(self, type, value, traceback):
        self.ready = False

        # Try and release any pending transfers
        for iso in self.iso:
            try:
                iso.cancel()
            except:
                pass

        self.device_handle.releaseInterface(EASYCAP_INTERFACE)
        self.device_handle.close()
        self.usb_context.exit()

    # This function (which runs in it's own thread) will
    # kick off the 20 iso transfers, then handle all pending USB events
    # until we're told to stop
    def kickoff(self):
        for i in range(20):
            self.transfer_iso()
        while self.ready:
            self.handle_usb_events()

    def transfer_iso(self):
        iso = self.device_handle.getTransfer(iso_packets=8)
        iso.setIsochronous(
            0x81, buffer_or_len=0x6000, callback=self.iso_ready, timeout=1000
        )
        iso.submit()
        self.iso.append(iso)

    def handle_usb_events(self):
        self.usb_context.handleEvents()

    def build_images(self, buffer_list, setup_list):
        # Trim buffers down to their "actual length"
        packets = [
            buffer_list[i][: int(setup_list[i]["actual_length"])]
            for i in range(len(buffer_list))
        ]
        for packet in packets:
            if len(packet) == 0:
                continue

            # Split the packet into 3 smaller packets
            sub_len = len(packet) // 3
            sub_packets = [packet[sub_len * i : sub_len * (i + 1)] for i in range(3)]
            for sub_packet in sub_packets:
                # First byte is always 0x88
                if sub_packet[0] != 0x88:
                    # Skip empty/invalid packets
                    continue

                # This could be used to detect dropped frames
                self.frame_counter = sub_packet[1]

                # The packet counter is constructed a bit weirdly
                # The first bit is the interlace bit, and the 2nd-4th bits are ignored
                # The 5th-8th bits form the first 4 bits of the packet counter
                # Which are then OR'd with the 3rd byte of the packet
                # (Only the last bit of the sub_packet[2] is used, as it only goes to 360...)
                packet_counter = ((sub_packet[2] & 0x0F) << 8) | sub_packet[3]
                interlace = (sub_packet[2] & 0xF0) >> 7  # opposite of original

                # Add 360 to the packet number if the interlace bit is set,
                # So that it turns it into a continuous range 0-720
                # Then multiply by 960 (the amount of data in each packet)
                offset = (packet_counter + (interlace * 360)) * 960

                # Remove the first 4 bytes and the last 60 bytes (which are padding)
                frame_data = sub_packet[4:-60]
                # Copy the data into the framebuffer
                self.framebuffer[offset : offset + 960] = frame_data

                # 360 packets * 2 times (interlaced) * 960 bytes per packet = 691200 = 720 * 480 * 2

                # We've drawn a whole frame
                if interlace == 1 and packet_counter == 359 and self.frame_handler:
                    self.frame_handler()

    def iso_ready(self, transfer: usb.USBTransfer):
        buffer_list = transfer.getISOBufferList()
        setup_list = transfer.getISOSetupList()
        self.build_images(buffer_list, setup_list)

        # Because this is a callback, we need to make sure that
        # we don't try and submit if we're not in a ready state
        if self.ready:
            try:
                # Submits the transfer, it will get called again
                transfer.submit()
            except usb.USBError as e:
                print("Unable to submit transfer", e)

    def test(self):
        protocol.begin_audio_capture(self.device_handle)
        #protocol.set_input(self.device_handle, "S-Video")
