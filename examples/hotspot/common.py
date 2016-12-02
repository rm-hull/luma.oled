#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import ImageFont


tiny_font = ImageFont.truetype("examples/fonts/FreePixel.ttf", 10)


def bytes2human(n, fmt="{0:0.2f}"):
    symbols = [
        ('YB', 2 ** 80),
        ('ZB', 2 ** 70),
        ('EB', 2 ** 60),
        ('PB', 2 ** 50),
        ('TB', 2 ** 40),
        ('GB', 2 ** 30),
        ('MB', 2 ** 20),
        ('KB', 2 ** 10),
        ('B', 2 ** 0)
    ]

    for suffix, v in symbols:
        if n >= v:
            value = float(n) / v
            return fmt.format(value) + suffix
    return "{0}B".format(n)


def right_text(draw, y, width, margin, text):
    x = width - margin - draw.textsize(text, font=tiny_font)[0]
    draw.text((x, y), text=text, font=tiny_font, fill="white")


def title_text(draw, y, width, text):
    x = (width - draw.textsize(text)[0]) / 2
    draw.text((x, y), text=text, fill="yellow")
