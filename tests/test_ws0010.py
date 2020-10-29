#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for the :py:class:`luma.oled.device.ws0010` device.
"""

from luma.core.framebuffer import full_frame
from luma.oled.device import ws0010, winstar_weh
from luma.core.render import canvas
from luma.core.util import bytes_to_nibbles

from PIL import Image, ImageDraw
from unittest.mock import Mock, call

CLEAR = 0x01
HOME = 0x02
ENTRY = 0x06
DISPLAYOFF = 0x08
DISPLAYON = 0x0C
POWEROFF = 0x13
POWERON = 0x17
GRAPHIC = 0x08
CHAR = 0x00
FUNCTIONSET = 0x29
DL8 = 0x10
DL4 = 0x00
DDRAMADDR = 0x80
CGRAMADDR = 0x40

interface = Mock(unsafe=True, _bitmode=4, _pulse_time=1e-6)


def test_init_4bitmode():
    ws0010(interface, framebuffer=full_frame())

    to_4 = \
        [call(0, 0, 0, 0, 0, 2, 2, 9)]

    calls = \
        to_4 + \
        [call(*bytes_to_nibbles([DISPLAYOFF]))] + \
        [call(*bytes_to_nibbles([POWEROFF]))] + \
        [call(*bytes_to_nibbles([ENTRY]))] + \
        [call(*bytes_to_nibbles([POWERON | GRAPHIC]))] + \
        [call(*bytes_to_nibbles([DISPLAYON]))] + \
        [call(*bytes_to_nibbles([DDRAMADDR, CGRAMADDR]))] + \
        [call(*bytes_to_nibbles([DDRAMADDR, CGRAMADDR + 1]))]

    interface.command.assert_has_calls(calls)

    # Data to clear the screen
    calls = \
        [call(bytes_to_nibbles([0] * 100))] + \
        [call(bytes_to_nibbles([0] * 100))]

    interface.data.assert_has_calls(calls)


def test_init_8bitmode():
    interface._bitmode = 8
    ws0010(interface, framebuffer=full_frame())

    to_4 = \
        [call(0, 0, 3, 57)]

    calls = \
        to_4 + \
        [call(DISPLAYOFF)] + \
        [call(POWEROFF)] + \
        [call(ENTRY)] + \
        [call(POWERON | GRAPHIC)] + \
        [call(DISPLAYON)] + \
        [call(*[DDRAMADDR, CGRAMADDR])] + \
        [call(*[DDRAMADDR, CGRAMADDR + 1])]

    interface.command.assert_has_calls(calls)

    # Data to clear the screen
    calls = \
        [call(bytearray([0] * 100))] + \
        [call(bytearray([0] * 100))]

    interface.data.assert_has_calls(calls)


def test_display():
    interface._bitmode = 4
    d = ws0010(interface, framebuffer=full_frame())
    interface.reset_mock()

    # Use canvas to create an all white screen
    with canvas(d) as drw:
        drw.rectangle((0, 0, 99, 15), fill='white', outline='white')

    line1 = [call.command(*bytes_to_nibbles([DDRAMADDR, CGRAMADDR])),
        call.data([0x0F] * 200)]
    line2 = [call.command(*bytes_to_nibbles([DDRAMADDR, CGRAMADDR + 1])),
        call.data([0x0F] * 200)]

    interface.assert_has_calls(line1 + line2)


def test_get_font():
    interface._bitmode = 8
    device = ws0010(interface, framebuffer=full_frame())

    img = Image.new('1', (11, 8), 0)
    device.font.current = 0
    f0 = device.font.current
    f3 = device.get_font('FT11')
    drw = ImageDraw.Draw(img)

    assert f0.getsize('\u00E0') == (5, 8)
    assert f0.getsize('A\u00E0') == (11, 8)

    drw.text((0, 0), '\u00E0', font=f0, fill='white')  # Font 0: α
    drw.text((6, 0), '\u00E0', font=f3, fill='white')  # Font 3: à

    # Compare to image containing αà
    assert img.tobytes() == \
        b'\x01\x00\x00\x80I\xc0\xa8 \x91\xe0\x92 i\xe0\x00\x00'


def test_unsupported_display_mode():
    import luma.core
    try:
        ws0010(interface, width=99, height=15)
    except luma.core.error.DeviceDisplayModeError as ex:
        assert str(ex) == "Unsupported display mode: 99 x 15"


def test_winstar_weh():

    class image_retaining_framebuffer(full_frame):

        def redraw(self, image):
            self.image = image
            yield image, (0, 0) + image.size

    interface._bitmode = 4
    device = winstar_weh(interface, framebuffer=image_retaining_framebuffer())

    device.text = 'This is a test'

    img = Image.new('1', (80, 16), 0)
    drw = ImageDraw.Draw(img)
    drw.text((0, 0), 'This is a test', font=device.font, fill='white')

    assert 'This is a test' == str(device.text)
    assert device.font.getsize('This is a test') == (70, 8)
    assert device.framebuffer.image == img
