# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

from PIL import Image, ImageChops


class full_frame(object):

    def __init__(self, device):
        self.bbox = [0, 0, device.width, device.height]

    def calc(self, image):
        self.image = image

    def getdata(self):
        return self.image.getdata()


class diff_to_previous(object):

    def __init__(self, device):
        self._prev = Image.new(device.mode, device.size, "white")

    def calc(self, image):
        self.bbox = ImageChops.difference(self._prev, image).getbbox()
        if self.bbox is not None:
            self._prev = image.copy()

    def getdata(self):
        return self._prev.crop(self.bbox).getdata()
