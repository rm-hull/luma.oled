# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Base class for SSD13xx greyscale devices
"""

from luma.core.device import device
import luma.core.error
import luma.core.framebuffer
import luma.oled.const


class greyscale_device(device):
    def __init__(self, const, serial_interface, width, height, rotate, mode, framebuffer, nibble_order, **kwargs):
        super(greyscale_device, self).__init__(const, serial_interface)
        self.capabilities(width, height, rotate, mode)
        self.framebuffer = getattr(luma.core.framebuffer, framebuffer)(self)
        self._populate = self._render_mono if mode == "1" else self._render_greyscale
        self._nibble_order = nibble_order

        if (width, height) not in self._supported_dimensions():
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self._init_sequence()
        self.contrast(0x7F)
        self.clear()
        self.show()

    def _check_dimensions(self):
        raise NotImplementedError()

    def _init_sequence(self):
        raise NotImplementedError()

    def _set_position(self, top, right, bottom, left):
        raise NotImplementedError()

    def _render_mono(self, buf, pixel_data):
        i = 0
        for pix in pixel_data:
            if pix > 0:
                if i % 2 == self._nibble_order:
                    buf[i // 2] |= 0xF0
                else:
                    buf[i // 2] |= 0x0F

            i += 1

    def _render_greyscale(self, buf, pixel_data):
        i = 0
        for r, g, b in pixel_data:
            # RGB->Greyscale luma calculation into 4-bits
            grey = (r * 306 + g * 601 + b * 117) >> 14

            if grey > 0:
                if i % 2 == self._nibble_order:
                    buf[i // 2] |= (grey << 4)
                else:
                    buf[i // 2] |= grey

            i += 1

    def display(self, image):
        """
        Takes a 1-bit monochrome or 24-bit RGB image and renders it
        to the SSD1322 OLED display. RGB pixels are converted to 4-bit
        greyscale values using a simplified Luma calculation, based on
        *Y'=0.299R'+0.587G'+0.114B'*.

        :param image: the image to render
        :type image: PIL.Image.Image
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        if self.framebuffer.redraw_required(image):
            left, top, right, bottom = self.framebuffer.inflate_bbox()
            width = right - left
            height = bottom - top

            buf = bytearray(width * height >> 1)
            self._set_position(top, right, bottom, left)
            self._populate(buf, self.framebuffer.getdata())
            self.data(list(buf))
