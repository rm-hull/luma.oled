#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1316
from luma.core.render import canvas

from baseline_data import primitives, get_reference_data
from helpers import serial, assert_invalid_dimensions, setup_function  # noqa: F401
from unittest.mock import call

def test_init_128x32():
    """
    SSD1316 OLED with a 128 x 32 resolution works correctly.
    """
    ssd1316(serial)
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

    # Next are all data: zero's to clear the RAM
    serial.data.assert_called_once_with([0] * (128 * 32 // 8))


def test_init_invalid_dimensions():
    """
    SSD1316 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1316, serial, 59, 22)


def test_hide():
    """
    SSD1316 OLED screen content can be hidden.
    """
    device = ssd1316(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1316 OLED screen content can be displayed.
    """
    device = ssd1316(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    """
    SSD1316 OLED screen can draw and display an image.
    """
    device = ssd1316(serial)
    serial.reset_mock()

    with canvas(device) as draw:
        primitives(device, draw)

    serial.command.assert_called_once_with(33, 0, 127, 34, 0, 3)
    serial.data.assert_called_once_with(get_reference_data('demo_ssd1316'))
