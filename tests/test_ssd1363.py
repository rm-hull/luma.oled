#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2024 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.oled.device import ssd1363
from luma.core.render import canvas
from luma.core.framebuffer import full_frame

from baseline_data import get_reference_data, primitives
from helpers import serial, assert_invalid_dimensions, setup_function  # noqa: F401
from unittest.mock import call


def test_init_256x128():
    """
    SSD1363 OLED with a 256 x 128 resolution initialises correctly.

    The SSD1363 DC-pin protocol means each command opcode is a separate
    serial.command() call; parameter bytes arrive via serial.data() (DC-HIGH).
    """
    ssd1363(serial, framebuffer=full_frame())

    # Each opcode in the init sequence arrives as its own command() call.
    serial.command.assert_has_calls([
        call(0xFD),   # Unlock command register
        call(0xAE),   # Display OFF
        call(0xC1),   # Contrast (opcode only)
        call(0xA0),   # Remap (opcode only)
        call(0xA2),   # Display offset (opcode only)
        call(0xCA),   # Mux ratio (opcode only)
        call(0xAD),   # Internal IREF (opcode only)
        call(0xB3),   # Clock divider (opcode only)
        call(0xB9),   # Linear grayscale table (no params)
        call(0xC1),   # contrast(0x7F) from base class
        call(0x15),   # column window (clear → display → _set_position)
        call(0x75),   # row window
        call(0x5C),   # Write RAM
        call(0xAF),   # Display ON (show)
    ])

    # Parameter bytes arrive via data() (DC-HIGH), one call per command.
    serial.data.assert_has_calls([
        call([0x12]),           # Unlock param
        call([0xA0]),           # Contrast init param
        call([0x32, 0x00]),     # Remap params
        call([0x20]),           # Display offset param
        call([0x7F]),           # Mux ratio param
        call([0x90]),           # IREF param
        call([0x61]),           # Clock divider param
        call([0x7F]),           # contrast(0x7F) param
        call([8, 71]),          # column window [8..71] for 256 px width
        call([0, 127]),         # row window [0..127] for 128 px height
        call([0] * (256 * 128 // 2)),   # clear frame (16384 zero bytes)
    ])


def test_init_invalid_dimensions():
    """
    SSD1363 OLED with an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    assert_invalid_dimensions(ssd1363, serial, 256, 64)


def test_hide():
    """
    SSD1363 OLED screen content can be hidden.
    """
    device = ssd1363(serial)
    serial.reset_mock()
    device.hide()
    serial.command.assert_called_once_with(0xAE)


def test_show():
    """
    SSD1363 OLED screen content can be shown.
    """
    device = ssd1363(serial)
    serial.reset_mock()
    device.show()
    serial.command.assert_called_once_with(0xAF)


def test_contrast():
    """
    SSD1363 contrast() sends opcode at DC-LOW then level at DC-HIGH.

    The base class contrast() calls self.command(SETCONTRAST, level) which,
    through the overridden command(), correctly routes the level byte as data.
    """
    device = ssd1363(serial)
    serial.reset_mock()
    device.contrast(0x80)
    serial.command.assert_called_once_with(0xC1)
    serial.data.assert_called_once_with([0x80])


def test_greyscale_display():
    """
    SSD1363 OLED screen can draw and display a greyscale image.

    Verifies that _set_position uses the correct column arithmetic
    (pixel_x // 4 + 8) and that byte pairs are swapped in the output buffer.
    """
    device = ssd1363(serial, mode="RGB", framebuffer=full_frame())
    serial.reset_mock()

    with canvas(device) as draw:
        primitives(device, draw)

    # _set_position sends three separate command() calls.
    serial.command.assert_has_calls([
        call(0x15),   # column window opcode
        call(0x75),   # row window opcode
        call(0x5C),   # Write RAM
    ])
    serial.data.assert_has_calls([
        call([8, 71]),    # full-width column window
        call([0, 127]),   # full-height row window
    ])

    # To regenerate test data, uncomment the following (remember not to commit though)
    # ================================================================================
    # from baseline_data import save_reference_data
    # save_reference_data("demo_ssd1363_greyscale", serial.data.call_args.args[0])

    # Pixel data (last data() call) matches the reference image, including swap.
    assert serial.data.call_args == call(get_reference_data('demo_ssd1363_greyscale'))


def test_monochrome_display():
    """
    SSD1363 OLED screen can draw and display a monochrome image.
    """
    device = ssd1363(serial, mode="1", framebuffer=full_frame())
    serial.reset_mock()

    with canvas(device) as draw:
        primitives(device, draw)

    serial.command.assert_has_calls([
        call(0x15),
        call(0x75),
        call(0x5C),
    ])
    serial.data.assert_has_calls([
        call([8, 71]),
        call([0, 127]),
    ])

    # To regenerate test data, uncomment the following (remember not to commit though)
    # ================================================================================
    # from baseline_data import save_reference_data
    # save_reference_data("demo_ssd1363_monochrome", serial.data.call_args.args[0])

    assert serial.data.call_args == call(get_reference_data('demo_ssd1363_monochrome'))
