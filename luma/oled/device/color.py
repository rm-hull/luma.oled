# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Base class for SSD13xx color devices

.. versionadded:: 3.0.0
"""

from luma.core.device import device
import luma.core.error
import luma.core.framebuffer
import luma.oled.const


class color_device(device):
    def __init__(self, serial_interface, width, height, rotate, framebuffer, **kwargs):
        super(color_device, self).__init__(luma.oled.const.common, serial_interface)
        self.capabilities(width, height, rotate, mode="RGB")
        self.framebuffer = getattr(luma.core.framebuffer, framebuffer)(self)

        if (width, height) not in self._supported_dimensions():
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self._init_sequence()
        self.contrast(0xFF)
        self.clear()
        self.show()

    def _supported_dimensions(self):
        raise NotImplementedError()

    def _init_sequence(self):
        raise NotImplementedError()

    def _set_position(self, top, right, bottom, left):
        raise NotImplementedError()

    def _apply_offsets(self, bbox):
        return bbox

    def display(self, image):
        """
        Renders a 24-bit RGB image to the Color OLED display.

        :param image: the image to render.
        :type image: PIL.Image.Image
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        if self.framebuffer.redraw_required(image):
            left, top, right, bottom = self._apply_offsets(self.framebuffer.bounding_box)
            width = right - left
            height = bottom - top

            self._set_position(top, right, bottom, left)

            i = 0
            buf = bytearray(width * height * 2)
            for r, g, b in self.framebuffer.getdata():
                if not(r == g == b == 0):
                    # 65K format 1
                    buf[i] = r & 0xF8 | g >> 5
                    buf[i + 1] = g << 5 & 0xE0 | b >> 3
                i += 2

            self.data(list(buf))
