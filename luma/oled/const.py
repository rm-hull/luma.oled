# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.


from luma.core.const import common


class ssd1306(common):
    CHARGEPUMP = 0x8D
    COLUMNADDR = 0x21
    COMSCANDEC = 0xC8
    COMSCANINC = 0xC0
    EXTERNALVCC = 0x1
    MEMORYMODE = 0x20
    PAGEADDR = 0x22
    SETCOMPINS = 0xDA
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


class ssd1322(common):
    DISPLAYON = 0xAF
    DISPLAYOFF = 0xAE
    SETCONTRAST = 0xC1
