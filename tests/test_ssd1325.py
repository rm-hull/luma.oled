#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1325
from luma.core.render import canvas

from baseline_data import get_json_data, primitives
from helpers import call, serial, setup_function, assert_invalid_dimensions  # noqa: F401


def test_init_128x64():
    """
    SSD1325 OLED with a 128 x 64 resolution works correctly.
    """
    ssd1325(serial)
    serial.command.assert_has_calls([
        call(174, 179, 242, 168, 63, 162, 76, 161, 0, 173, 2, 160, 80, 134, 184,
             1, 17, 34, 50, 67, 84, 101, 118, 178, 81, 177, 85, 180, 3, 176, 40,
             188, 1, 190, 0, 191, 2, 164),
        call(129, 127),
        call(21, 0, 63, 117, 0, 63),
        call(175)
    ])

    # Next 4096 are all data: zero's to clear the RAM
    # (4096 = 128 * 64 / 2)
    serial.data.assert_called_once_with([0] * (128 * 64 // 2))


def test_init_invalid_dimensions():
    """
    SSD1325 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1325, serial, 128, 77)


def test_hide():
    """
    SSD1325 OLED screen content can be hidden.
    """
    device = ssd1325(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1325 OLED screen content can be displayed.
    """
    device = ssd1325(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_greyscale_display():
    """
    SSD1325 OLED screen can draw and display a greyscale image.
    """
    device = ssd1325(serial, mode="RGB")
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 63, 117, 0, 63)

    # Next 4096 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_json_data('demo_ssd1325_greyscale'))


def test_monochrome_display():
    """
    SSD1325 OLED screen can draw and display a monochrome image.
    """
    device = ssd1325(serial, mode="1")
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 63, 117, 0, 63)

    # Next 4096 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_json_data('demo_ssd1325_monochrome'))


def test_framebuffer_override():
    """
    Reproduce https://github.com/rm-hull/luma.examples/issues/95
    """
    ssd1325(serial, mode="1", framebuffer="diff_to_previous")
