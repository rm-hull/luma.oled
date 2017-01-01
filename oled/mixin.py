# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

from PIL import Image


class capabilities(object):
    def capabilities(self, width, height, rotate, mode="1"):
        assert mode in ("1", "RGB", "RGBA")
        assert rotate in (0, 1, 2, 3)
        self._w = width
        self._h = height
        self.width = width if rotate % 2 == 0 else height
        self.height = height if rotate % 2 == 0 else width
        self.size = (self.width, self.height)
        self.bounding_box = (0, 0, self.width - 1, self.height - 1)
        self.rotate = rotate
        self.mode = mode

    def clear(self):
        """
        Initializes the device memory with an empty (blank) image.
        """
        self.display(Image.new(self.mode, self.size))

    def preprocess(self, image):
        if self.rotate == 0:
            return image

        angle = self.rotate * -90
        return image.rotate(angle, expand=True).crop((0, 0, self._w, self._h))

    def display(self, image):
        raise NotImplementedError()
