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


def control_read(
    device_handle: usb.USBDeviceHandle,
    request: int,
    value: int,
    index: int,
    length: int,
) -> bytes:
    reply = device_handle.controlRead(
        usb.libusb1.LIBUSB_TYPE_VENDOR | usb.libusb1.LIBUSB_RECIPIENT_DEVICE,
        request,
        value,
        index,
        length,
    )
    return reply


def control_write(
    device_handle: usb.USBDeviceHandle, request: int, value: int, index: int, data
) -> int:
    reply = device_handle.controlWrite(
        usb.libusb1.LIBUSB_TYPE_VENDOR | usb.libusb1.LIBUSB_RECIPIENT_DEVICE,
        request,
        value,
        index,
        bytes(data, encoding="utf-8"),
    )
    return reply


USBTV_BASE = 0xC000
USBTV_REQUEST_REG = 12


def set_registers(device_handle: usb.USBDeviceHandle, registers: list):
    for register in registers:
        index = register[0]
        value = register[1]

        reply = control_write(device_handle, USBTV_REQUEST_REG, value, index, "")
        if reply != 0:
            raise Exception("Unexpected reply %02x" % reply)


def set_standard(device_handle: usb.USBDeviceHandle, standard: str):
    AVPAL = [
        # "AVPAL" tuning sequence from .INF file
        [USBTV_BASE + 0x0003, 0x0004],
        [USBTV_BASE + 0x001A, 0x0068],
        [USBTV_BASE + 0x0100, 0x00D3],
        [USBTV_BASE + 0x010E, 0x0072],
        [USBTV_BASE + 0x010F, 0x00A2],
        [USBTV_BASE + 0x0112, 0x00B0],
        [USBTV_BASE + 0x0115, 0x0015],
        [USBTV_BASE + 0x0117, 0x0001],
        [USBTV_BASE + 0x0118, 0x002C],
        [USBTV_BASE + 0x012D, 0x0010],
        [USBTV_BASE + 0x012F, 0x0020],
        [USBTV_BASE + 0x0220, 0x002E],
        [USBTV_BASE + 0x0225, 0x0008],
        [USBTV_BASE + 0x024E, 0x0002],
        [USBTV_BASE + 0x024F, 0x0002],
        [USBTV_BASE + 0x0254, 0x0059],
        [USBTV_BASE + 0x025A, 0x0016],
        [USBTV_BASE + 0x025B, 0x0035],
        [USBTV_BASE + 0x0263, 0x0017],
        [USBTV_BASE + 0x0266, 0x0016],
        [USBTV_BASE + 0x0267, 0x0036],
        # End image tuning
        [USBTV_BASE + 0x024E, 0x0002],
        [USBTV_BASE + 0x024F, 0x0002],
    ]

    AVNTSC = [
        # "AVNTSC" tuning sequence from .INF file
        [USBTV_BASE + 0x0003, 0x0004],
        [USBTV_BASE + 0x001A, 0x0079],
        [USBTV_BASE + 0x0100, 0x00D3],
        [USBTV_BASE + 0x010E, 0x0068],
        [USBTV_BASE + 0x010F, 0x009C],
        [USBTV_BASE + 0x0112, 0x00F0],
        [USBTV_BASE + 0x0115, 0x0015],
        [USBTV_BASE + 0x0117, 0x0000],
        [USBTV_BASE + 0x0118, 0x00FC],
        [USBTV_BASE + 0x012D, 0x0004],
        [USBTV_BASE + 0x012F, 0x0008],
        [USBTV_BASE + 0x0220, 0x002E],
        [USBTV_BASE + 0x0225, 0x0008],
        [USBTV_BASE + 0x024E, 0x0002],
        [USBTV_BASE + 0x024F, 0x0001],
        [USBTV_BASE + 0x0254, 0x005F],
        [USBTV_BASE + 0x025A, 0x0012],
        [USBTV_BASE + 0x025B, 0x0001],
        [USBTV_BASE + 0x0263, 0x001C],
        [USBTV_BASE + 0x0266, 0x0011],
        [USBTV_BASE + 0x0267, 0x0005],
        # End image tuning
        [USBTV_BASE + 0x024E, 0x0002],
        [USBTV_BASE + 0x024F, 0x0002],
    ]

    AVSECAM = [
        # "AVSECAM" tuning sequence from .INF file
        [USBTV_BASE + 0x0003, 0x0004],
        [USBTV_BASE + 0x001A, 0x0073],
        [USBTV_BASE + 0x0100, 0x00DC],
        [USBTV_BASE + 0x010E, 0x0072],
        [USBTV_BASE + 0x010F, 0x00A2],
        [USBTV_BASE + 0x0112, 0x0090],
        [USBTV_BASE + 0x0115, 0x0035],
        [USBTV_BASE + 0x0117, 0x0001],
        [USBTV_BASE + 0x0118, 0x0030],
        [USBTV_BASE + 0x012D, 0x0004],
        [USBTV_BASE + 0x012F, 0x0008],
        [USBTV_BASE + 0x0220, 0x002D],
        [USBTV_BASE + 0x0225, 0x0028],
        [USBTV_BASE + 0x024E, 0x0008],
        [USBTV_BASE + 0x024F, 0x0002],
        [USBTV_BASE + 0x0254, 0x0069],
        [USBTV_BASE + 0x025A, 0x0016],
        [USBTV_BASE + 0x025B, 0x0035],
        [USBTV_BASE + 0x0263, 0x0021],
        [USBTV_BASE + 0x0266, 0x0016],
        [USBTV_BASE + 0x0267, 0x0036],
        # End image tuning
        [USBTV_BASE + 0x024E, 0x0002],
        [USBTV_BASE + 0x024F, 0x0002],
    ]

    if standard == "NTSC":
        set_registers(device_handle, AVNTSC)
        norm = 0x00B8
    elif standard == "PAL":
        set_registers(device_handle, AVPAL)
        norm = 0x00EE
    elif standard == "SECAM":
        print("WARNING: SECAM not tested")
        set_registers(device_handle, AVSECAM)
        norm = 0x00FF
    else:
        raise ValueError("Unknown encoding: %s" % standard)

    # Set the norm (not really sure what this is, and there seem to be more options in the Linux driver)
    set_registers(device_handle, [[USBTV_BASE + 0x016F, norm]])


def set_input(device_handle, input):
    COMPOSITE = [
        [USBTV_BASE + 0x0105, 0x0060],
        [USBTV_BASE + 0x011F, 0x00F2],
        [USBTV_BASE + 0x0127, 0x0060],
        [USBTV_BASE + 0x00AE, 0x0010],
        [USBTV_BASE + 0x0239, 0x0060],
    ]

    SVIDEO = [
        [USBTV_BASE + 0x0105, 0x0010],
        [USBTV_BASE + 0x011F, 0x00FF],
        [USBTV_BASE + 0x0127, 0x0060],
        [USBTV_BASE + 0x00AE, 0x0030],
        [USBTV_BASE + 0x0239, 0x0060],
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
        [USBTV_BASE + 0x0008, 0x0001],
        [USBTV_BASE + 0x01D0, 0x00FF],
        [USBTV_BASE + 0x01D9, 0x0002],
        # These seem to influence color parameters, such as
        #  brightness, etc.
        [USBTV_BASE + 0x0239, 0x0040],
        [USBTV_BASE + 0x0240, 0x0000],
        [USBTV_BASE + 0x0241, 0x0000],
        [USBTV_BASE + 0x0242, 0x0002],
        [USBTV_BASE + 0x0243, 0x0080],
        [USBTV_BASE + 0x0244, 0x0012],
        [USBTV_BASE + 0x0245, 0x0090],
        [USBTV_BASE + 0x0246, 0x0000],
        [USBTV_BASE + 0x0278, 0x002D],
        [USBTV_BASE + 0x0279, 0x000A],
        [USBTV_BASE + 0x027A, 0x0032],
        [0xF890, 0x000C],
        [0xF894, 0x0086],
        # Other setup values
        [USBTV_BASE + 0x00AC, 0x00C0],
        [USBTV_BASE + 0x00AD, 0x0000],
        [USBTV_BASE + 0x00A2, 0x0012],
        [USBTV_BASE + 0x00A3, 0x00E0],
        [USBTV_BASE + 0x00A4, 0x0028],
        [USBTV_BASE + 0x00A5, 0x0082],
        [USBTV_BASE + 0x00A7, 0x0080],
        [USBTV_BASE + 0x0000, 0x0014],
        [USBTV_BASE + 0x0006, 0x0003],
        [USBTV_BASE + 0x0090, 0x0099],
        [USBTV_BASE + 0x0091, 0x0090],
        [USBTV_BASE + 0x0094, 0x0068],
        [USBTV_BASE + 0x0095, 0x0070],
        [USBTV_BASE + 0x009C, 0x0030],
        [USBTV_BASE + 0x009D, 0x00C0],
        [USBTV_BASE + 0x009E, 0x00E0],
        [USBTV_BASE + 0x0019, 0x0006],
        [USBTV_BASE + 0x008C, 0x00BA],
        [USBTV_BASE + 0x0101, 0x00FF],
        [USBTV_BASE + 0x010C, 0x00B3],
        [USBTV_BASE + 0x01B2, 0x0080],
        [USBTV_BASE + 0x01B4, 0x00A0],
        [USBTV_BASE + 0x014C, 0x00FF],
        [USBTV_BASE + 0x014D, 0x00CA],
        [USBTV_BASE + 0x0113, 0x0053],
        [USBTV_BASE + 0x0119, 0x008A],
        [USBTV_BASE + 0x013C, 0x0003],
        [USBTV_BASE + 0x0150, 0x009C],
        [USBTV_BASE + 0x0151, 0x0071],
        [USBTV_BASE + 0x0152, 0x00C6],
        [USBTV_BASE + 0x0153, 0x0084],
        [USBTV_BASE + 0x0154, 0x00BC],
        [USBTV_BASE + 0x0155, 0x00A0],
        [USBTV_BASE + 0x0156, 0x00A0],
        [USBTV_BASE + 0x0157, 0x009C],
        [USBTV_BASE + 0x0158, 0x001F],
        [USBTV_BASE + 0x0159, 0x0006],
        [USBTV_BASE + 0x015D, 0x0000],
    ]

    set_registers(device_handle, SETUP)


## AUDIO

def enable_audio(device_handle: usb.USBDeviceHandle):
    SETUP = [
        # These seem to enable the device.
        [USBTV_BASE + 0x0008, 0x0001],
        [USBTV_BASE + 0x01D0, 0x00FF],
        [USBTV_BASE + 0x01D9, 0x0002],
        [USBTV_BASE + 0x01DA, 0x0013],
        [USBTV_BASE + 0x01DB, 0x0012],
        [USBTV_BASE + 0x01E9, 0x0002],
        [USBTV_BASE + 0x01EC, 0x006C],
        [USBTV_BASE + 0x0294, 0x0020],
        [USBTV_BASE + 0x0255, 0x00CF],
        [USBTV_BASE + 0x0256, 0x0020],
        [USBTV_BASE + 0x01EB, 0x0030],
        [USBTV_BASE + 0x027D, 0x00A6],
        [USBTV_BASE + 0x0280, 0x0011],
        [USBTV_BASE + 0x0281, 0x0040],
        [USBTV_BASE + 0x0282, 0x0011],
        [USBTV_BASE + 0x0283, 0x0040],
        [0xF891, 0x0010],
        # this sets the input from composite
        [USBTV_BASE + 0x0284, 0x00AA],
    ]

    set_registers(device_handle, SETUP)

def disable_audio(device_handle: usb.USBDeviceHandle):
    SETUP = [
        # The original windows driver sometimes sends also:
        #   [ USBTV_BASE + 0x00a2, 0x0013 ],
	    # but it seems useless and its real effects are untested at
	    # the moment.
	    #
		[ USBTV_BASE + 0x027d, 0x0000 ],
		[ USBTV_BASE + 0x0280, 0x0010 ],
		[ USBTV_BASE + 0x0282, 0x0010 ],
    ]

    set_registers(device_handle, SETUP)
