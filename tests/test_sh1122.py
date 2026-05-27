#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2026 Richard Hull and contributors
# See LICENSE.rst for details.

from unittest.mock import call

from PIL import Image

from luma.core.framebuffer import diff_to_previous, full_frame
from luma.oled.device import sh1122

from helpers import serial, assert_invalid_dimensions, setup_function  # noqa: F401


def test_init_256x64():
    """
    SH1122 OLED with a 256 x 64 resolution initializes and clears RAM row by row.
    """
    sh1122(serial, framebuffer=full_frame())

    serial.command.assert_any_call(
        0xAE, 0x40, 0x30, 0xAD, 0x81, 0xA0, 0xC0, 0xA8, 0x3F,
        0xD3, 0x00, 0xD5, 0x90, 0xD9, 0x76, 0xDB, 0x3B, 0xDC,
        0x1A, 0xA6, 0xA4)
    serial.command.assert_any_call(0x81, 0x7F)
    serial.command.assert_any_call(0xB0, 0x00, 0x00, 0x10)
    serial.command.assert_any_call(0xB0, 0x3F, 0x00, 0x10)
    serial.command.assert_called_with(0xAF)

    assert serial.data.call_count == 64
    serial.data.assert_has_calls([call([0] * 128)] * 64)


def test_init_external_dcdc():
    """
    SH1122 OLED can be initialized for modules with an external VPP supply.
    """
    sh1122(serial, framebuffer=full_frame(), dcdc=False)

    serial.command.assert_any_call(
        0xAE, 0x40, 0x30, 0xAD, 0x80, 0xA0, 0xC0, 0xA8, 0x3F,
        0xD3, 0x00, 0xD5, 0x90, 0xD9, 0x76, 0xDB, 0x3B, 0xDC,
        0x1A, 0xA6, 0xA4)


def test_init_invalid_dimensions():
    """
    SH1122 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(sh1122, serial, 128, 64)


def test_hide():
    """
    SH1122 OLED screen content can be hidden.
    """
    device = sh1122(serial, framebuffer=full_frame())
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(0xAE)


def test_show():
    """
    SH1122 OLED screen content can be displayed.
    """
    device = sh1122(serial, framebuffer=full_frame())
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(0xAF)


def test_greyscale_display():
    """
    SH1122 OLED screen can draw and display a greyscale RGB image.
    """
    device = sh1122(serial, mode="RGB", framebuffer=full_frame())
    serial.reset_mock()

    image = Image.new("RGB", device.size)
    image.putpixel((0, 0), (255, 255, 255))
    image.putpixel((1, 0), (16, 16, 16))
    image.putpixel((2, 0), (255, 0, 0))
    image.putpixel((3, 1), (0, 255, 0))

    device.display(image)

    assert serial.command.call_count == 64
    assert serial.data.call_count == 64
    assert serial.command.call_args_list[0] == call(0xB0, 0x00, 0x00, 0x10)
    assert serial.command.call_args_list[1] == call(0xB0, 0x01, 0x00, 0x10)
    assert serial.command.call_args_list[-1] == call(0xB0, 0x3F, 0x00, 0x10)

    row0 = serial.data.call_args_list[0].args[0]
    row1 = serial.data.call_args_list[1].args[0]
    assert row0[:4] == [0xF1, 0x40, 0x00, 0x00]
    assert row1[:4] == [0x00, 0x09, 0x00, 0x00]


def test_monochrome_display():
    """
    SH1122 OLED screen can draw and display a monochrome image.
    """
    device = sh1122(serial, mode="1", framebuffer=full_frame())
    serial.reset_mock()

    image = Image.new("1", device.size)
    image.putpixel((0, 0), 1)
    image.putpixel((1, 0), 1)
    image.putpixel((2, 0), 1)

    device.display(image)

    row0 = serial.data.call_args_list[0].args[0]
    assert row0[:4] == [0xFF, 0xF0, 0x00, 0x00]


def test_partial_framebuffer_aligns_to_pixel_pair():
    """
    SH1122 partial redraws align the update to a 2-pixel RAM column.
    """
    framebuffer = diff_to_previous(num_segments=1)
    device = sh1122(serial, mode="1", framebuffer=framebuffer)
    first = Image.new("1", device.size)
    device.display(first)

    serial.reset_mock()

    second = first.copy()
    second.putpixel((3, 2), 1)
    device.display(second)

    serial.command.assert_called_once_with(0xB0, 0x02, 0x01, 0x10)
    serial.data.assert_called_once_with([0x0F])
