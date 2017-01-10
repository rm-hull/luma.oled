#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock

import pytest
import luma.core.error
from luma.oled.device import ssd1325
from luma.core.render import canvas
import baseline_data

serial = Mock(unsafe=True)


def setup_function(function):
    serial.reset_mock()
    serial.command.side_effect = None


def test_init_128x64():
    ssd1325(serial)
    serial.command.assert_has_calls([
        call(174, 179, 241, 168, 63, 162, 76, 161, 0, 173, 2, 160, 80, 134, 184, 1, 17, 34, 50, 67, 84, 101, 118),
        call(129, 255),
        call(178, 81, 177, 85, 180, 2, 176, 40, 190, 28, 191, 15, 164),
        call(21, 0, 127, 117, 0, 63),
        call(175)
    ])

    # Next 4096 are all data: zero's to clear the RAM
    # (4096 = 128 * 64 / 2)
    serial.data.assert_called_once_with([0] * (128 * 64 // 2))


def test_init_invalid_dimensions():
    with pytest.raises(luma.core.error.DeviceDisplayModeError) as ex:
        ssd1325(serial, width=128, height=77)
    assert "Unsupported display mode: 128 x 77" in str(ex.value)


def test_hide():
    device = ssd1325(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    device = ssd1325(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    device = ssd1325(serial)
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 127, 117, 0, 63)

    # Next 4096 bytes are data representing the drawn image
    serial.data.assert_called_once_with(baseline_data.demo_ssd1325)
