# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2016 Richard Hull
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


class common(object):
    DISPLAYOFF = 0xAE
    DISPLAYON = 0xAF
    DISPLAYALLON = 0xA5
    DISPLAYALLON_RESUME = 0xA4
    NORMALDISPLAY = 0xA6
    INVERTDISPLAY = 0xA7
    SETREMAP = 0xA0
    SETMULTIPLEX = 0xA8


class ssd1306(common):
    CHARGEPUMP = 0x8D
    COLUMNADDR = 0x21
    COMSCANDEC = 0xC8
    COMSCANINC = 0xC0
    EXTERNALVCC = 0x1
    MEMORYMODE = 0x20
    PAGEADDR = 0x22
    SETCOMPINS = 0xDA
    SETCONTRAST = 0x81
    SETDISPLAYCLOCKDIV = 0xD5
    SETDISPLAYOFFSET = 0xD3
    SETHIGHCOLUMN = 0x10
    SETLOWCOLUMN = 0x00
    SETPRECHARGE = 0xD9
    SETSEGMENTREMAP = 0xA1
    SETSTARTLINE = 0x40
    SETVCOMDETECT = 0xDB
    SWITCHCAPVCC = 0x2


sh1106 = ssd1306


class ssd1331(common):
    ACTIVESCROLLING = 0x2F
    CLOCKDIVIDER = 0xB3
    CONTINUOUSSCROLLINGSETUP = 0x27
    DEACTIVESCROLLING = 0x2E
    DISPLAYONDIM = 0xAC
    LOCKMODE = 0xFD
    MASTERCURRENTCONTROL = 0x87
    NORMALDISPLAY = 0xA4
    PHASE12PERIOD = 0xB1
    POWERSAVEMODE = 0xB0
    SETCOLUMNADDR = 0x15
    SETCONTRASTA = 0x81
    SETCONTRASTB = 0x82
    SETCONTRASTC = 0x83
    SETDISPLAYOFFSET = 0xA2
    SETDISPLAYSTARTLINE = 0xA1
    SETMASTERCONFIGURE = 0xAD
    SETPRECHARGESPEEDA = 0x8A
    SETPRECHARGESPEEDB = 0x8B
    SETPRECHARGESPEEDC = 0x8C
    SETPRECHARGEVOLTAGE = 0xBB
    SETROWADDR = 0x75
    SETVVOLTAGE = 0xBE
