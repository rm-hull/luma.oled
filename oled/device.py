#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2015 Richard Hull
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# See examples directory for usage.

# Stdlib.
import logging
import struct
import sys

# 3rd party.
try:
    import wiringpi2
except ImportError:
    logging.error('Need wiringPi2. Try: sudo pip install wiringpi2')
    raise


logging.basicConfig(level=logging.DEBUG)
        

class I2C(object):
    """Wrap a I2C serial interface.
    """
    def __init__(self, port=1, address=0x3C, cmd_mode=0x00, data_mode=0x40):
        self._address = address
        self._cmd_mode = cmd_mode
        self._data_mode = data_mode
        self._fd = wiringpi2.wiringPiI2CSetup(port)

    def command(self, *cmd):
        """Sends a command or sequence of commands through to the device -
        maximum allowed is 32 bytes in one go.
        """
        assert(len(cmd) <= 32)
        wiringpi2.wiringPiI2CWriteReg8(self._fd, self._address, self._cmd_mode)
        buf = struct.pack('{}B'.format(len(cmd)), *cmd)
        wiringpi2.wiringPiI2CWrite(self._fd, buf)

    def data(self, data):
        """Sends a data byte or sequence of data bytes through to the device -
        maximum allowed in one transaction is 32 bytes, so if data is larger
        than this it is sent in chunks.
        """
        wiringpi2.wiringPiI2CWriteReg8(self._fd, self._address, self._data_mode)
        for i in xrange(0, len(data), 32):
            v = data[i:i+32]
            buf = struct.pack('{}B'.format(len(v)), *v)
            wiringpi2.wiringPiI2CWrite(self._fd, buf)

    def reset(self):
        pass

class SPI(object):
    """Wrap an SPI serial interface.
    """
    def __init__(self, port=0, spi_bus_speed_hz=32000000, gpio_command_data_select=24, gpio_reset=25):
        self._port = port
        self._gpio_command_data_select = gpio_command_data_select
        self._gpio_reset = gpio_reset
        wiringpi2.wiringPiSetupGpio()
        wiringpi2.wiringPiSPISetup(port, spi_bus_speed_hz)
        wiringpi2.pinMode(gpio_command_data_select, 1)
        wiringpi2.pinMode(gpio_reset, 1)
        
    def command(self, *cmd):
        assert(len(cmd) <= 32)
        wiringpi2.digitalWrite(self._gpio_command_data_select, 0) 
        buf = struct.pack('{}B'.format(len(cmd)), *cmd)
        wiringpi2.wiringPiSPIDataRW(self._port, buf)

    def data(self, data):
        wiringpi2.digitalWrite(self._gpio_command_data_select, 1)
        for i in xrange(0, len(data), 32):
            v = data[i:i+32]
            buf = struct.pack('{}B'.format(len(v)), *v)
            wiringpi2.wiringPiSPIDataRW(self._port, buf)

    def reset(self):
        wiringpi2.digitalWrite(self._gpio_reset, 0)
        wiringpi2.delay(1)
        wiringpi2.digitalWrite(self._gpio_reset, 1)
        wiringpi2.delay(1)
            

class sh1106(object):
    def __init__(self, serial_interface):
        self._serial_interface = serial_interface
        self.width = 128
        self.height = 64
        self.pages = self.height / 8
        
        self._serial_interface.reset()

        self._serial_interface.command(
            _Command.DISPLAYOFF,
            _Command.MEMORYMODE,
            _Command.SETHIGHCOLUMN,      0xB0, 0xC8,
            _Command.SETLOWCOLUMN,       0x10, 0x40,
            _Command.SETCONTRAST,        0x7F,
            _Command.SETSEGMENTREMAP,
            _Command.NORMALDISPLAY,
            _Command.SETMULTIPLEX,       0x3F,
            _Command.DISPLAYALLON_RESUME,
            _Command.SETDISPLAYOFFSET,   0x00,
            _Command.SETDISPLAYCLOCKDIV, 0xF0,
            _Command.SETPRECHARGE,       0x22,
            _Command.SETCOMPINS,         0x12,
            _Command.SETVCOMDETECT,      0x20,
            _Command.CHARGEPUMP,         0x14,
            _Command.DISPLAYON)

    def display(self, image):
        """
        Takes a 1-bit image and dumps it to the SH1106 OLED display.
        """
        assert(image.mode == '1')
        assert(image.size[0] == self.width)
        assert(image.size[1] == self.height)

        page = 0xB0
        pix = list(image.getdata())
        step = self.width * 8
        for y in xrange(0, self.pages * step, step):
            # move to given page, then reset the column address
            self._serial_interface.command(page, 0x02, 0x10)
            page += 1
            buf = []
            for x in xrange(self.width):
                byte = 0
                for n in xrange(0, step, self.width):
                    byte |= (pix[x + y + n] & 0x01) << 8
                    byte >>= 1
                buf.append(byte)
            self._serial_interface.data(buf)


class ssd1306(object):
    def __init__(self, serial_interface):
        self._serial_interface = serial_interface
        self.width = 128
        self.height = 64
        self.pages = self.height / 8

        self._serial_interface.reset()
        
        self._serial_interface.command(
            _Command.DISPLAYOFF,
            _Command.SETDISPLAYCLOCKDIV, 0x80,
            _Command.SETMULTIPLEX,       0x3F,
            _Command.SETDISPLAYOFFSET,   0x00,
            _Command.SETSTARTLINE,
            _Command.CHARGEPUMP,         0x14,
            _Command.MEMORYMODE,         0x00,
            _Command.SEGREMAP,
            _Command.COMSCANDEC,
            _Command.SETCOMPINS,         0x12,
            _Command.SETCONTRAST,        0xCF,
            _Command.SETPRECHARGE,       0xF1,
            _Command.SETVCOMDETECT,      0x40,
            _Command.DISPLAYALLON_RESUME,
            _Command.NORMALDISPLAY,
            _Command.DISPLAYON)

    def display(self, image):
        """
        Takes a 1-bit image and dumps it to the SSD1306 OLED display.
        """
        assert(image.mode == '1')
        assert(image.size[0] == self.width)
        assert(image.size[1] == self.height)

        self._serial_interface.command(
            _Command.COLUMNADDR, 0x00, self.width-1,  # Column start/end address
            _Command.PAGEADDR,   0x00, self.pages-1)  # Page start/end address

        pix = list(image.getdata())
        step = self.width * 8
        buf = []
        for y in xrange(0, self.pages * step, step):
            i = y + self.width-1
            while i >= y:
                byte = 0
                for n in xrange(0, step, self.width):
                    byte |= (pix[i + n] & 0x01) << 8
                    byte >>= 1

                buf.append(byte)
                i -= 1

        self._serial_interface.data(buf)


class _Command:
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
    SETSEGMENTREMAP = 0xA1
    SETSTARTLINE = 0x40
    SETVCOMDETECT = 0xDB
    SWITCHCAPVCC = 0x2
