#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock

import pytest
from oled.device import ssd1331
from oled.render import canvas
import baseline_data

serial = Mock(unsafe=True)


def setup_function(function):
    serial.reset_mock()
    serial.command.side_effect = None


def test_init_96x64():
    ssd1331(serial)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 160, 114, 161, 0, 162, 0, 164, 168, 63, 173,
             142, 176, 11, 177, 116, 179, 208, 138, 128, 139,
             128, 140, 128, 187, 62, 190, 62, 135, 15),
        # set contrast
        call(129, 255, 130, 255, 131, 255),
        # reset the display
        call(21, 0, 95, 117, 0, 63),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next 1024 are all data: zero's to clear the RAM
    # (12288 = 96 * 64 * 2)
    serial.data.assert_called_once_with([0] * 96 * 64 * 2)


def test_init_invalid_dimensions():
    with pytest.raises(ValueError) as ex:
        ssd1331(serial, width=23, height=57)
    assert "Unsupported display mode: 23x57" in str(ex.value)


def test_init_handle_ioerror():
    serial.command.side_effect = IOError(-99, "Test exception")
    with pytest.raises(IOError) as ex:
        ssd1331(serial)
    assert "Failed to initialize SSD1331 display driver" in str(ex.value)


def test_hide():
    device = ssd1331(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    device = ssd1331(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    device = ssd1331(serial)
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 95, 117, 0, 63)

    # Next 1024 bytes are data representing the drawn image
    serial.data.assert_called_once_with(baseline_data.demo_ssd1331)
