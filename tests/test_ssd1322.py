#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import pytest
import luma.core.error
from luma.oled.device import ssd1322
from luma.core.render import canvas
import baseline_data

serial = Mock(unsafe=True)


def setup_function(function):
    serial.reset_mock()
    serial.command.side_effect = None


def test_init_256x64():
    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command.side_effect = command
    serial.data.side_effect = data

    ssd1322(serial)

    serial.data.assert_called()
    serial.command.assert_called()

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
        {'command': [117]}, {'data': [0, 127]},
        {'command': [92]}, {'data': [0] * (256 * 64 // 2)},
        {'command': [175]}
    ]


def test_init_invalid_dimensions():
    with pytest.raises(luma.core.error.DeviceDisplayModeError) as ex:
        ssd1322(serial, width=128, height=77)
    assert "Unsupported display mode: 128 x 77" in str(ex.value)


def test_hide():
    device = ssd1322(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(174)


def test_show():
    device = ssd1322(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(175)


def test_display():
    device = ssd1322(serial)
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
        baseline_data.primitives(device, draw)

    serial.data.assert_called()
    serial.command.assert_called()

    assert recordings == [
        {'command': [21]}, {'data': [28, 91]},
        {'command': [117]}, {'data': [0, 127]},
        {'command': [92]}, {'data': baseline_data.demo_ssd1322}
    ]
