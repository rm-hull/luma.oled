#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1362
from luma.core.render import canvas

from baseline_data import get_json_data, primitives
from helpers import call, serial, setup_function, assert_invalid_dimensions  # noqa: F401


def test_init_256x64():
    """
    SSD1362 OLED with a 256 x 64 resolution works correctly.
    """
    ssd1362(serial)
    serial.command.assert_has_calls([
        call(171, 1, 173, 158, 21, 0, 127, 117, 0, 63, 160, 67, 161, 0, 162, 0, 164, 168, 63, 177, 17, 179, 240, 185, 188, 4, 190, 5),
        call(129, 127),
        call(21, 0, 127, 117, 0, 63),
        call(175)
    ])

    # Next 4096 are all data: zero's to clear the RAM
    # (4096 = 128 * 64 / 2)
    serial.data.assert_called_once_with([0] * (256 * 64 // 2))


def test_init_invalid_dimensions():
    """
    SSD1362 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1362, serial, 128, 77)


def test_hide():
    """
    SSD1362 OLED screen content can be hidden.
    """
    device = ssd1362(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1362 OLED screen content can be displayed.
    """
    device = ssd1362(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_greyscale_display():
    """
    SSD1362 OLED screen can draw and display a greyscale image.
    """
    device = ssd1362(serial, mode="RGB")
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 127, 117, 0, 63)

    # Next 4096 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_json_data('demo_ssd1362_greyscale'))


def test_monochrome_display():
    """
    SSD1362 OLED screen can draw and display a monochrome image.
    """
    device = ssd1362(serial, mode="1")
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 127, 117, 0, 63)

    # Next 4096 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_json_data('demo_ssd1362_monochrome'))
