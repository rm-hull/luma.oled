#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Collection of datasets to prevent regression bugs from creeping in.
"""

import json
from pathlib import Path


def primitives(device, draw):
    padding = 2
    shape_width = 20
    top = padding
    bottom = device.height - padding - 1
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    x = padding
    draw.ellipse((x, top, x + shape_width, bottom), outline="red", fill="black")
    x += shape_width + padding
    draw.rectangle((x, top, x + shape_width, bottom), outline="blue", fill="black")
    x += shape_width + padding
    draw.polygon([(x, bottom), (x + shape_width / 2, top), (x + shape_width, bottom)], outline="green", fill="black")
    x += shape_width + padding
    draw.line((x, bottom, x + shape_width, top), fill="yellow")
    draw.line((x, top, x + shape_width, bottom), fill="yellow")
    x += shape_width + padding
    draw.text((x, top), 'Hello', fill="cyan")
    draw.text((x, top + 20), 'World!', fill="purple")


def get_reference_data(fname):
    """
    Load JSON reference data.

    :param fname: Filename without extension.
    :type fname: str
    """
    base_dir = Path(__file__).resolve().parent
    fpath = base_dir.joinpath('reference', 'data', fname + '.json')
    with fpath.open() as f:
        return json.load(f)


def save_reference_data(fname, recordings):
    base_dir = Path(__file__).resolve().parent
    fpath = base_dir.joinpath('reference', 'data', fname + '.json')
    with fpath.open("w") as f:
        json.dump(recordings, f)
        raise AssertionError("Regenerating reference data ... do not commit with this active in tests!")
