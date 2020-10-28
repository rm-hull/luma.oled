#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1327
from luma.core.render import canvas
from luma.core.framebuffer import diff_to_previous, full_frame

from baseline_data import get_reference_data, primitives
from helpers import serial, assert_invalid_dimensions, setup_function  # noqa: F401
from unittest.mock import call


def test_init_128x128():
    """
    SSD1327 OLED with a 128 x 128 resolution works correctly.
    """
    ssd1327(serial, framebuffer=full_frame())
    serial.command.assert_has_calls([
        call(174, 160, 83, 161, 0, 162, 0, 164, 168, 127),
        call(184, 1, 17, 34, 50, 67, 84, 101, 118),
        call(179, 0, 171, 1, 177, 241, 188, 8, 190, 7, 213, 98, 182, 15),
        call(129, 127),
        call(21, 0, 63, 117, 0, 127),
        call(175)
    ])

    # Next 4096 are all data: zero's to clear the RAM
    # (4096 = 128 * 128 / 2)
    serial.data.assert_called_once_with([0] * (128 * 128 // 2))


def test_init_invalid_dimensions():
    """
    SSD1327 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1327, serial, 128, 77)


def test_hide():
    """
    SSD1327 OLED screen content can be hidden.
    """
    device = ssd1327(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1327 OLED screen content can be displayed.
    """
    device = ssd1327(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_greyscale_display():
    """
    SSD1327 OLED screen can draw and display a greyscale image.
    """
    device = ssd1327(serial, mode="RGB", framebuffer=full_frame())
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 63, 117, 0, 127)

    # To regenerate test data, uncomment the following (remember not to commit though)
    # ================================================================================
    # from baseline_data import save_reference_data
    # save_reference_data("demo_ssd1327_greyscale", serial.data.call_args.args[0])

    # Next 4096 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_reference_data('demo_ssd1327_greyscale'))


def test_monochrome_display():
    """
    SSD1327 OLED screen can draw and display a monochrome image.
    """
    device = ssd1327(serial, mode="1", framebuffer=full_frame())
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 63, 117, 0, 127)

    # To regenerate test data, uncomment the following (remember not to commit though)
    # ================================================================================
    # from baseline_data import save_reference_data
    # save_reference_data("demo_ssd1327_monochrome", serial.data.call_args.args[0])

    # Next 4096 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_reference_data('demo_ssd1327_monochrome'))


def test_framebuffer_override():
    """
    Reproduce https://github.com/rm-hull/luma.examples/issues/95
    """
    ssd1327(serial, mode="1", framebuffer=diff_to_previous())
