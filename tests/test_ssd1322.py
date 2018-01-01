#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1322
from luma.core.render import canvas

from baseline_data import get_json_data, primitives
from helpers import serial, setup_function, assert_invalid_dimensions  # noqa: F401


def test_init_256x64():
    """
    SSD1322 OLED with a 256 x 64 resolution works correctly.
    """
    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command.side_effect = command
    serial.data.side_effect = data

    ssd1322(serial)

    assert serial.data.called
    assert serial.command.called

    assert recordings == [
        {'command': [253]}, {'data': [18]},
        {'command': [164]},
        {'command': [179]}, {'data': [242]},
        {'command': [202]}, {'data': [63]},
        {'command': [162]}, {'data': [0]},
        {'command': [161]}, {'data': [0]},
        {'command': [160]}, {'data': [20, 17]},
        {'command': [181]}, {'data': [0]},
        {'command': [171]}, {'data': [1]},
        {'command': [180]}, {'data': [160, 253]},
        {'command': [199]}, {'data': [15]},
        {'command': [185]},
        {'command': [177]}, {'data': [240]},
        {'command': [209]}, {'data': [130, 32]},
        {'command': [187]}, {'data': [13]},
        {'command': [182]}, {'data': [8]},
        {'command': [190]}, {'data': [0]},
        {'command': [166]},
        {'command': [169]},
        {'command': [193]}, {'data': [127]},
        {'command': [21]}, {'data': [28, 91]},
        {'command': [117]}, {'data': [0, 63]},
        {'command': [92]}, {'data': [0] * (256 * 64 // 2)},
        {'command': [175]}
    ]


def test_init_invalid_dimensions():
    """
    SSD1322 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1322, serial, 128, 77)


def test_hide():
    """
    SSD1322 OLED screen content can be hidden.
    """
    device = ssd1322(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1322 OLED screen content can be displayed.
    """
    device = ssd1322(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_greyscale_display():
    """
    SSD1322 OLED screen can draw and display a greyscale image.
    """
    device = ssd1322(serial, mode="RGB")
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
        {'command': [21]}, {'data': [28, 91]},
        {'command': [117]}, {'data': [0, 63]},
        {'command': [92]}, {'data': get_json_data('demo_ssd1322_greyscale')}
    ]


def test_monochrome_display():
    """
    SSD1322 OLED screen can draw and display a monochrome image.
    """
    device = ssd1322(serial, mode="1")
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
        {'command': [21]}, {'data': [28, 91]},
        {'command': [117]}, {'data': [0, 63]},
        {'command': [92]}, {'data': get_json_data('demo_ssd1322_monochrome')}
    ]
