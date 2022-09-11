# Copyright (c) 2013 Federico Ruiz Ugalde
# Author: Federico Ruiz-Ugalde <memeruiz at gmail dot com>
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


def control_read(device_handle: usb.USBDeviceHandle, request: int, value: int, index: int, length: int) -> bytes:
    reply = device_handle.controlRead(
        usb.libusb1.LIBUSB_TYPE_VENDOR | usb.libusb1.LIBUSB_RECIPIENT_DEVICE,
        request, value, index, length)
    #print("Control read: request=%02x value=%04x index=%04x length=%d reply=%02x" % (request, value, index, length, reply[0]))
    return reply

def control_write(device_handle: usb.USBDeviceHandle, request: int, value: int, index: int, data) -> int:
    reply = device_handle.controlWrite(
        usb.libusb1.LIBUSB_TYPE_VENDOR | usb.libusb1.LIBUSB_RECIPIENT_DEVICE,
        request, value, index, bytes(data, encoding='utf-8'))
    return reply

USBTV_BASE = 0xc000
USBTV_REQUEST_REG = 12

def set_registers(device_handle: usb.USBDeviceHandle, registers: list):
    for register in registers:
        index = register[0]
        value = register[1]

        reply = control_write(device_handle, USBTV_REQUEST_REG, value, index, '')
        if reply != 0:
            raise Exception("Unexpected reply %02x" % reply)

def set_standard(device_handle: usb.USBDeviceHandle, standard: str):
    AVPAL = [
		# "AVPAL" tuning sequence from .INF file
		[ USBTV_BASE + 0x0003, 0x0004 ],
		[ USBTV_BASE + 0x001a, 0x0068 ],
		[ USBTV_BASE + 0x0100, 0x00d3 ],
		[ USBTV_BASE + 0x010e, 0x0072 ],
		[ USBTV_BASE + 0x010f, 0x00a2 ],
		[ USBTV_BASE + 0x0112, 0x00b0 ],
		[ USBTV_BASE + 0x0115, 0x0015 ],
		[ USBTV_BASE + 0x0117, 0x0001 ],
		[ USBTV_BASE + 0x0118, 0x002c ],
		[ USBTV_BASE + 0x012d, 0x0010 ],
		[ USBTV_BASE + 0x012f, 0x0020 ],
		[ USBTV_BASE + 0x0220, 0x002e ],
		[ USBTV_BASE + 0x0225, 0x0008 ],
		[ USBTV_BASE + 0x024e, 0x0002 ],
		[ USBTV_BASE + 0x024f, 0x0002 ],
		[ USBTV_BASE + 0x0254, 0x0059 ],
		[ USBTV_BASE + 0x025a, 0x0016 ],
		[ USBTV_BASE + 0x025b, 0x0035 ],
		[ USBTV_BASE + 0x0263, 0x0017 ],
		[ USBTV_BASE + 0x0266, 0x0016 ],
		[ USBTV_BASE + 0x0267, 0x0036 ],
		# End image tuning
		[ USBTV_BASE + 0x024e, 0x0002 ],
		[ USBTV_BASE + 0x024f, 0x0002 ]
    ]

    AVNTSC = [
        # "AVNTSC" tuning sequence from .INF file
		[ USBTV_BASE + 0x0003, 0x0004 ],
		[ USBTV_BASE + 0x001a, 0x0079 ],
		[ USBTV_BASE + 0x0100, 0x00d3 ],
		[ USBTV_BASE + 0x010e, 0x0068 ],
		[ USBTV_BASE + 0x010f, 0x009c ],
		[ USBTV_BASE + 0x0112, 0x00f0 ],
		[ USBTV_BASE + 0x0115, 0x0015 ],
		[ USBTV_BASE + 0x0117, 0x0000 ],
		[ USBTV_BASE + 0x0118, 0x00fc ],
		[ USBTV_BASE + 0x012d, 0x0004 ],
		[ USBTV_BASE + 0x012f, 0x0008 ],
		[ USBTV_BASE + 0x0220, 0x002e ],
		[ USBTV_BASE + 0x0225, 0x0008 ],
		[ USBTV_BASE + 0x024e, 0x0002 ],
		[ USBTV_BASE + 0x024f, 0x0001 ],
		[ USBTV_BASE + 0x0254, 0x005f ],
		[ USBTV_BASE + 0x025a, 0x0012 ],
		[ USBTV_BASE + 0x025b, 0x0001 ],
		[ USBTV_BASE + 0x0263, 0x001c ],
		[ USBTV_BASE + 0x0266, 0x0011 ],
		[ USBTV_BASE + 0x0267, 0x0005 ],
		# End image tuning
		[ USBTV_BASE + 0x024e, 0x0002 ],
		[ USBTV_BASE + 0x024f, 0x0002 ],
    ]

    AVSECAM = [
		# "AVSECAM" tuning sequence from .INF file
		[ USBTV_BASE + 0x0003, 0x0004 ],
		[ USBTV_BASE + 0x001a, 0x0073 ],
		[ USBTV_BASE + 0x0100, 0x00dc ],
		[ USBTV_BASE + 0x010e, 0x0072 ],
		[ USBTV_BASE + 0x010f, 0x00a2 ],
		[ USBTV_BASE + 0x0112, 0x0090 ],
		[ USBTV_BASE + 0x0115, 0x0035 ],
		[ USBTV_BASE + 0x0117, 0x0001 ],
		[ USBTV_BASE + 0x0118, 0x0030 ],
		[ USBTV_BASE + 0x012d, 0x0004 ],
		[ USBTV_BASE + 0x012f, 0x0008 ],
		[ USBTV_BASE + 0x0220, 0x002d ],
		[ USBTV_BASE + 0x0225, 0x0028 ],
		[ USBTV_BASE + 0x024e, 0x0008 ],
		[ USBTV_BASE + 0x024f, 0x0002 ],
		[ USBTV_BASE + 0x0254, 0x0069 ],
		[ USBTV_BASE + 0x025a, 0x0016 ],
		[ USBTV_BASE + 0x025b, 0x0035 ],
		[ USBTV_BASE + 0x0263, 0x0021 ],
		[ USBTV_BASE + 0x0266, 0x0016 ],
		[ USBTV_BASE + 0x0267, 0x0036 ],
		# End image tuning
		[ USBTV_BASE + 0x024e, 0x0002 ],
		[ USBTV_BASE + 0x024f, 0x0002 ],
    ]

    if standard == "NTSC":
        set_registers(device_handle, AVNTSC)
        norm = 0x00b8
    elif standard == "PAL":
        set_registers(device_handle, AVPAL)
        norm = 0x00ee
    elif standard == "SECAM":
        print("WARNING: SECAM not tested")
        set_registers(device_handle, AVSECAM)
        norm = 0x00ff
    else:
        raise ValueError("Unknown encoding: %s" % standard)

    # Set the norm (not really sure what this is, and there seem to be more options in the Linux driver)
    set_registers(device_handle, [ [ USBTV_BASE + 0x016f, norm ] ])

def set_input(device_handle, input):
    COMPOSITE = [
		[ USBTV_BASE + 0x0105, 0x0060 ],
		[ USBTV_BASE + 0x011f, 0x00f2 ],
		[ USBTV_BASE + 0x0127, 0x0060 ],
		[ USBTV_BASE + 0x00ae, 0x0010 ],
		[ USBTV_BASE + 0x0239, 0x0060 ],
    ]

    SVIDEO = [
		[ USBTV_BASE + 0x0105, 0x0010 ],
		[ USBTV_BASE + 0x011f, 0x00ff ],
		[ USBTV_BASE + 0x0127, 0x0060 ],
		[ USBTV_BASE + 0x00ae, 0x0030 ],
		[ USBTV_BASE + 0x0239, 0x0060 ],
    ]

    if input == "S-Video":
        set_registers(device_handle, SVIDEO)
    elif input == "Composite":
        set_registers(device_handle, COMPOSITE)
    else:
        raise ValueError("Unknown input: %s" % input)

def begin_capture(device_handle):
    SETUP = [
		# These seem to enable the device.
		[ USBTV_BASE + 0x0008, 0x0001 ],
		[ USBTV_BASE + 0x01d0, 0x00ff ],
		[ USBTV_BASE + 0x01d9, 0x0002 ],

		# These seem to influence color parameters, such as
		#  brightness, etc.
		[ USBTV_BASE + 0x0239, 0x0040 ],
		[ USBTV_BASE + 0x0240, 0x0000 ],
		[ USBTV_BASE + 0x0241, 0x0000 ],
		[ USBTV_BASE + 0x0242, 0x0002 ],
		[ USBTV_BASE + 0x0243, 0x0080 ],
		[ USBTV_BASE + 0x0244, 0x0012 ],
		[ USBTV_BASE + 0x0245, 0x0090 ],
		[ USBTV_BASE + 0x0246, 0x0000 ],

		[ USBTV_BASE + 0x0278, 0x002d ],
		[ USBTV_BASE + 0x0279, 0x000a ],
		[ USBTV_BASE + 0x027a, 0x0032 ],
		[ 0xf890, 0x000c ],
		[ 0xf894, 0x0086 ],

		[ USBTV_BASE + 0x00ac, 0x00c0 ],
		[ USBTV_BASE + 0x00ad, 0x0000 ],
		[ USBTV_BASE + 0x00a2, 0x0012 ],
		[ USBTV_BASE + 0x00a3, 0x00e0 ],
		[ USBTV_BASE + 0x00a4, 0x0028 ],
		[ USBTV_BASE + 0x00a5, 0x0082 ],
		[ USBTV_BASE + 0x00a7, 0x0080 ],
		[ USBTV_BASE + 0x0000, 0x0014 ],
		[ USBTV_BASE + 0x0006, 0x0003 ],
		[ USBTV_BASE + 0x0090, 0x0099 ],
		[ USBTV_BASE + 0x0091, 0x0090 ],
		[ USBTV_BASE + 0x0094, 0x0068 ],
		[ USBTV_BASE + 0x0095, 0x0070 ],
		[ USBTV_BASE + 0x009c, 0x0030 ],
		[ USBTV_BASE + 0x009d, 0x00c0 ],
		[ USBTV_BASE + 0x009e, 0x00e0 ],
		[ USBTV_BASE + 0x0019, 0x0006 ],
		[ USBTV_BASE + 0x008c, 0x00ba ],
		[ USBTV_BASE + 0x0101, 0x00ff ],
		[ USBTV_BASE + 0x010c, 0x00b3 ],
		[ USBTV_BASE + 0x01b2, 0x0080 ],
		[ USBTV_BASE + 0x01b4, 0x00a0 ],
		[ USBTV_BASE + 0x014c, 0x00ff ],
		[ USBTV_BASE + 0x014d, 0x00ca ],
		[ USBTV_BASE + 0x0113, 0x0053 ],
		[ USBTV_BASE + 0x0119, 0x008a ],
		[ USBTV_BASE + 0x013c, 0x0003 ],
		[ USBTV_BASE + 0x0150, 0x009c ],
		[ USBTV_BASE + 0x0151, 0x0071 ],
		[ USBTV_BASE + 0x0152, 0x00c6 ],
		[ USBTV_BASE + 0x0153, 0x0084 ],
		[ USBTV_BASE + 0x0154, 0x00bc ],
		[ USBTV_BASE + 0x0155, 0x00a0 ],
		[ USBTV_BASE + 0x0156, 0x00a0 ],
		[ USBTV_BASE + 0x0157, 0x009c ],
		[ USBTV_BASE + 0x0158, 0x001f ],
		[ USBTV_BASE + 0x0159, 0x0006 ],
		[ USBTV_BASE + 0x015d, 0x0000 ],
    ]

    set_registers(device_handle, SETUP)


## AUDIO

import pyaudio

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                output=True)

def audio_callback(transfer: usb.USBTransfer):
    buffer = transfer.getBuffer()
    
    stream.write(bytes(buffer[4:-12]))

    transfer.submit()


def begin_audio_capture(device_handle: usb.USBDeviceHandle):
    SETUP = [
	    # These seem to enable the device.
        [ USBTV_BASE + 0x0008, 0x0001 ],
        [ USBTV_BASE + 0x01d0, 0x00ff ],
        [ USBTV_BASE + 0x01d9, 0x0002 ],

		[ USBTV_BASE + 0x01da, 0x0013 ],
		[ USBTV_BASE + 0x01db, 0x0012 ],
		[ USBTV_BASE + 0x01e9, 0x0002 ],
		[ USBTV_BASE + 0x01ec, 0x006c ],
		[ USBTV_BASE + 0x0294, 0x0020 ],
		[ USBTV_BASE + 0x0255, 0x00cf ],
		[ USBTV_BASE + 0x0256, 0x0020 ],
		[ USBTV_BASE + 0x01eb, 0x0030 ],
		[ USBTV_BASE + 0x027d, 0x00a6 ],
		[ USBTV_BASE + 0x0280, 0x0011 ],
		[ USBTV_BASE + 0x0281, 0x0040 ],
		[ USBTV_BASE + 0x0282, 0x0011 ],
		[ USBTV_BASE + 0x0283, 0x0040 ],
		[ 0xf891, 0x0010 ],

		# this sets the input from composite
		[ USBTV_BASE + 0x0284, 0x00aa ],
	]

    transfer = device_handle.getTransfer(1)
    # Note that this is a bulk transfer, not an isochronous transfer.
    # Orignally this had a *really* large buffer (20480), but it wasn't getting filled...
    transfer.setBulk(0x83, buffer_or_len=256, callback=audio_callback, timeout=1000)

    set_registers(device_handle, SETUP)
    
    transfer.submit()