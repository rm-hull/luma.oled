#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1309
from luma.core.render import canvas

from baseline_data import primitives, get_reference_data
from helpers import serial, assert_invalid_dimensions, setup_function  # noqa: F401
from unittest.mock import call


def test_init_128x64():
    """
    SSD1309 OLED with a 128 x 64 resolution works correctly.
    """
    ssd1309(serial)
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


def test_init_invalid_dimensions():
    """
    SSD1309 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1309, serial, 59, 22)


def test_hide():
    """
    SSD1309 OLED screen content can be hidden.
    """
    device = ssd1309(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1309 OLED screen content can be displayed.
    """
    device = ssd1309(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    """
    SSD1309 OLED screen can draw and display an image.
    """
    device = ssd1309(serial)
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(33, 0, 127, 34, 0, 7)

    # To regenerate test data, uncomment the following (remember not to commit though)
    # ================================================================================
    # from baseline_data import save_reference_data
    # save_reference_data("demo_ssd1309", serial.data.call_args.args[0])

    # Next 1024 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_reference_data('demo_ssd1309'))
