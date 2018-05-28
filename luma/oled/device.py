# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Collection of serial interfaces to OLED devices.
"""

# Example usage:
#
#   from luma.core.interface.serial import i2c, spi
#   from luma.core.render import canvas
#   from luma.oled.device import ssd1306, sh1106
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
# to the device

from luma.core.device import device
import luma.core.error
import luma.core.framebuffer
import luma.oled.const


__all__ = ["ssd1306", "ssd1322", "ssd1325", "ssd1327", "ssd1331", "ssd1351", "sh1106"]


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
            (128, 64): dict(multiplex=0x3F, displayoffset=0x00),
            (128, 32): dict(multiplex=0x20, displayoffset=0x0F)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

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
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

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


class ssd1306(device):
    """
    Serial interface to a monochrome SSD1306 OLED display.

    On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=128, height=64, rotate=0, **kwargs):
        super(ssd1306, self).__init__(luma.oled.const.ssd1306, serial_interface)
        self.capabilities(width, height, rotate)

        # Supported modes
        settings = {
            (128, 64): dict(multiplex=0x3F, displayclockdiv=0x80, compins=0x12),
            (128, 32): dict(multiplex=0x1F, displayclockdiv=0x80, compins=0x02),
            (96, 16): dict(multiplex=0x0F, displayclockdiv=0x60, compins=0x02),
            (64, 48): dict(multiplex=0x2F, displayclockdiv=0x80, compins=0x12),
            (64, 32): dict(multiplex=0x1F, displayclockdiv=0x80, compins=0x12)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self._pages = height // 8
        self._mask = [1 << (i // width) % 8 for i in range(width * height)]
        self._offsets = [(width * (i // (width * 8))) + (i % width) for i in range(width * height)]
        self._colstart = (0x80 - self._w) // 2
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
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the SSD1306
        OLED display.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

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


class ssd1331(device):
    """
    Serial interface to a 16-bit color (5-6-5 RGB) SSD1331 OLED display.

    On creation, an initialization sequence is pumped to
    the display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.

    :param serial_interface: the serial interface (usually a
        :py:class`luma.core.interface.serial.spi` instance) to delegate sending
        data and commands through.
    :param width: the number of horizontal pixels (optional, defaults to 96).
    :type width: int
    :param height: the number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: an integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param framebuffer: Framebuffering strategy, currently values of
        ``diff_to_previous`` or ``full_frame`` are only supported.
    :type framebuffer: str
    """
    def __init__(self, serial_interface=None, width=96, height=64, rotate=0,
                 framebuffer="diff_to_previous", **kwargs):
        super(ssd1331, self).__init__(luma.oled.const.common, serial_interface)
        self.capabilities(width, height, rotate, mode="RGB")
        self.framebuffer = getattr(luma.core.framebuffer, framebuffer)(self)

        if width != 96 or height != 64:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

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

        self.contrast(0xFF)
        self.clear()
        self.show()

    def display(self, image):
        """
        Renders a 24-bit RGB image to the SSD1331 OLED display.

        :param image: the image to render.
        :type image: PIL.Image.Image
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        if self.framebuffer.redraw_required(image):
            left, top, right, bottom = self.framebuffer.bounding_box
            width = right - left
            height = bottom - top

            self.command(
                0x15, left, right - 1,    # Set column addr
                0x75, top, bottom - 1)    # Set row addr

            i = 0
            buf = bytearray(width * height * 2)
            for r, g, b in self.framebuffer.getdata():
                if not(r == g == b == 0):
                    # 65K format 1
                    buf[i] = r & 0xF8 | g >> 5
                    buf[i + 1] = g << 5 & 0xE0 | b >> 3
                i += 2

            self.data(list(buf))

    def contrast(self, level):
        """
        Switches the display contrast to the desired level, in the range
        0-255. Note that setting the level to a low (or zero) value will
        not necessarily dim the display to nearly off. In other words,
        this method is **NOT** suitable for fade-in/out animation.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0 <= level <= 255)
        self.command(0x81, level,  # Set contrast A
                     0x82, level,  # Set contrast B
                     0x83, level)  # Set contrast C


class ssd1351(device):
    """
    Serial interface to the 16-bit color (5-6-5 RGB) SSD1351 OLED display.

    On creation, an initialization sequence is pumped to
    the display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.

    :param serial_interface: the serial interface (usually a
        :py:class`luma.core.interface.serial.spi` instance) to delegate sending
        data and commands through.
    :param width: the number of horizontal pixels (optional, defaults to 128).
    :type width: int
    :param height: the number of vertical pixels (optional, defaults to 128).
    :type height: int
    :param rotate: an integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param framebuffer: Framebuffering strategy, currently values of
        ``diff_to_previous`` or ``full_frame`` are only supported.
    :type framebuffer: str
    :param bgr: Set to ``True`` if device pixels are BGR order (rather than RGB).
    :type bgr: bool
    :param h_offset: horizontal offset (in pixels) of screen to device memory
        (default: 0)
    :type h_offset: int
    :param v_offset: vertical offset (in pixels) of screen to device memory
        (default: 0)
    :type h_offset: int

    .. versionadded:: 2.3.0
    """
    def __init__(self, serial_interface=None, width=128, height=128, rotate=0,
                 framebuffer="diff_to_previous", h_offset=0, v_offset=0,
                 bgr=False, **kwargs):
        super(ssd1351, self).__init__(luma.oled.const.common, serial_interface)
        self.capabilities(width, height, rotate, mode="RGB")
        self.framebuffer = getattr(luma.core.framebuffer, framebuffer)(self)

        if h_offset != 0 or v_offset != 0:
            def offset(bbox):
                left, top, right, bottom = bbox
                return (left + h_offset, top + v_offset, right + h_offset, bottom + v_offset)
            self.apply_offsets = offset
        else:
            self.apply_offsets = lambda bbox: bbox

        if (width, height) not in [(96, 96), (128, 128)]:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        # RGB or BGR order
        order = 0x02 if bgr else 0x00

        self.command(0xFD, 0x12)              # Unlock IC MCU interface
        self.command(0xFD, 0xB1)              # Command A2,B1,B3,BB,BE,C1 accessible if in unlock state
        self.command(0xAE)                    # Display off
        self.command(0xB3, 0xF1)              # Clock divider
        self.command(0xCA, 0x7F)              # Mux ratio
        self.command(0x15, 0x00, width - 1)   # Set column address
        self.command(0x75, 0x00, height - 1)  # Set row address
        self.command(0xA0, 0x74 | order)      # Segment remapping
        self.command(0xA1, 0x00)              # Set Display start line
        self.command(0xA2, 0x00)              # Set display offset
        self.command(0xB5, 0x00)              # Set GPIO
        self.command(0xAB, 0x01)              # Function select (internal - diode drop)
        self.command(0xB1, 0x32)              # Precharge
        self.command(0xB4, 0xA0, 0xB5, 0x55)  # Set segment low voltage
        self.command(0xBE, 0x05)              # Set VcomH voltage
        self.command(0xC7, 0x0F)              # Contrast master
        self.command(0xB6, 0x01)              # Precharge2
        self.command(0xA6)                    # Normal display

        self.contrast(0xFF)
        self.clear()
        self.show()

    def display(self, image):
        """
        Renders a 24-bit RGB image to the SSD1351 OLED display.

        :param image: the image to render.
        :type image: PIL.Image.Image
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        if self.framebuffer.redraw_required(image):
            left, top, right, bottom = self.apply_offsets(self.framebuffer.bounding_box)
            width = right - left
            height = bottom - top

            self.command(0x15, left, right - 1)    # Set column addr
            self.command(0x75, top, bottom - 1)    # Set row addr
            self.command(0x5C)                     # Write RAM

            i = 0
            buf = bytearray(width * height * 2)
            for r, g, b in self.framebuffer.getdata():
                if not(r == g == b == 0):
                    # 65K format 1
                    buf[i] = r & 0xF8 | g >> 5
                    buf[i + 1] = g << 5 & 0xE0 | b >> 3
                i += 2

            self.data(list(buf))

    def contrast(self, level):
        """
        Switches the display contrast to the desired level, in the range
        0-255. Note that setting the level to a low (or zero) value will
        not necessarily dim the display to nearly off. In other words,
        this method is **NOT** suitable for fade-in/out animation.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0 <= level <= 255)
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


class ssd1322(device):
    """
    Serial interface to a 4-bit greyscale SSD1322 OLED display.

    On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.

    :param serial_interface: the serial interface (usually a
       :py:class`luma.core.interface.serial.spi` instance) to delegate sending
       data and commands through.
    :param width: the number of horizontal pixels (optional, defaults to 96).
    :type width: int
    :param height: the number of vertical pixels (optional, defaults to 64).
    :type height: int
    :param rotate: an integer value of 0 (default), 1, 2 or 3 only, where 0 is
        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
        represents 270° rotation.
    :type rotate: int
    :param mode: Supplying "1" or "RGB" effects a different rendering
         mechanism, either to monochrome or 4-bit greyscale.
    :type mode: str
    :param framebuffer: Framebuffering strategy, currently values of
        ``diff_to_previous`` or ``full_frame`` are only supported
    :type framebuffer: str

    """
    def __init__(self, serial_interface=None, width=256, height=64, rotate=0,
                 mode="RGB", framebuffer="diff_to_previous", **kwargs):
        super(ssd1322, self).__init__(luma.oled.const.ssd1322, serial_interface)
        self.capabilities(width, height, rotate, mode)
        self.framebuffer = getattr(luma.core.framebuffer, framebuffer)(self)
        self.populate = self._render_mono if mode == "1" else self._render_greyscale
        self.column_offset = (480 - width) // 2

        if width <= 0 or width > 256 or \
           height <= 0 or height > 64 or \
           width % 16 != 0 or height % 16 != 0:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

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

        self.contrast(0x7F)             # Reset
        self.clear()
        self.show()

    def _render_mono(self, buf, pixel_data):
        i = 0
        for pix in pixel_data:
            if pix > 0:
                if i % 2 == 0:
                    buf[i // 2] = 0xF0
                else:
                    buf[i // 2] |= 0x0F

            i += 1

    def _render_greyscale(self, buf, pixel_data):
        i = 0
        for r, g, b in pixel_data:
            # RGB->Greyscale luma calculation into 4-bits
            grey = (r * 306 + g * 601 + b * 117) >> 14

            if grey > 0:
                if i % 2 == 0:
                    buf[i // 2] = (grey << 4)
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

            pix_start = self.column_offset + left
            coladdr_start = pix_start >> 2
            coladdr_end = (pix_start + width >> 2) - 1

            self.command(0x15, coladdr_start, coladdr_end)  # set column addr
            self.command(0x75, top, bottom - 1)             # Reset row addr
            self.command(0x5C)                              # Enable MCU to write data into RAM

            buf = bytearray(width * height >> 1)

            self.populate(buf, self.framebuffer.getdata())
            self.data(list(buf))

    def command(self, cmd, *args):
        """
        Sends a command and an (optional) sequence of arguments through to the
        delegated serial interface. Note that the arguments are passed through
        as data.
        """
        self._serial_interface.command(cmd)
        if len(args) > 0:
            self._serial_interface.data(list(args))


class ssd1325(device):
    """
    Serial interface to a 4-bit greyscale SSD1325 OLED display.

    On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=128, height=64, rotate=0,
                 mode="RGB", **kwargs):
        super(ssd1325, self).__init__(luma.core.const.common, serial_interface)
        self.capabilities(width, height, rotate, mode)
        self._buffer_size = width * height // 2

        if width != 128 or height != 64:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

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

        self.contrast(0x7F)
        self.clear()
        self.show()

    def _render_mono(self, buf, image):
        i = 0
        for pix in image.getdata():
            if pix > 0:
                if i % 2 == 0:
                    buf[i // 2] = 0x0F
                else:
                    buf[i // 2] |= 0xF0

            i += 1

    def _render_greyscale(self, buf, image):
        i = 0
        for r, g, b in image.getdata():
            # RGB->Greyscale luma calculation into 4-bits
            grey = (r * 306 + g * 601 + b * 117) >> 14

            if grey > 0:
                if i % 2 == 0:
                    buf[i // 2] = grey
                else:
                    buf[i // 2] |= (grey << 4)

            i += 1

    def display(self, image):
        """
        Takes a 1-bit monochrome or 24-bit RGB :py:mod:`PIL.Image` and dumps it
        to the SSD1325 OLED display, converting the image pixels to 4-bit
        greyscale using a simplified Luma calculation, based on
        *Y'=0.299R'+0.587G'+0.114B'*.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        self.command(
            0x15, 0x00, self._w - 1,  # set column addr
            0x75, 0x00, self._h - 1)  # set row addr

        buf = bytearray(self._buffer_size)

        if self.mode == "1":
            self._render_mono(buf, image)
        else:
            self._render_greyscale(buf, image)

        self.data(list(buf))


class ssd1327(device):
    """
    Serial interface to a 4-bit greyscale SSD1327 OLED display.

    On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=128, height=128, rotate=0,
                 mode="RGB", **kwargs):
        super(ssd1327, self).__init__(luma.core.const.common, serial_interface)
        self.capabilities(width, height, rotate, mode)
        self._buffer_size = width * height // 2

        if width != 128 or height != 128:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self.command(
            0xAE,               # Display off (all pixels off)
            0xA0, 0x53,         # gment remap (com split, com remap, nibble remap, column remap)
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

        self.contrast(0x7F)
        self.clear()
        self.show()

    def _render_mono(self, buf, image):
        i = 0
        for pix in image.getdata():
            if pix > 0:
                if i % 2 == 0:
                    buf[i // 2] = 0x0F
                else:
                    buf[i // 2] |= 0xF0

            i += 1

    def _render_greyscale(self, buf, image):
        i = 0
        for r, g, b in image.getdata():
            # RGB->Greyscale luma calculation into 4-bits
            grey = (r * 306 + g * 601 + b * 117) >> 14

            if grey > 0:
                if i % 2 == 0:
                    buf[i // 2] = grey
                else:
                    buf[i // 2] |= (grey << 4)

            i += 1

    def display(self, image):
        """
        Takes a 1-bit monochrome or 24-bit RGB :py:mod:`PIL.Image` and dumps it
        to the SSD1327 OLED display, converting the image pixels to 4-bit
        greyscale using a simplified Luma calculation, based on
        *Y'=0.299R'+0.587G'+0.114B'*.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        self.command(
            0x15, 0x00, self._w - 1,  # set column addr
            0x75, 0x00, self._h - 1)  # set row addr

        buf = bytearray(self._buffer_size)

        if self.mode == "1":
            self._render_mono(buf, image)
        else:
            self._render_greyscale(buf, image)

        self.data(list(buf))
