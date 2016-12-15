#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

import hashlib
import os.path
from tempfile import NamedTemporaryFile

from oled.emulator import capture, gifanim
from oled.render import canvas

import baseline_data


def md5(fname):
    with open(fname, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()


def test_capture_noops():
    fname = NamedTemporaryFile(suffix=".png").name
    device = capture(file_template=fname, transform="none")
    # All these should have no effect
    device.hide()
    device.show()
    device.command(1, 2, 4, 4)
    device.data([1, 2, 4, 4])


def test_capture_display():
    reference = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference',
        'capture.png'))

    fname = NamedTemporaryFile(suffix=".png").name
    device = capture(file_template=fname, transform="none")

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    assert md5(reference) == md5(fname)


def test_gifanim_write():
    reference = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference',
        'anim.gif'))

    fname = NamedTemporaryFile(suffix=".gif").name
    device = gifanim(filename=fname)

    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    with canvas(device) as draw:
        draw.text((30, 10), text="Blipvert", fill="white")

    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    device.write_animation()
    assert md5(reference) == md5(fname)
