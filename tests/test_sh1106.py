#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import sh1106
from luma.core.render import canvas

import baseline_data
from helpers import (serial, call, Mock, setup_function,  # noqa: F401
    assert_invalid_dimensions)


def test_init_128x64():
    """
    SH1106 OLED with a 128 x 64 resolution works correctly.
    """
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
    """
    SH1106 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(sh1106, serial, 77, 105)


def test_display():
    """
    SH1106 OLED screen can draw and display an image.
    """
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
