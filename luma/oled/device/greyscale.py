# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Base class for SSD13xx greyscale devices

.. versionadded:: 3.0.0
"""

from abc import abstractmethod, ABCMeta

from luma.core.device import device
import luma.core.error
import luma.core.framebuffer
import luma.oled.const


class greyscale_device(device):
    __metaclass__ = ABCMeta

    def __init__(self, const, serial_interface, width, height, rotate, mode,
                 framebuffer, nibble_order, **kwargs):
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

    @abstractmethod
    def _supported_dimensions(self):
        """
        Enumerates the screen resolutions that the specific device supports, as
        a list of tuples; e.g.: ``[(96, 64), (96, 32), (96, 16)]``
        """
        pass  # pragma: no cover

    @abstractmethod
    def _init_sequence(self):
        """
        Concrete implementations should call the initiation sequence for the
        specific device. Invoked from the constructor, but no assumptions should
        be made about what has been initialized so far. No return value is
        expected.
        """
        pass  # pragma: no cover

    @abstractmethod
    def _set_position(self, top, right, bottom, left):
        """
        Invoked once as part of the devices display refresh. The four coordinates
        form a bounding box that determines the area of the screen that will get
        get redrawn; thus the concrete implementations should send the correct
        command sequence to the device to set that bounding box. No return value
        is expected.
        """
        pass  # pragma: no cover

    def _render_mono(self, buf, pixel_data):
        i = 0
        nibble_order = self._nibble_order
        for pix in pixel_data:
            if pix > 0:
                if i % 2 == nibble_order:
                    buf[i // 2] |= 0xF0
                else:
                    buf[i // 2] |= 0x0F

            i += 1

    def _render_greyscale(self, buf, pixel_data):
        i = 0
        nibble_order = self._nibble_order
        for r, g, b in pixel_data:
            # RGB->Greyscale luma calculation into 4-bits
            grey = (r * 306 + g * 601 + b * 117) >> 14

            if grey > 0:
                if i % 2 == nibble_order:
                    buf[i // 2] |= (grey << 4)
                else:
                    buf[i // 2] |= grey

            i += 1

    def display(self, image):
        """
        Takes a 1-bit monochrome or 24-bit RGB image and renders it
        to the greyscale OLED display. RGB pixels are converted to 4-bit
        greyscale values using a simplified Luma calculation, based on
        *Y'=0.299R'+0.587G'+0.114B'*.

        :param image: The image to render.
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
