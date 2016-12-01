#!/usr/bin/env python

import hashlib
import os.path
from tempfile import NamedTemporaryFile

from oled.device import capture
from oled.render import canvas

import baseline_data


def md5(fname):
    with open(fname, 'rb') as fp:
        hashlib.md5(fp.read()).hexdigest()


def test_noops():
    device = capture()
    # All these should have no effect
    device.hide()
    device.show()
    device.command(1, 2, 4, 4)
    device.data([1, 2, 4, 4])


def test_display():
    reference = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference.png'))

    fname = NamedTemporaryFile(suffix=".png").name
    device = capture(file_template=fname)

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    assert md5(reference) == md5(fname)
