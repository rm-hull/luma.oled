#!/usr/bin/env python

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from oled.device import sh1106
from oled.render import canvas

import baseline_data

serial = Mock()


def test_display():
    device = sh1106(serial)
    serial.reset_mock()

    recordings = []

    def data(data):
        recordings.append({'data': data})

    def command(*cmd):
        recordings.append({'command': list(cmd)})

    serial.command = Mock(side_effect=command)
    serial.data = Mock(side_effect=data)

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    serial.data.assert_called()
    serial.command.assert_called()

    print(recordings)
    assert recordings == baseline_data.demo_sh1106
