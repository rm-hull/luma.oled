#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ch1115
from luma.core.render import canvas

from baseline_data import get_reference_data, primitives
from helpers import serial, assert_invalid_dimensions, setup_function  # noqa: F401
from unittest.mock import Mock, call


def test_init_128x64():
    """
    CH1115 OLED with a 128 x 64 resolution works correctly.
    """
    ch1115(serial)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 213, 128, 168, 63, 211, 0, 64, 173, 139, 161, 200, 218, 18, 129, 127, 217, 34, 219, 32, 164, 166),
        # clear display
        call(176, 2, 16),
        call(177, 2, 16),
        call(178, 2, 16),
        call(179, 2, 16),
        call(180, 2, 16),
        call(181, 2, 16),
        call(182, 2, 16),
        call(183, 2, 16),
        # show display
        call(175),
        # display on
        call(175)
    ])

    # Next 1024 are all data: zero's to clear the RAM
    # (1024 = 128 * 64 / 8)
    serial.data.assert_has_calls([call(bytearray([0] * 128))] * 8)


def test_init_invalid_dimensions():
    """
    CH1115 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ch1115, serial, 128, 32)


def test_display():
    """
    CH1115 OLED screen can draw and display an image.
    """
    device = ch1115(serial)
    serial.reset_mock()

    recordings = []

    def data(data):
        recordings.append({'data': list(data)})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command = Mock(side_effect=command, unsafe=True)
    serial.data = Mock(side_effect=data, unsafe=True)

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        primitives(device, draw)

    serial.data.assert_called()
    serial.command.assert_called()

    # To regenerate test data, uncomment the following (remember not to commit though)
    # ================================================================================
    # from baseline_data import save_reference_data
    # save_reference_data("demo_ch1115", recordings)

    assert recordings == get_reference_data('demo_ch1115')
