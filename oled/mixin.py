# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

from PIL import Image


class capabilities(object):
    def capabilities(self, width, height, mode="1"):
        assert mode in ("1", "RGB", "RGBA")
        self.width = width
        self.height = height
        self.size = (width, height)
        self.mode = mode
        self.bounding_box = (0, 0, self.width - 1, self.height - 1)

    def clear(self):
        """
        Initializes the device memory with an empty (blank) image.
        """
        self.display(Image.new(self.mode, self.size))

    def display(self, image):
        raise NotImplementedError()
