# -*- coding: utf-8 -*-
# Copyright (c) 2014-2023 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Collection of serial interfaces to OLED devices.
"""

# Example usage:
#
#   from luma.core.interface.serial import i2c
#   from luma.core.render import canvas
#   from luma.oled.device import ssd1306
#   from PIL import ImageDraw
#
#   serial = i2c(port=1, address=0x3C)
#   device = ssd1306(serial)
#
#   with canvas(device) as draw:
#      draw.rectangle(device.bounding_box, outline="white", fill="black")
#      draw.text(30, 40, "Hello World", fill="white")
#
# As soon as the with-block scope level is complete, the graphics primitives
# will be flushed to the device.
#
# Creating a new canvas is effectively 'carte blanche': If you want to retain
# an existing canvas, then make a reference like:
#
#    c = canvas(device)
#    for X in ...:
#        with c as draw:
#            draw.rectangle(...)
#
# As before, as soon as the with block completes, the canvas buffer is flushed
# to the device.

from time import sleep
from luma.core.device import device, parallel_device
from luma.core.virtual import character
from luma.oled.device.color import color_device
from luma.oled.device.greyscale import greyscale_device
import luma.core.error
from luma.core.framebuffer import full_frame
from luma.core.bitmap_font import embedded_fonts
import luma.oled.const
from luma.oled.device.framebuffer_mixin import __framebuffer_mixin

__all__ = [
    "ssd1306", "ssd1309", "ssd1322", "ssd1362", "ssd1322_nhd", "ssd1325",
    "ssd1327", "ssd1331", "ssd1351", "sh1106", "sh1107", "ws0010",
    "winstar_weh"
]


class sh1106(device):
    """
    Serial interface to a monochrome SH1106 OLED display.

    On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.
    """

    def __init__(self, serial_interface=None, width=128, height=64, rotate=0, **kwargs):
        super(sh1106, self).__init__(luma.oled.const.sh1106, serial_interface)
        self.capabilities(width, height, rotate)
        self._pages = self._h // 8

        settings = {
            (128, 128): dict(multiplex=0xFF, displayoffset=0x02),
            (128, 64): dict(multiplex=0x3F, displayoffset=0x00),
            (128, 32): dict(multiplex=0x20, displayoffset=0x0F)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError(
                f"Unsupported display mode: {width} x {height}")

        self.command(
            self._const.DISPLAYOFF,
            self._const.MEMORYMODE,
            self._const.SETHIGHCOLUMN,      0xB0, 0xC8,
            self._const.SETLOWCOLUMN,       0x10, 0x40,
            self._const.SETSEGMENTREMAP,
            self._const.NORMALDISPLAY,
            self._const.SETMULTIPLEX,       settings['multiplex'],
            self._const.DISPLAYALLON_RESUME,
            self._const.SETDISPLAYOFFSET,   settings['displayoffset'],
            self._const.SETDISPLAYCLOCKDIV, 0xF0,
            self._const.SETPRECHARGE,       0x22,
            self._const.SETCOMPINS,         0x12,
            self._const.SETVCOMDETECT,      0x20,
            self._const.CHARGEPUMP,         0x14)

        self.contrast(0x7F)
        self.clear()
        self.show()

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the SH1106
        OLED display.

        :param image: Image to display.
        :type image: :py:mod:`PIL.Image`
        """
        assert image.mode == self.mode
        assert image.size == self.size

        image = self.preprocess(image)

        set_page_address = 0xB0
        image_data = image.getdata()
        pixels_per_page = self.width * 8
        buf = bytearray(self.width)

        for y in range(0, int(self._pages * pixels_per_page), pixels_per_page):
            self.command(set_page_address, 0x02, 0x10)
            set_page_address += 1
            offsets = [y + self.width * i for i in range(8)]

            for x in range(self.width):
                buf[x] = \
                    (image_data[x + offsets[0]] and 0x01) | \
                    (image_data[x + offsets[1]] and 0x02) | \
                    (image_data[x + offsets[2]] and 0x04) | \
                    (image_data[x + offsets[3]] and 0x08) | \
                    (image_data[x + offsets[4]] and 0x10) | \
                    (image_data[x + offsets[5]] and 0x20) | \
                    (image_data[x + offsets[6]] and 0x40) | \
                    (image_data[x + offsets[7]] and 0x80)

            self.data(list(buf))


class sh1107(device):
    """
    Serial interface to a monochrome SH1107 OLED display.

    On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.i2c` instance) to delegate sending
        data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 64).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 128).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int

    .. versionadded:: 3.11.0
    """

    def __init__(self, serial_interface=None, width=64, height=128, rotate=0, **kwargs):
        super(sh1107, self).__init__(luma.oled.const.sh1107, serial_interface)
        self.capabilities(width, height, rotate)

        self._pages = self._h // 8
        self._pagelen = self._w

        settings = {
            (64, 128): dict(multiplex=0x7F, displayoffset=0x60),
            (80, 128): dict(multiplex=0x4F, displayoffset=0x68),
            (128, 128): dict(multiplex=0x7F, displayoffset=0x00)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError(
                f"Unsupported display mode: {width} x {height}")

        self.command(
            self._const.DISPLAYOFF,
            self._const.MEMORYMODE,
            self._const.NORMALDISPLAY,
            self._const.SETMULTIPLEX,       settings['multiplex'],
            self._const.DISPLAYALLON_RESUME,
            self._const.SETDISPLAYOFFSET,   settings['displayoffset'],
            self._const.SETDISPLAYCLOCKDIV, 0x80,
            self._const.SETPRECHARGE,       0x22,
            self._const.SETCOMPINS,         0x12,
            self._const.SETVCOMDETECT,      0x35,
        )

        self.contrast(0x7F)
        self.clear()
        self.show()

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the SH1107
        OLED display.

        :param image: Image to display.
        :type image: :py:mod:`PIL.Image`
        """
        assert image.mode == self.mode
        assert image.size == self.size

        image = self.preprocess(image)
        pixmap = image.load()
        buf = bytearray(self._pagelen)

        for page in range(self._pages):
            for x in range(self._pagelen):
                tmp = 0
                for y in range(8):
                    tmp |= (pixmap[x, y + 8 * page] & 1) << y
                buf[x] = tmp
            self.command(0x10, 0x00, 0xb0 | page)
            self.data(list(buf))


class ssd1306(device):
    """
    Serial interface to a monochrome SSD1306 OLED display.

    On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.i2c` instance) to delegate sending
        data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 128).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    """

    def __init__(self, serial_interface=None, width=128, height=64, rotate=0, **kwargs):
        super(ssd1306, self).__init__(luma.oled.const.ssd1306, serial_interface)
        self.capabilities(width, height, rotate)

        # Supported modes
        settings = {
            (128, 64): dict(multiplex=0x3F, displayclockdiv=0x80, compins=0x12, colstart=0),
            (128, 32): dict(multiplex=0x1F, displayclockdiv=0x80, compins=0x02, colstart=0),
            (96, 16): dict(multiplex=0x0F, displayclockdiv=0x60, compins=0x02, colstart=0),
            (64, 48): dict(multiplex=0x2F, displayclockdiv=0x80, compins=0x12, colstart=32),
            (64, 32): dict(multiplex=0x1F, displayclockdiv=0x80, compins=0x12, colstart=32)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError(
                f"Unsupported display mode: {width} x {height}")

        self._pages = height // 8
        self._mask = [1 << (i // width) % 8 for i in range(width * height)]
        self._offsets = [(width * (i // (width * 8))) + (i % width) for i in range(width * height)]
        self._colstart = settings['colstart']
        self._colend = self._colstart + self._w

        self.command(
            self._const.DISPLAYOFF,
            self._const.SETDISPLAYCLOCKDIV, settings['displayclockdiv'],
            self._const.SETMULTIPLEX,       settings['multiplex'],
            self._const.SETDISPLAYOFFSET,   0x00,
            self._const.SETSTARTLINE,
            self._const.CHARGEPUMP,         0x14,
            self._const.MEMORYMODE,         0x00,
            self._const.SETSEGMENTREMAP,
            self._const.COMSCANDEC,
            self._const.SETCOMPINS,         settings['compins'],
            self._const.SETPRECHARGE,       0xF1,
            self._const.SETVCOMDETECT,      0x40,
            self._const.DISPLAYALLON_RESUME,
            self._const.NORMALDISPLAY)

        self.contrast(0xCF)
        self.clear()
        self.show()

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the OLED
        display.

        :param image: Image to display.
        :type image: :py:mod:`PIL.Image`
        """
        assert image.mode == self.mode
        assert image.size == self.size

        image = self.preprocess(image)

        self.command(
            # Column start/end address
            self._const.COLUMNADDR, self._colstart, self._colend - 1,
            # Page start/end address
            self._const.PAGEADDR, 0x00, self._pages - 1)

        buf = bytearray(self._w * self._pages)
        off = self._offsets
        mask = self._mask

        idx = 0
        for pix in image.getdata():
            if pix > 0:
                buf[off[idx]] |= mask[idx]
            idx += 1

        self.data(list(buf))


class ssd1309(ssd1306):
    """
    Serial interface to a monochrome SSD1309 OLED display.

    On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.spi` instance) to delegate sending
        data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 128).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int

    .. versionadded:: 3.1.0
    """


class ssd1331(color_device):
    """
    Serial interface to a 16-bit color (5-6-5 RGB) SSD1331 OLED display.

    On creation, an initialization sequence is pumped to the display to
    properly configure it. Further control commands can then be called to
    affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.spi` instance) to delegate
        sending data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 96).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param framebuffer: Framebuffering strategy, currently instances of
        ``diff_to_previous`` or ``full_frame`` are only supported.
    :type framebuffer: str
    """

    def __init__(self, serial_interface=None, width=96, height=64, rotate=0,
                 framebuffer=None, **kwargs):
        super(ssd1331, self).__init__(serial_interface, width, height, rotate,
                                      framebuffer, **kwargs)

    def _supported_dimensions(self):
        return [(96, 64)]

    def _init_sequence(self):
        self.command(
            0xAE,        # Display off
            0xA0, 0x72,  # Seg remap
            0xA1, 0x00,  # Set Display start line
            0xA2, 0x00,  # Set display offset
            0xA4,        # Normal display
            0xA8, 0x3F,  # Set multiplex
            0xAD, 0x8E,  # Master configure
            0xB0, 0x0B,  # Power save mode
            0xB1, 0x74,  # Phase12 period
            0xB3, 0xD0,  # Clock divider
            0x8A, 0x80,  # Set precharge speed A
            0x8B, 0x80,  # Set precharge speed B
            0x8C, 0x80,  # Set precharge speed C
            0xBB, 0x3E,  # Set pre-charge voltage
            0xBE, 0x3E,  # Set voltage
            0x87, 0x0F)  # Master current control

    def _set_position(self, top, right, bottom, left):
        self.command(
            0x15, left, right - 1,    # Set column addr
            0x75, top, bottom - 1)    # Set row addr

    def contrast(self, level):
        """
        Switches the display contrast to the desired level, in the range
        0-255. Note that setting the level to a low (or zero) value will
        not necessarily dim the display to nearly off. In other words,
        this method is **NOT** suitable for fade-in/out animation.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert 0 <= level <= 255
        self.command(0x81, level,  # Set contrast A
                     0x82, level,  # Set contrast B
                     0x83, level)  # Set contrast C


class ssd1351(color_device):
    """
    Serial interface to the 16-bit color (5-6-5 RGB) SSD1351 OLED display.

    On creation, an initialization sequence is pumped to
    the display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.spi` instance) to delegate
        sending data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 128).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 128).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param framebuffer: Framebuffering strategy, currently instances of
        ``diff_to_previous`` or ``full_frame`` are only supported.
    :type framebuffer: str
    :param bgr: Set to ``True`` if device pixels are BGR order (rather than RGB).
    :type bgr: bool
    :param h_offset: Horizontal offset (in pixels) of screen to device memory
        (default: 0)
    :type h_offset: int
    :param v_offset: Vertical offset (in pixels) of screen to device memory
        (default: 0)
    :type h_offset: int

    .. versionadded:: 2.3.0
    """

    def __init__(self, serial_interface=None, width=128, height=128, rotate=0,
                 framebuffer=None, h_offset=0, v_offset=0,
                 bgr=False, **kwargs):

        # RGB or BGR order
        self._color_order = 0x04 if bgr else 0x00

        if h_offset != 0 or v_offset != 0:
            def offset(bbox):
                left, top, right, bottom = bbox
                return (left + h_offset, top + v_offset, right + h_offset, bottom + v_offset)
            self._apply_offsets = offset

        super(ssd1351, self).__init__(serial_interface, width, height, rotate, framebuffer, **kwargs)

    def _supported_dimensions(self):
        return [(96, 96), (128, 128), (128, 96)]

    def _init_sequence(self):
        self.command(0xFD, 0x12)               # Unlock IC MCU interface
        self.command(0xFD, 0xB1)               # Command A2,B1,B3,BB,BE,C1 accessible if in unlock state
        self.command(0xAE)                     # Display off
        self.command(0xB3, 0xF1)               # Clock divider
        self.command(0xCA, 0x7F)               # Mux ratio
        self.command(0x15, 0x00, self.width - 1)    # Set column address
        self.command(0x75, 0x00, self.height - 1)   # Set row address
        self.command(0xA0, 0x70 | self._color_order)  # Segment remapping
        self.command(0xA1, 0x00)               # Set Display start line
        self.command(0xA2, 0x00)               # Set display offset
        self.command(0xB5, 0x00)               # Set GPIO
        self.command(0xAB, 0x01)               # Function select (internal - diode drop)
        self.command(0xB1, 0x32)               # Precharge
        self.command(0xB4, 0xA0, 0xB5, 0x55)   # Set segment low voltage
        self.command(0xBE, 0x05)               # Set VcomH voltage
        self.command(0xC7, 0x0F)               # Contrast master
        self.command(0xB6, 0x01)               # Precharge2
        self.command(0xA6)                     # Normal display

    def _set_position(self, top, right, bottom, left):
        self.command(0x15, left, right - 1)    # Set column addr
        self.command(0x75, top, bottom - 1)    # Set row addr
        self.command(0x5C)                     # Write RAM

    def contrast(self, level):
        """
        Switches the display contrast to the desired level, in the range
        0-255. Note that setting the level to a low (or zero) value will
        not necessarily dim the display to nearly off. In other words,
        this method is **NOT** suitable for fade-in/out animation.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert 0 <= level <= 255
        self.command(0xC1, level, level, level)

    def command(self, cmd, *args):
        """
        Sends a command and an (optional) sequence of arguments through to the
        delegated serial interface. Note that the arguments are passed through
        as data.
        """
        self._serial_interface.command(cmd)
        if len(args) > 0:
            self._serial_interface.data(list(args))


class ssd1322(greyscale_device):
    """
    Serial interface to a 4-bit greyscale SSD1322 OLED display.

    On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
       :py:class:`luma.core.interface.serial.spi` instance) to delegate sending
       data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 96).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param mode: Supplying "1" or "RGB" effects a different rendering
         mechanism, either to monochrome or 4-bit greyscale.
    :type mode: str
    :param framebuffer: Framebuffering strategy, currently instances of
        ``diff_to_previous`` or ``full_frame`` are only supported
    :type framebuffer: str

    """

    def __init__(self, serial_interface=None, width=256, height=64, rotate=0,
                 mode="RGB", framebuffer=None, **kwargs):
        self._column_offset = (480 - width) // 2
        super(ssd1322, self).__init__(luma.oled.const.ssd1322, serial_interface,
                                      width, height, rotate, mode, framebuffer,
                                      nibble_order=0, **kwargs)

    def _supported_dimensions(self):
        return [(256, 64), (256, 48), (256, 32),
                (128, 64), (128, 48), (128, 32),
                (64, 64),  (64, 48),  (64, 32)]

    def _init_sequence(self):
        self.command(0xFD, 0x12)        # Unlock IC
        self.command(0xA4)              # Display off (all pixels off)
        self.command(0xB3, 0xF2)        # Display divide clockratio/freq
        self.command(0xCA, 0x3F)        # Set MUX ratio
        self.command(0xA2, 0x00)        # Display offset
        self.command(0xA1, 0x00)        # Display start Line
        self.command(0xA0, 0x14, 0x11)  # Set remap & dual COM Line
        self.command(0xB5, 0x00)        # Set GPIO (disabled)
        self.command(0xAB, 0x01)        # Function select (internal Vdd)
        self.command(0xB4, 0xA0, 0xFD)  # Display enhancement A (External VSL)
        self.command(0xC7, 0x0F)        # Master contrast (reset)
        self.command(0xB9)              # Set default greyscale table
        self.command(0xB1, 0xF0)        # Phase length
        self.command(0xD1, 0x82, 0x20)  # Display enhancement B (reset)
        self.command(0xBB, 0x0D)        # Pre-charge voltage
        self.command(0xB6, 0x08)        # 2nd precharge period
        self.command(0xBE, 0x00)        # Set VcomH
        self.command(0xA6)              # Normal display (reset)
        self.command(0xA9)              # Exit partial display

    def _set_position(self, top, right, bottom, left):
        width = right - left
        pix_start = self._column_offset + left
        coladdr_start = pix_start >> 2
        coladdr_end = (pix_start + width >> 2) - 1

        self.command(0x15, coladdr_start, coladdr_end)  # set column addr
        self.command(0x75, top, bottom - 1)             # Reset row addr
        self.command(0x5C)                              # Enable MCU to write data into RAM

    def command(self, cmd, *args):
        """
        Sends a command and an (optional) sequence of arguments through to the
        delegated serial interface. Note that the arguments are passed through
        as data.
        """
        self._serial_interface.command(cmd)
        if len(args) > 0:
            self._serial_interface.data(list(args))


class ssd1362(greyscale_device):
    """
    Serial interface to a 4-bit greyscale SSD1362 OLED display.

    On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.

    :param serial_interface: The serial interface (usually a
       :py:class:`luma.core.interface.serial.spi` instance) to delegate sending
       data and commands through.
    :param width: The number of horizontal pixels (optional, defaults to 96).
    :type width: int
    :param height: The number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param mode: Supplying "1" or "RGB" effects a different rendering
         mechanism, either to monochrome or 4-bit greyscale.
    :type mode: str
    :param framebuffer: Framebuffering strategy, currently instances of
        ``diff_to_previous`` or ``full_frame`` are only supported
    :type framebuffer: str

    .. versionadded:: 3.4.0
    """

    def __init__(self, serial_interface=None, width=256, height=64, rotate=0,
                 mode="RGB", framebuffer=None, **kwargs):
        super(ssd1362, self).__init__(luma.oled.const.ssd1362, serial_interface,
                                      width, height, rotate, mode, framebuffer,
                                      nibble_order=1, **kwargs)

    def _supported_dimensions(self):
        return [(256, 64)]

    def _init_sequence(self):
        self.command(
            0xAB,              # Set Vdd Mode
            0x01,              # ELW2106AA VCI = 3.0V
            0xAD, 0x9E,        # Set IREF selection
            0x15, 0x00, 0x7F,  # Set column address
            0x75, 0x00, 0x3F,  # Set row address
            0xA0, 0x43,        # Set Re-map
            0xA1, 0x00,        # Set display start line
            0xA2, 0x00,        # Set display offset
            0xA4,              # Set display mode
            0xA8, 0x3F,        # Set multiplex ratio
            0xB1, 0x11,        # Set Phase1,2 length
            0xB3, 0xF0,        # Set display clock divide ratio
            0xB9,              # Grey scale table
            0xBC, 0x04,        # Set pre-charge voltage
            0xBE, 0x05)        # Set VCOMH deselect level, 0.82 * Vcc

    def _set_position(self, top, right, bottom, left):
        self.command(
            0x15, left >> 1, (right - 1) >> 1,  # set column addr
            0x75, top, bottom - 1)              # set row addr


class ssd1322_nhd(greyscale_device):
    """Similar to ssd1322 but several options are hard coded: width, height and
    frame buffer"""

    def __init__(self, serial_interface=None, width=128, height=64, rotate=0,
                 mode="RGB", framebuffer=full_frame(), **kwargs):
        super(ssd1322_nhd, self).__init__(luma.oled.const.ssd1322, serial_interface,
                                      128, 64, rotate, mode, framebuffer,
                                      nibble_order=0, **kwargs)

    def _supported_dimensions(self):
        return [(128, 64)]

    def _init_sequence(self):
        self.command(0xFD, 0x12)  # Unlock IC
        self.command(0xAE)  # Display off
        self.command(0xB3, 0x91)  # Display divide clockratio/freq
        self.command(0xCA, 0x3F)  # Set MUX ratio
        self.command(0xA2, 0x00)  # Display offset
        self.command(0xAB, 0x01)  # Internal VDD
        self.command(0xA0, 0x16, 0x11)  # Set remap & dual COM Line
        self.command(0xC7, 0x0F)  # Master contrast (reset)
        self.command(0xC1, 0x9F)  # Set contrast current
        self.command(0xB1, 0xF2)  # Phase 1 and 2 lengths
        self.command(0xBB, 0x1F)  # Pre-charge voltage
        self.command(0xB4, 0xA0, 0xFD)  # Display enhancement A (External VSL)
        self.command(0xBE, 0x04)  # Set VcomH
        self.command(0xA6)  # Normal display (reset)
        self.command(0xAF)  # Exit partial display

    def _set_position(self, top, bottom):
        coladdr_start = 28
        coladdr_end = 91

        self.command(0x15, coladdr_start, coladdr_end)  # set column addr
        self.command(0x75, top, bottom - 1)             # Reset row addr
        self.command(0x5C)                              # Enable MCU to write data into RAM

    def command(self, cmd, *args):
        """
        Sends a command and an (optional) sequence of arguments through to the
        delegated serial interface. Note that the arguments are passed through
        as data.
        """
        self._serial_interface.command(cmd)
        if len(args) > 0:
            self._serial_interface.data(list(args))

    def _render_mono(self, buf, pixel_data):
        i = 0
        for pix in pixel_data:
            if pix > 0:
                buf[i] = 0xFF

            i += 1

    def _render_greyscale(self, buf, pixel_data):
        i = 0
        for r, g, b in pixel_data:
            # RGB->Greyscale luma calculation into 4-bits
            grey = (r * 306 + g * 601 + b * 117) >> 14

            # NHD uses 2 SEG lines and one COM line per pixel
            if grey > 0:
                buf[i // 2] |= (grey << 4) | grey
            i += 2

    def display(self, image):
        """
        Takes a 1-bit monochrome or 24-bit RGB image and renders it
        to the greyscale OLED display. RGB pixels are converted to 8-bit
        greyscale values using a simplified Luma calculation, based on
        *Y'=0.299R'+0.587G'+0.114B'*.

        :param image: the image to render
        :type image: PIL.Image.Image
        """
        assert image.mode == self.mode
        assert image.size == self.size

        image = self.preprocess(image)

        for image, bounding_box in self.framebuffer.redraw(image):
            left, top, right, bottom = bounding_box
            width = right - left
            height = bottom - top

            buf = bytearray(width * height)
            self._set_position(top, bottom)
            self._populate(buf, image.getdata())
            self.data(list(buf))


class ssd1325(greyscale_device):
    """
    Serial interface to a 4-bit greyscale SSD1325 OLED display.

    On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.
    """

    def __init__(self, serial_interface=None, width=128, height=64, rotate=0,
                 mode="RGB", framebuffer=None, **kwargs):
        super(ssd1325, self).__init__(luma.core.const.common, serial_interface,
                                      width, height, rotate, mode, framebuffer,
                                      nibble_order=1, **kwargs)

    def _supported_dimensions(self):
        return [(128, 64)]

    def _init_sequence(self):
        self.command(
            0xAE,               # Diplay off (all pixels off)
            0xB3, 0xF2,         # Display divide clockratio/freq
            0xA8, 0x3F,         # Set MUX ratio
            0xA2, 0x4C,         # Display offset
            0xA1, 0x00,         # Display start line
            0xAD, 0x02,         # Master configuration (external Vcc)
            0xA0, 0x50,         # Set remap (enable COM remap & split odd/even)
            0x86,               # Set current range (full)
            0xB8, 0x01, 0x11,   # Set greyscale table
            0x22, 0x32, 0x43,   # .. cont
            0x54, 0x65, 0x76,   # .. cont
            0xB2, 0x51,         # Set row period
            0xB1, 0x55,         # Set phase length
            0xB4, 0x03,         # Set pre-charge compensation level
            0xB0, 0x28,         # Set pre-charge compensation enable
            0xBC, 0x01,         # Pre-charge voltage
            0xBE, 0x00,         # Set VcomH
            0xBF, 0x02,         # Set VSL (not connected)
            0xA4)               # Normal dislay

    def _set_position(self, top, right, bottom, left):
        self.command(
            0x15, left >> 1, (right - 1) >> 1,  # set column addr
            0x75, top, bottom - 1)  # set row addr


class ssd1327(greyscale_device):
    """
    Serial interface to a 4-bit greyscale SSD1327 OLED display.

    On creation, an initialization sequence is pumped to the display to
    properly configure it. Further control commands can then be called to
    affect the brightness and other settings.

    .. versionadded:: 2.4.0
    """

    def __init__(self, serial_interface=None, width=128, height=128, rotate=0,
                 mode="RGB", framebuffer=None, **kwargs):
        super(ssd1327, self).__init__(luma.core.const.common, serial_interface,
                                      width, height, rotate, mode, framebuffer,
                                      nibble_order=1, **kwargs)

    def _supported_dimensions(self):
        return [(128, 128)]

    def _init_sequence(self):
        self.command(
            0xAE,               # Display off (all pixels off)
            0xA0, 0x53,         # Segment remap (com split, com remap, nibble remap, column remap)
            0xA1, 0x00,         # Display start line
            0xA2, 0x00,         # Display offset
            0xA4,               # regular display
            0xA8, 0x7F)         # set multiplex ratio: 127

        self.command(
            0xB8, 0x01, 0x11,   # Set greyscale table
            0x22, 0x32, 0x43,   # .. cont
            0x54, 0x65, 0x76)   # .. cont

        self.command(
            0xB3, 0x00,         # Front clock divider: 0, Fosc: 0
            0xAB, 0x01,         # Enable Internal Vdd

            0xB1, 0xF1,         # Set phase periods - 1: 1 clk, 2: 15 clks
            0xBC, 0x08,         # Pre-charge voltage: Vcomh
            0xBE, 0x07,         # COM deselect voltage level: 0.86 x Vcc

            0xD5, 0x62,         # Enable 2nd pre-charge
            0xB6, 0x0F)         # 2nd Pre-charge period: 15 clks

    def _set_position(self, top, right, bottom, left):
        self.command(
            0x15, left >> 1, (right - 1) >> 1,  # set column addr
            0x75, top, bottom - 1)  # set row addr


class ws0010(parallel_device, character, __framebuffer_mixin):
    """
    Serial interface to a monochrome Winstar WS0010 OLED display.  This
    interface will work with most ws0010 powered devices including the weg010016.

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.parallel` instance) to delegate sending
        data and commands through.
    :param width: The number of pixels laid out horizontally.
    :type width: int
    :param height: The number of pixels laid out vertically.
    :type height: int
    :param undefined: The character to display if the font doesn't contain
        the requested character
    :type undefined: str
    :param font: Allows you to override the internal font by passing in an alternate
    :type font: :py:mod:`PIL.ImageFont`
    :param selected_font: Select one of the ws0010's embedded font tables (see
        note).  Can be selected by number or name.  Default is 'FT00'
        (English Japanese).
    :type selected_font: int or str
    :param exec_time: Time in seconds to wait for a command to complete.
        Default is 50 μs (1e-6 * 50) which is enough for all ws0010 commands.
    :type exec_time: float
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param framebuffer: Framebuffering strategy, currently values of
        ``diff_to_previous`` or ``full_frame`` are only supported.
    :type framebuffer: str

    To place text on the display, simply assign the text to the 'text'
    instance variable::

        p = parallel(RS=7, E=8, PINS=[25,24,23,18])
        my_display = ws0010(p, selected_font='FT01')
        my_display.text = 'WS0010 Display\\nFont FT01 5x8'

    For more details on how to use the 'text' interface see
    :class:`luma.core.virtual.character`

    .. note:
        The ws0010 is a fully graphical device that also supports character-based
        operations similar to LCD displays such as the hd44780.  This driver
        uses the graphics mode but includes functionality to allow the device
        to act like a character-based one.  To do this it includes four
        embedded fonts which are available in two sizes (5x8 pixel and 5x10
        pixel).  You can select which font to use by providing the appropriate
        name or number to selected_font during initialization.  You can also use
        any PIL.ImageFont object instead by providing it to the font parameter.
        If you do, the internal fonts will be bypassed.

        Available Internal Fonts
        +--------+---------+----------------------+------+
        | Number | Name    | Font                 | Size |
        +--------+---------+----------------------+------+
        |    0   | FT00    | English Japanese     | 5x8  |
        +--------+---------+----------------------+------+
        |    1   | FT01    | Western European I   | 5x8  |
        +--------+---------+----------------------+------+
        |    2   | FT10    | English Russian      | 5x8  |
        +--------+---------+----------------------+------+
        |    3   | FT11    | Western European II  | 5x8  |
        +--------+---------+----------------------+------+
        |    4   | FT00_10 | English Japanese     | 5x10 |
        +--------+---------+----------------------+------+
        |    5   | FT01_10 | Western European I   | 5x10 |
        +--------+---------+----------------------+------+
        |    6   | FT10_10 | English Russian      | 5x10 |
        +--------+---------+----------------------+------+
        |    7   | FT11_10 | Western European II  | 5x10 |
        +--------+---------+----------------------+------+

    .. versionadded:: 3.6.0
    """

    def __init__(self, serial_interface=None, width=100, height=16, undefined='_', font=None,
                 selected_font=0, exec_time=1e-6 * 50, rotate=0, framebuffer=None,
                 const=luma.oled.const.ws0010, **kwargs):
        super(ws0010, self).__init__(const, serial_interface, exec_time=exec_time, **kwargs)
        self.capabilities(width, height, rotate)
        self.init_framebuffer(framebuffer)
        self.font = font if font is not None else embedded_fonts(self._const.FONTDATA, selected_font=selected_font)
        self._undefined = undefined
        self.device = self

        # Supported modes
        supported = (width, height) in [(40, 8), (40, 16), (60, 8), (60, 16), (80, 8), (80, 16), (100, 8), (100, 16)]
        if not supported:
            raise luma.core.error.DeviceDisplayModeError(
                f"Unsupported display mode: {width} x {height}")

        # In case display just powered up, sleep to be sure it has finished
        # its internal initialization
        sleep(0.5)
        self._reset()
        self.text = ""

    def _reset(self):
        """
        WS0010 Initialization Routine

        Reset (not really needed after power-on but does no harm and is useful
        in case the display is already initialized)

        Send five 0s in four bit mode (e.g. d4-d7 are the only pins that matter)
        Set interface data length FUNCTIONSET|DL8 or FUNCTIONSET|DL4 (again in 4 bit mode)
        Turn Display Off
        Turn internal power off
        Configure Entry Mode (Set Cursor to Right and Shift Off)
        Set Graphics Mode and Internal Power On
        Turn Display On (with Cursor Off and Blink Off)

        Device is now ready to receive data
        """

        dl = 0x03 if self._bitmode == 8 else 0x02
        self.command(0x00, 0x00, dl, self._const.FUNCTIONSET | (dl << 4))
        self.command(self._const.DISPLAYOFF)  # Set Display Off
        self.command(self._const.POWEROFF)
        self.command(self._const.ENTRY)  # Set entry mode to direction right, no shift
        self.command(self._const.POWERON | self._const.GRAPHIC)  # Turn internal power on and set into graphics mode
        self.command(self._const.DISPLAYON)  # Turn Display back on

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the ws0010
        OLED display.
        """
        assert image.mode == self.mode
        assert image.size == self.size

        image = self.preprocess(image)

        for _, bounding_box in self.framebuffer.redraw(image):
            # Expand bounding box to align to cell height boundary (8)
            # TODO: Should consider whether this should be moved into framebuffer class
            left, top, right, bottom = bounding_box
            top = top // 8 * 8
            bottom = bottom // 8 * 8 if not bottom % 8 else (bottom // 8 + 1) * 8

            if self._bitmode == 4:
                # If in 4 bit mode, issue reset to make sure we are in sync with the display
                self._reset()

            w = right - left
            h = bottom - top
            mask = [1 << (i // w) % 8 for i in range(w * h)]
            off = [(w * (i // (w * 8))) + (i % w) for i in range(w * h)]
            buf = bytearray(w * h // 8)

            image_segment = image.crop((left, top, right, bottom))
            for idx, pix in enumerate(image_segment.getdata()):
                if pix > 0:
                    buf[off[idx]] |= mask[idx]

            lines = int((bottom - top) / 8)
            lineSize = int(len(buf) / lines)
            for i in range(lines):
                self.command(self._const.DDRAMADDR + left, self._const.CGRAMADDR + i + (top // 8))  # Set display to current line at the starting column to update
                self.data(buf[lineSize * i:lineSize * (i + 1)])   # Send section of current line that needs to be changed

    def get_font(self, ft):
        """
        Load one of the devices embedded fonts by its index value or name and
        return it

        :param val: The index or the name of the font to return
        :type val: int or str
        """

        return self.font.load(ft)


class winstar_weh(ws0010):
    """
    Serial interface to a monochrome Winstar WEH OLED display.  This is the
    character version of the display using the ws0010 controller.  This class
    provides the same ``text`` property as the ws0010 interface so you can set
    the text value which will be rendered to the display's screen.  This
    interface uses a variant of the ws0010 controller's built-in font that is
    designed to match the grid structure of the weh displays (see note below).

    :param serial_interface: The serial interface (usually a
        :py:class:`luma.core.interface.serial.parallel` instance) to delegate sending
        data and commands through.
    :param width: The number of characters that can be displayed on a single line.
        Example: the weh001602a has a width of 16 characters.
    :type width: int
    :param height: The number of lines the display has.  Example: the weh001602a
        has a height of 2 lines.
    :type height: int
    :param undefined: The character to display if the font doesn't contain
        the requested character
    :type undefined: str
    :param font: Allows you to override the internal font by passing in an alternate
    :type font: :py:mod:`PIL.ImageFont`
    :param default_table: Select one of the ws0010's four embedded font tables
        (see :py:class:`ws0010` documentation)
    :type default_table: int
    :param embedded_font: Select the size of the embedded font to use.  Allowed
        sizes are 5x8 (default) and 5x10
    :type embedded_font: str '5x8' or '5x10'
    :param exec_time: Time in seconds to wait for a command to complete.
        Default is 50 μs (1e-6 * 50)
    :type exec_time: float
    :param rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param framebuffer: Framebuffering strategy, currently values of
        ``diff_to_previous`` or ``full_frame`` are only supported.
    :type framebuffer: str

    .. note:
      The WEH devices mimic character displays by having a small gap every fifth
      horizontal pixel. So, while the device can be addressed as a graphical
      display, the images that are shown will have a one pixel gap every 5th pixel.
      For this reason, you should be careful when designing you screens to
      account for this effect.

      The included text functionality automatically takes care of this for you
      if you are displaying character-based content.

    .. versionadded:: 3.6.0
    """

    def __init__(self, serial_interface=None, width=16, height=2, **kwargs):
        super(winstar_weh, self).__init__(const=luma.oled.const.winstar_weh, serial_interface=serial_interface, width=width * 5, height=height * 8, xwidth=5, **kwargs)
