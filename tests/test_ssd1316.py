#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1316
from luma.core.render import canvas
from luma.oled.const import ssd1306 as ssd1306_const

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
        call(ssd1306_const.DISPLAYOFF, ssd1306_const.SETDISPLAYCLOCKDIV, 128,
             ssd1306_const.SETMULTIPLEX, 31, ssd1306_const.SETDISPLAYOFFSET, 0,
             ssd1306_const.SETSTARTLINE, ssd1306_const.CHARGEPUMP, 20,
             ssd1306_const.MEMORYMODE, 0, ssd1306_const.SETSEGMENTREMAP,
             ssd1306_const.COMSCANDEC, ssd1306_const.SETCOMPINS, 2,
             ssd1306_const.SETPRECHARGE, 241, ssd1306_const.SETVCOMDETECT, 64,
             ssd1306_const.DISPLAYALLON_RESUME, ssd1306_const.NORMALDISPLAY),
        # set contrast
        call(ssd1306_const.SETCONTRAST, 207),
        # reset the display
        call(ssd1306_const.COLUMNADDR, 0, 127, ssd1306_const.PAGEADDR, 0, 3),
        # called last, is a command to show the screen
        call(ssd1306_const.DISPLAYON)
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
    serial.command.assert_called_once_with(ssd1306_const.DISPLAYOFF)


def test_show():
    """
    SSD1316 OLED screen content can be displayed.
    """
    device = ssd1316(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(ssd1306_const.DISPLAYON)


def test_display():
    """
    SSD1316 OLED screen can draw and display an image.
    """
    device = ssd1316(serial)
    serial.reset_mock()

    with canvas(device) as draw:
        primitives(device, draw)

    serial.command.assert_called_once_with(ssd1306_const.COLUMNADDR, 0, 127, ssd1306_const.PAGEADDR, 0, 3)
    serial.data.assert_called_once_with(get_reference_data('demo_ssd1316'))
