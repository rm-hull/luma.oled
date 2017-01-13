#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock

import pytest
import luma.core.error
from luma.oled.device import ssd1306
from luma.core.render import canvas
import baseline_data

serial = Mock(unsafe=True)


def setup_function(function):
    serial.reset_mock()
    serial.command.side_effect = None


def test_init_128x64():
    ssd1306(serial)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 63, 211, 0, 64, 141, 20, 32, 0,
             160, 200, 218, 18, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 0, 127, 34, 0, 7),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next 1024 are all data: zero's to clear the RAM
    # (1024 = 128 * 64 / 8)
    serial.data.assert_called_once_with([0] * (128 * 64 // 8))


def test_init_128x32():
    ssd1306(serial, width=128, height=32)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 31, 211, 0, 64, 141, 20, 32, 0,
             160, 200, 218, 2, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 0, 127, 34, 0, 3),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next 512 are all data: zero's to clear the RAM
    # (512 = 128 * 32 / 8)
    serial.data.assert_called_once_with([0] * (128 * 32 // 8))


def test_init_96x16():
    ssd1306(serial, width=96, height=16)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 96, 168, 15, 211, 0, 64, 141, 20, 32, 0,
             160, 200, 218, 2, 217, 241, 219, 64, 164, 166),
        # set contrast
        call(129, 207),
        # reset the display
        call(33, 0, 95, 34, 0, 1),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next 192 are all data: zero's to clear the RAM
    # (192 = 96 * 16 / 8)
    serial.data.assert_called_once_with([0] * (96 * 16 // 8))


def test_init_invalid_dimensions():
    with pytest.raises(luma.core.error.DeviceDisplayModeError) as ex:
        ssd1306(serial, width=59, height=22)
    assert "Unsupported display mode: 59 x 22" in str(ex.value)


def test_hide():
    device = ssd1306(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    device = ssd1306(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    device = ssd1306(serial)
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(33, 0, 127, 34, 0, 7)

    # Next 1024 bytes are data representing the drawn image
    serial.data.assert_called_once_with(baseline_data.demo_ssd1306)
