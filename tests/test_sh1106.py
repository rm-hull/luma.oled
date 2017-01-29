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
from luma.oled.device import sh1106
from luma.core.render import canvas

import baseline_data

serial = Mock(unsafe=True)


def setup_function(function):
    serial.reset_mock()
    serial.command.side_effect = None


def test_init_128x64():
    sh1106(serial)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 32, 16, 176, 200, 0, 16, 64, 161, 166, 168, 63, 164,
             211, 0, 213, 240, 217, 34, 218, 18, 219, 32, 141, 20),
        # set contrast
        call(129, 127),
        # reset the display
        call(176, 2, 16),
        call(177, 2, 16),
        call(178, 2, 16),
        call(179, 2, 16),
        call(180, 2, 16),
        call(181, 2, 16),
        call(182, 2, 16),
        call(183, 2, 16)
    ])

    # Next 1024 are all data: zero's to clear the RAM
    # (1024 = 128 * 64 / 8)
    serial.data.assert_has_calls([call([0] * 128)] * 8)


def test_init_invalid_dimensions():
    with pytest.raises(luma.core.error.DeviceDisplayModeError) as ex:
        sh1106(serial, width=77, height=105)
    assert "Unsupported display mode: 77 x 105" in str(ex.value)


def test_display():
    device = sh1106(serial)
    serial.reset_mock()

    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command = Mock(side_effect=command, unsafe=True)
    serial.data = Mock(side_effect=data, unsafe=True)

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    serial.data.assert_called()
    serial.command.assert_called()

    assert recordings == baseline_data.demo_sh1106
