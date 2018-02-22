#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1351
from luma.core.render import canvas

from baseline_data import get_json_data, primitives
from helpers import serial, setup_function, assert_invalid_dimensions  # noqa: F401


def test_init_128x128():
    """
    SSD1351 OLED with a 128 x 128 resolution works correctly.
    """
    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command.side_effect = command
    serial.data.side_effect = data

    ssd1351(serial)

    assert serial.data.called
    assert serial.command.called

    assert recordings == [
        {'command': [253]}, {'data': [18]},
        {'command': [253]}, {'data': [177]},
        {'command': [174]},
        {'command': [179]}, {'data': [241]},
        {'command': [202]}, {'data': [127]},
        {'command': [21]}, {'data': [0, 127]},
        {'command': [117]}, {'data': [0, 127]},
        {'command': [160]}, {'data': [116]},
        {'command': [161]}, {'data': [0]},
        {'command': [162]}, {'data': [0]},
        {'command': [181]}, {'data': [0]},
        {'command': [171]}, {'data': [1]},
        {'command': [177]}, {'data': [50]},
        {'command': [180]}, {'data': [160, 181, 85]},
        {'command': [190]}, {'data': [5]},
        {'command': [199]}, {'data': [15]},
        {'command': [182]}, {'data': [1]},
        {'command': [166]},
        {'command': [193]}, {'data': [255, 255, 255]},
        {'command': [21]}, {'data': [0, 127]},
        {'command': [117]}, {'data': [0, 127]},
        {'command': [92]}, {'data': [0] * (128 * 128 * 2)},
        {'command': [175]}
    ]


def test_init_96x96_with_BGR():
    """
    SSD1351 OLED with a 96 x 96 resolution and BGR pixels works correctly.
    """
    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command.side_effect = command
    serial.data.side_effect = data

    ssd1351(serial, width=96, height=96, bgr=True)

    assert serial.data.called
    assert serial.command.called

    assert recordings == [
        {'command': [253]}, {'data': [18]},
        {'command': [253]}, {'data': [177]},
        {'command': [174]},
        {'command': [179]}, {'data': [241]},
        {'command': [202]}, {'data': [127]},
        {'command': [21]}, {'data': [0, 95]},
        {'command': [117]}, {'data': [0, 95]},
        {'command': [160]}, {'data': [118]},
        {'command': [161]}, {'data': [0]},
        {'command': [162]}, {'data': [0]},
        {'command': [181]}, {'data': [0]},
        {'command': [171]}, {'data': [1]},
        {'command': [177]}, {'data': [50]},
        {'command': [180]}, {'data': [160, 181, 85]},
        {'command': [190]}, {'data': [5]},
        {'command': [199]}, {'data': [15]},
        {'command': [182]}, {'data': [1]},
        {'command': [166]},
        {'command': [193]}, {'data': [255, 255, 255]},
        {'command': [21]}, {'data': [0, 95]},
        {'command': [117]}, {'data': [0, 95]},
        {'command': [92]}, {'data': [0] * (96 * 96 * 2)},
        {'command': [175]}
    ]


def test_init_invalid_dimensions():
    """
    SSD1351 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1351, serial, 128, 77)


def test_hide():
    """
    SSD1351 OLED screen content can be hidden.
    """
    device = ssd1351(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1351 OLED screen content can be displayed.
    """
    device = ssd1351(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    """
    SSD1351 OLED screen can draw and display a color image.
    """
    device = ssd1351(serial)
    serial.reset_mock()

    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command.side_effect = command
    serial.data.side_effect = data

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    assert serial.data.called
    assert serial.command.called

    assert recordings == [
        {'command': [21]}, {'data': [0, 127]},
        {'command': [117]}, {'data': [0, 127]},
        {'command': [92]}, {'data': get_json_data('demo_ssd1351')}
    ]
