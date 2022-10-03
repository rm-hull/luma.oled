# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Base class for SSD13xx color devices

.. versionadded:: 3.0.0
"""

from abc import abstractmethod, ABCMeta

from luma.core.device import device
import luma.core.error
import luma.core.framebuffer
import luma.oled.const
from luma.oled.device.framebuffer_mixin import __framebuffer_mixin


class color_device(device, __framebuffer_mixin):
    __metaclass__ = ABCMeta

    def __init__(self, serial_interface, width, height, rotate, framebuffer, **kwargs):
        super(color_device, self).__init__(luma.oled.const.common, serial_interface)
        self.capabilities(width, height, rotate, mode="RGB")
        self.init_framebuffer(framebuffer)

        if (width, height) not in self._supported_dimensions():
            raise luma.core.error.DeviceDisplayModeError(
                f"Unsupported display mode: {width} x {height}")

        self._init_sequence()
        self.contrast(0xFF)
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

    def _apply_offsets(self, bbox):
        return bbox

    def display(self, image):
        """
        Renders a 24-bit RGB image to the Color OLED display.

        :param image: The image to render.
        :type image: PIL.Image.Image
        """
        assert image.mode == self.mode
        assert image.size == self.size

        image = self.preprocess(image)

        for image, bounding_box in self.framebuffer.redraw(image):
            left, top, right, bottom = self._apply_offsets(bounding_box)
            width = right - left
            height = bottom - top

            self._set_position(top, right, bottom, left)

            i = 0
            buf = bytearray(width * height * 2)
            for r, g, b in image.getdata():
                if not r == g == b == 0:
                    # 65K format 1
                    buf[i] = r & 0xF8 | g >> 5
                    buf[i + 1] = g << 3 & 0xE0 | b >> 3
                i += 2

            self.data(list(buf))
