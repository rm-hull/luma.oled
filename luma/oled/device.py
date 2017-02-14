# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

# Example usage:
#
#   from luma.core.serial import i2c, spi
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
import luma.oled.const


class sh1106(device):
    """
    Encapsulates the serial interface to the monochrome SH1106 OLED display
    hardware. On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=128, height=64, rotate=0, **kwargs):
        super(sh1106, self).__init__(luma.oled.const.sh1106, serial_interface)
        self.capabilities(width, height, rotate)
        self._pages = self._h // 8

        # FIXME: Delay doing anything here with alternate screen sizes
        # until we are able to get a device to test with.
        if width != 128 or height != 64:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self.command(
            self._const.DISPLAYOFF,
            self._const.MEMORYMODE,
            self._const.SETHIGHCOLUMN,      0xB0, 0xC8,
            self._const.SETLOWCOLUMN,       0x10, 0x40,
            self._const.SETSEGMENTREMAP,
            self._const.NORMALDISPLAY,
            self._const.SETMULTIPLEX,       0x3F,
            self._const.DISPLAYALLON_RESUME,
            self._const.SETDISPLAYOFFSET,   0x00,
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
    Encapsulates the serial interface to the monochrome SSD1306 OLED display
    hardware. On creation, an initialization sequence is pumped to the display
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
            (96, 16): dict(multiplex=0x0F, displayclockdiv=0x60, compins=0x02)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self._pages = height // 8
        self._mask = [1 << (i // width) % 8 for i in range(width * height)]
        self._offsets = [(width * (i // (width * 8))) + (i % width) for i in range(width * height)]

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
            self._const.COLUMNADDR, 0x00, self._w - 1,
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
    Encapsulates the serial interface to the 16-bit color (5-6-5 RGB) SSD1331
    OLED display hardware. On creation, an initialization sequence is pumped to
    the display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=96, height=64, rotate=0, **kwargs):
        super(ssd1331, self).__init__(luma.oled.const.ssd1331, serial_interface)
        self.capabilities(width, height, rotate, mode="RGB")
        self._buffer_size = width * height * 2

        if width != 96 or height != 64:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self.command(
            self._const.DISPLAYOFF,
            self._const.SETREMAP,             0x72,
            self._const.SETDISPLAYSTARTLINE,  0x00,
            self._const.SETDISPLAYOFFSET,     0x00,
            self._const.NORMALDISPLAY,
            self._const.SETMULTIPLEX,         0x3F,
            self._const.SETMASTERCONFIGURE,   0x8E,
            self._const.POWERSAVEMODE,        0x0B,
            self._const.PHASE12PERIOD,        0x74,
            self._const.CLOCKDIVIDER,         0xD0,
            self._const.SETPRECHARGESPEEDA,   0x80,
            self._const.SETPRECHARGESPEEDB,   0x80,
            self._const.SETPRECHARGESPEEDC,   0x80,
            self._const.SETPRECHARGEVOLTAGE,  0x3E,
            self._const.SETVVOLTAGE,          0x3E,
            self._const.MASTERCURRENTCONTROL, 0x0F)

        self.contrast(0xFF)
        self.clear()
        self.show()

    def display(self, image):
        """
        Takes a 24-bit RGB :py:mod:`PIL.Image` and dumps it to the SSD1331 OLED
        display.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        self.command(
            self._const.SETCOLUMNADDR, 0x00, self._w - 1,
            self._const.SETROWADDR, 0x00, self._h - 1)

        i = 0
        buf = bytearray(self._buffer_size)
        for r, g, b in image.getdata():
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
        assert(level >= 0)
        assert(level <= 255)
        self.command(self._const.SETCONTRASTA, level,
                     self._const.SETCONTRASTB, level,
                     self._const.SETCONTRASTC, level)


class ssd1322(device):
    """
    Encapsulates the serial interface to the 4-bit greyscale SSD1322 OLED
    display hardware. On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=256, height=64, rotate=0,
                 mode="RGB", **kwargs):
        super(ssd1322, self).__init__(luma.oled.const.ssd1322, serial_interface)
        self.capabilities(width, height, rotate, mode)
        self._buffer_size = width * height // 2
        self._coladdr_start = (480 - width) // 8
        self._coladdr_end = self._coladdr_start + (width // 4) - 1

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

    def _render_mono(self, buf, image):
        i = 0
        for pix in image.getdata():
            if pix > 0:
                if i % 2 == 0:
                    buf[i // 2] = 0xF0
                else:
                    buf[i // 2] |= 0x0F

            i += 1

    def _render_greyscale(self, buf, image):
        i = 0
        for r, g, b in image.getdata():
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
        Takes a 1-bit monochrome or 24-bit RGB :py:mod:`PIL.Image` and dumps it
        to the SSD1322 OLED display, converting the image pixels to 4-bit
        greyscale using a simplified Luma calculation, based on
        *Y'=0.299R'+0.587G'+0.114B'*.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        self.command(0x15, self._coladdr_start, self._coladdr_end)  # set column addr
        self.command(0x75, 0x00, 0x7F)      # Reset row addr
        self.command(0x5C)                  # Enable MCU to write data into RAM

        buf = bytearray(self._buffer_size)

        if self.mode == "1":
            self._render_mono(buf, image)
        else:
            self._render_greyscale(buf, image)

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
    Encapsulates the serial interface to the 4-bit greyscale SSD1325 OLED
    display hardware. On creation, an initialization sequence is pumped to the
    display to properly configure it. Further control commands can then be
    called to affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=128, height=64, rotate=0,
                 mode="RGB", **kwargs):
        super(ssd1325, self).__init__(luma.oled.const.ssd1325, serial_interface)
        self.capabilities(width, height, rotate, mode)
        self._buffer_size = width * height // 2

        if width != 128 or height != 64:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self.command(
            self._const.DISPLAYOFF,
            self._const.SETCLOCK,               0xF1,
            self._const.SETMULTIPLEX,           0x3F,
            self._const.SETOFFSET,              0x4C,
            self._const.SETSTARTLINE,           0x00,
            self._const.MASTERCONFIG,           0x02,
            self._const.SETREMAP,               0x50,
            self._const.SETCURRENT + 2,
            self._const.SETGRAYTABLE,           0x01, 0x11, 0x22, 0x32, 0x43, 0x54, 0x65, 0x76)

        self.contrast(0xFF)

        self.command(
            self._const.SETROWPERIOD,           0x51,
            self._const.SETPHASELEN,            0x55,
            self._const.SETPRECHARGECOMP,       0x02,
            self._const.SETPRECHARGECOMPENABLE, 0x28,
            self._const.SETVCOMLEVEL,           0x1C,
            self._const.SETVSL,                 0x0F,
            self._const.NORMALDISPLAY)

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
            self._const.SETCOLUMNADDR, 0x00, self._w - 1,
            self._const.SETROWADDR, 0x00, self._h - 1)

        buf = bytearray(self._buffer_size)

        if self.mode == "1":
            self._render_mono(buf, image)
        else:
            self._render_greyscale(buf, image)

        self.data(list(buf))
