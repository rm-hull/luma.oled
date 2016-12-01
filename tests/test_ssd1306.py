#!/usr/bin/env python

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock

from oled.device import ssd1306
from oled.render import canvas
import baseline_data

serial = Mock()


def setup_function(function):
    serial.reset_mock()


def test_init():
    ssd1306(serial)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 63, 211, 0, 64, 141, 20, 32, 0, 160,
             200, 218, 18, 129, 207, 217, 241, 219, 64, 164, 166),
        # reset the display
        call(33, 0, 127, 34, 0, 7),
        # called last, is a command to show the screen
        call(175)
    ])

    # Next 1024 are all data: zero's to clear the RAM
    # (1024 = 128 * 64 / 8)
    serial.data.assert_called_once_with([0] * 1024)


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
