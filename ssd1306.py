#/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2014 Richard Hull
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Example usage:
#
#   from ssd1306 import device, canvas
#   from PIL import ImageFont, ImageDraw
#
#   font = ImageFont.load_default()
#   oled = device(port=1, address=0x3C)
#
#   with canvas(oled) as draw:
#      draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
#      draw.text(30, 40, "Hello World", font=font, fill=255)
#
# As soon as the with-block scope level is complete, the graphics primitives
# will be flushed to the device.
#
# Creating a new canvas is effectively 'carte blanche': If you want to retain
# an existing canvas, then make a reference like:
#
#    c = canvas(oled)
#    for X in ...:
#        with c as draw:
#            draw.rectangle(...)
#
# As before, as soon as the with block completes, the canvas buffer is flushed
# to the device

import smbus
from PIL import Image, ImageDraw


class canvas:
    """
    A canvas returns a properly-sized `ImageDraw` object onto which the caller
    can draw upon. As soon as the with-block completes, the resultant image is
    flushed onto the device.
    """
    def __init__(self, device):
        self.image = Image.new('1', (device.width, device.height))
        self.device = device

    def __enter__(self):
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def __exit__(self, type, value, traceback):
        if type is None:
            # do the drawing onto the device
            self.device.display(self.image)

        del self.draw   # Tidy up the resources
        return False    # Never suppress exceptions


class device:
    """
    A device encapsulates the I2C connection (address/port) to the OLED
    display hardware. The init method pumps commands to the display
    to properly initialize it. Further control commands can then be
    called to affect the brightness. Direct use of the command() and
    data() methods are discouraged.
    """
    def __init__(self, port=1, address=0x3C):
        self.bus = smbus.SMBus(port)
        self.address = address
        self.width = 128
        self.height = 64
        self.pages = self.height / 8

        self.command(
            const.DISPLAYON,
            const.SETDISPLAYCLOCKDIV, 0x80,
            const.SETMULTIPLEX,       0x3F,
            const.SETDISPLAYOFFSET,   0x00,
            const.SETSTARTLINE | 0,
            const.CHARGEPUMP,         0x14,
            const.MEMORYMODE,         0x00,
            const.SEGREMAP,
            const.COMSCANDEC,
            const.SETCOMPINS,         0x12,
            const.SETCONTRAST,        0xCF,
            const.SETPRECHARGE,       0xF1,
            const.SETVCOMDETECT,      0x40,
            const.DISPLAYALLON_RESUME,
            const.NORMALDISPLAY,
            const.DISPLAYON)

    def command(self, *cmd):
        """
        Sends a command or sequence of commands through to the
        device - maximum allowed is 32 bytes in one go.
        """
        assert(len(cmd) <= 32)
        self.bus.write_i2c_block_data(self.address, 0x00, list(cmd))

    def data(self, *data):
        """
        Sends a data byte or sequence of data bytes through to the
        device - maximum allowed in one transaction is 32 bytes, so if
        data is larger than this it is sent in chunks.
        """
        for i in xrange(0, len(data), 32):
            self.bus.write_i2c_block_data(self.address, 0x40, list(data[i:i+32]))

    def display(self, image):
        """
        Takes a 1-bit 128x64 image and dumps it to the OLED display. Sections ported from:
        https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/Adafruit_SSD1306/SSD1306.py
        """
        assert(image.mode == '1')
        assert(image.size[0] == self.width)
        assert(image.size[1] == self.height)
        pix = image.load()
        buf = [0] * self.width * self.pages
        index = 0
        for page in xrange(self.pages):
            x = self.width-1
            while x >= 0:
                bits = 0
                for bit in xrange(8):
                    bits = bits << 1
                    bits |= 0 if pix[(x, page*8+7-bit)] == 0 else 1

                buf[index] = bits
                index += 1
                x -= 1

        self.command(
                const.COLUMNADDR, 0x00, self.width-1, # Column start/end address
                const.PAGEADDR,   0x00, self.pages-1) # Page start/end address

        self.data(*buf)

class const:
    CHARGEPUMP = 0x8D
    COLUMNADDR = 0x21
    COMSCANDEC = 0xC8
    COMSCANINC = 0xC0
    DISPLAYALLON = 0xA5
    DISPLAYALLON_RESUME = 0xA4
    DISPLAYOFF = 0xAE
    DISPLAYON = 0xAF
    EXTERNALVCC = 0x1
    INVERTDISPLAY = 0xA7
    MEMORYMODE = 0x20
    NORMALDISPLAY = 0xA6
    PAGEADDR = 0x22
    SEGREMAP = 0xA0
    SETCOMPINS = 0xDA
    SETCONTRAST = 0x81
    SETDISPLAYCLOCKDIV = 0xD5
    SETDISPLAYOFFSET = 0xD3
    SETHIGHCOLUMN = 0x10
    SETLOWCOLUMN = 0x00
    SETMULTIPLEX = 0xA8
    SETPRECHARGE = 0xD9
    SETSTARTLINE = 0x40
    SETVCOMDETECT = 0xDB
    SWITCHCAPVCC = 0x2