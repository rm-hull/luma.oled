#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1306
from luma.core.render import canvas

from baseline_data import primitives, get_json_data
from helpers import serial, call, setup_function, assert_invalid_dimensions  # noqa: F401


def test_init_128x64():
    """
    SSD1306 OLED with a 128 x 64 resolution works correctly.
    """
    ssd1306(serial)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 63, 211, 0, 64, 141, 20, 32, 0,
             161, 200, 218, 18, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 0, 127, 34, 0, 7),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next are all data: zero's to clear the RAM
    serial.data.assert_called_once_with([0] * (128 * 64 // 8))


def test_init_128x32():
    """
    SSD1306 OLED with a 128 x 32 resolution works correctly.
    """
    ssd1306(serial, width=128, height=32)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 31, 211, 0, 64, 141, 20, 32, 0,
             161, 200, 218, 2, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 0, 127, 34, 0, 3),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next bytes are all data: zero's to clear the RAM
    serial.data.assert_called_once_with([0] * (128 * 32 // 8))


def test_init_96x16():
    """
    SSD1306 OLED with a 96 x 16 resolution works correctly.
    """
    ssd1306(serial, width=96, height=16)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 96, 168, 15, 211, 0, 64, 141, 20, 32, 0,
             161, 200, 218, 2, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 16, 111, 34, 0, 1),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next bytes are all data: zero's to clear the RAM
    serial.data.assert_called_once_with([0] * (96 * 16 // 8))


def test_init_64x48():
    """
    SSD1306 OLED with a 64 x 48 resolution works correctly.
    """
    ssd1306(serial, width=64, height=48)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 47, 211, 0, 64, 141, 20, 32, 0,
             161, 200, 218, 18, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 32, 95, 34, 0, 5),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next bytes are all data: zero's to clear the RAM
    serial.data.assert_called_once_with([0] * (64 * 48 // 8))


def test_init_64x32():
    """
    SSD1306 OLED with a 64 x 32 resolution works correctly.
    """
    ssd1306(serial, width=64, height=32)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 31, 211, 0, 64, 141, 20, 32, 0,
             161, 200, 218, 18, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 32, 95, 34, 0, 3),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next bytes are all data: zero's to clear the RAM
    serial.data.assert_called_once_with([0] * (64 * 32 // 8))


def test_init_invalid_dimensions():
    """
    SSD1306 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1306, serial, 59, 22)


def test_hide():
    """
    SSD1306 OLED screen content can be hidden.
    """
    device = ssd1306(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1306 OLED screen content can be displayed.
    """
    device = ssd1306(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    """
    SSD1306 OLED screen can draw and display an image.
    """
    device = ssd1306(serial)
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(33, 0, 127, 34, 0, 7)

    # Next 1024 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_json_data('demo_ssd1306'))
