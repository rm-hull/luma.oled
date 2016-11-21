#!/usr/bin/env python

from oled.device import sh1106
from oled.render import canvas

import mock
import baseline_data

port = 1
bus = mock.smbus(port)
addr = 0x3C


def teardown_function(function):
    bus.reset()


def test_display():
    device = sh1106(bus)
    bus.reset()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    assert len(bus.recordings) == 40

    for i in range(40):
        assert bus.recordings[i] == baseline_data.demo_sh1106[i]
