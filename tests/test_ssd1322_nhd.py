#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1322_nhd
from luma.core.render import canvas

from baseline_data import get_json_data, primitives
from helpers import serial, setup_function, assert_invalid_dimensions  # noqa: F401


def test_init_128x64():
    """
    SSD1322_NHD OLED with a 128 x 64 resolution works correctly.
    """
    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command.side_effect = command
    serial.data.side_effect = data

    ssd1322_nhd(serial)

    assert serial.data.called
    assert serial.command.called

    assert recordings == [
        {'command': [253]}, {'data': [18]},
        {'command': [174]},
        {'command': [179]}, {'data': [145]},
        {'command': [202]}, {'data': [63]},
        {'command': [162]}, {'data': [0]},
        {'command': [171]}, {'data': [1]},
        {'command': [160]}, {'data': [22, 17]},
        {'command': [199]}, {'data': [15]},
        {'command': [193]}, {'data': [159]},
        {'command': [177]}, {'data': [242]},
        {'command': [187]}, {'data': [31]},
        {'command': [180]}, {'data': [160, 253]},
        {'command': [190]}, {'data': [4]},
        {'command': [166]},
        {'command': [175]},
        {'command': [193]}, {'data': [127]},
        {'command': [21]}, {'data': [28, 91]},
        {'command': [117]}, {'data': [0, 63]},
        {'command': [92]}, {'data': [0] * (128 * 64)},
        {'command': [175]}
    ]


def test_hide():
    """
    SSD1322_NHD OLED screen content can be hidden.
    """
    device = ssd1322_nhd(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    """
    SSD1322_NHD OLED screen content can be displayed.
    """
    device = ssd1322_nhd(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_greyscale_display():
    """
    SSD1322_NHD OLED screen can draw and display a greyscale image.
    """
    device = ssd1322_nhd(serial, mode="RGB")
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
        {'command': [92]}, {'data': get_json_data('demo_ssd1322_nhd_greyscale')}
    ]


def test_monochrome_display():
    """
    SSD1322_NHD OLED screen can draw and display a monochrome image.
    """
    device = ssd1322_nhd(serial, mode="1")
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
        {'command': [92]}, {'data': get_json_data('demo_ssd1322_nhd_monochrome')}
    ]
