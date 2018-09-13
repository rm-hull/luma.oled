#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

import pytest

from luma.oled.device import ssd1331
from luma.core.render import canvas

from baseline_data import get_json_data, primitives
from helpers import call, serial, setup_function, assert_invalid_dimensions  # noqa: F401


def test_init_96x64():
    """
    SSD1331 OLED with a 96 x 64 resolution works correctly.
    """
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

    # Next 12288 are all data: zero's to clear the RAM
    # (12288 = 96 * 64 * 2)
    serial.data.assert_called_once_with([0] * 96 * 64 * 2)


def test_init_invalid_dimensions():
    """
    SSD1331 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1331, serial, 23, 57)


def test_hide():
    """
    SSD1331 OLED screen content can be hidden.
    """
    device = ssd1331(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1331 OLED screen content can be displayed.
    """
    device = ssd1331(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    """
    SSD1331 OLED screen can draw and display an image.
    """
    device = ssd1331(serial)
    serial.reset_mock()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    # Initial command to reset the display
    serial.command.assert_called_once_with(21, 0, 95, 117, 0, 63)

    # Next 12288 bytes are data representing the drawn image
    serial.data.assert_called_once_with(get_json_data('demo_ssd1331'))


@pytest.mark.parametrize("bit,expected_16_bit_color", [
    (7, [0b10000100, 0b00010000]),
    (6, [0b01000010, 0b00001000]),
    (5, [0b00100001, 0b00000100]),
    (4, [0b00010000, 0b10000010]),
    (3, [0b00001000, 0b01000001]),
    (2, [0b00000000, 0b00100000]),
    (1, [0b00000000, 0b00000000]),
    (0, [0b00000000, 0b00000000]),
])
def test_16bit_rgb_packing(bit, expected_16_bit_color):
    """
    Checks that 8 bit red component is packed into first 5 bits
    Checks that 8 bit green component is packed into next 6 bits
    Checks that 8 bit blue component is packed into remaining 5 bits
    """
    device = ssd1331(serial)
    serial.reset_mock()

    rgb_color = (2 ** bit,) * 3
    expected = expected_16_bit_color * device.width * device.height

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline=rgb_color, fill=rgb_color)

    serial.data.assert_called_once_with(expected)
