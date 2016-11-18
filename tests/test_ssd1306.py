#!/usr/bin/env python

from oled.device import ssd1306
from oled.render import canvas

import mock
import baseline_data

port = 1
bus = mock.smbus(port)
addr = 0x3C


def teardown_function(function):
    bus.reset()


def test_init():
    ssd1306(bus)
    assert len(bus.recordings) == 35
    # Bursts 0/1 are initialization commands
    cmds = [174, 213, 128, 168, 63, 211, 0, 64, 141, 20, 32, 0,
            160, 200, 218, 18, 129, 207, 217, 241, 219, 64, 164,
            166, 33, 0, 127, 34, 0, 7]
    assert bus.recordings[0].mode == 0
    assert bus.recordings[1].mode == 0
    assert bus.recordings[0].data + bus.recordings[1].data == cmds

    # Next 32 bursts are all data: zero's to clear the RAM
    # (32 * 32 = 1024 = 128 * 64 / 8)
    for i in range(32):
        assert bus.recordings[i + 2] == mock.recording(60, 64, [0] * 32)

    # Last burst is a command to show the screen
    assert bus.recordings[34] == mock.recording(60, 0, [175])


def test_hide():
    device = ssd1306(bus)
    bus.reset()
    device.hide()
    assert len(bus.recordings) == 1
    assert bus.recordings[0] == mock.recording(60, 0, [174])


def test_show():
    device = ssd1306(bus)
    bus.reset()
    device.show()
    assert len(bus.recordings) == 1
    assert bus.recordings[0] == mock.recording(60, 0, [175])


def test_diplay():
    device = ssd1306(bus)
    bus.reset()

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    assert len(bus.recordings) == 33

    # Initial command to reset the display
    assert bus.recordings[0] == mock.recording(60, 0, [33, 0, 127, 34, 0, 7])

    # Next 32 recordings are data representing the drawn image
    for i in range(32):
        assert bus.recordings[i + 1] == baseline_data.demo_ssd1306[i]
