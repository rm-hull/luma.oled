#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.


import pytest

from oled.render import canvas
from oled.virtual import history
from oled.emulator import dummy

import baseline_data


def test_restore_throws_error_when_empty():
    device = dummy()
    hist = history(device)
    assert len(hist) == 0
    with pytest.raises(IndexError):
        hist.restore()


def test_save_and_restore_reverts_image():
    device = dummy()
    hist = history(device)

    with canvas(hist) as draw:
        baseline_data.primitives(hist, draw)

    img1 = device.image
    hist.savepoint()
    assert len(hist) == 1

    with canvas(hist) as draw:
        draw.text((10, 10), text="Hello", fill="white")

    img2 = device.image
    assert img1 != img2
    hist.restore()
    img3 = device.image
    assert img1 == img3
    assert len(hist) == 0


def test_drop_and_restore():
    device = dummy()
    hist = history(device)

    copies = []
    for i in range(10):
        with canvas(hist) as draw:
            draw.text((10, 10), text="Hello {0}".format(i), fill="white")
        hist.savepoint()
        copies.append(device.image)

    hist.restore()
    assert device.image == copies[9]
    hist.restore(drop=2)
    assert device.image == copies[6]
    hist.restore(drop=4)
    assert device.image == copies[1]
    assert len(hist) == 1
