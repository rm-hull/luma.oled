#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import sh1107
from luma.core.render import canvas

from baseline_data import get_reference_data, primitives
from helpers import serial, assert_invalid_dimensions, setup_function  # noqa: F401
from unittest.mock import Mock, call


def test_init_64x128():
    """
    SH1107 OLED with a 64 x 128 resolution works correctly.
    """
    sh1107(serial)
    serial.command.assert_has_calls([
        # Initial burst are initialization commands
        call(174, 32, 166, 168, 127, 164, 211, 96, 213, 128, 217, 34, 218, 18, 219, 53),
        # set contrast
        call(129, 127),
        # reset the display
        call(16, 0, 176),
        call(16, 0, 177),
        call(16, 0, 178),
        call(16, 0, 179),
        call(16, 0, 180),
        call(16, 0, 181),
        call(16, 0, 182),
        call(16, 0, 183),
        call(16, 0, 184),
        call(16, 0, 185),
        call(16, 0, 186),
        call(16, 0, 187),
        call(16, 0, 188),
        call(16, 0, 189),
        call(16, 0, 190),
        call(16, 0, 191),
        call(175)])

    # Next 1024 are all data: zero's to clear the RAM
    # (1024 = 128 * 64 / 8)
    serial.data.assert_has_calls([call([0] * 64)] * 16)


def test_init_invalid_dimensions():
    """
    SH1107 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(sh1107, serial, 77, 105)


def test_display():
    """
    SH1107 OLED screen can draw and display an image.
    """
    device = sh1107(serial)
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
        primitives(device, draw)

    serial.data.assert_called()
    serial.command.assert_called()

    # To regenerate test data, uncomment the following (remember not to commit though)
    # ================================================================================
    # from baseline_data import save_reference_data
    # save_reference_data("demo_sh1107", recordings)

    assert recordings == get_reference_data('demo_sh1107')
