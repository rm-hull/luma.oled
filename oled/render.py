# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

from PIL import Image, ImageDraw


class canvas(object):
    """
    A canvas returns a properly-sized :py:mod:`PIL.ImageDraw` object onto
    which the caller can draw upon. As soon as the with-block completes, the
    resultant image is flushed onto the device.
    """
    def __init__(self, device):
        self.draw = None
        self.image = Image.new(device.mode, device.size)
        self.device = device

    def __enter__(self):
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def __exit__(self, type, value, traceback):
        if type is None:
            # do the drawing onto the device
            self.device.display(self.image)

        del self.draw   # Tidy up the resources
        return False    # Never suppress exceptions
