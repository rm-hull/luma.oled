#!/usr/bin/env python

from distutils.core import setup,Extension
setup(
    name = "ssd1306",
    version = "0.2.0",
    author = "Richard Hull",
    author_email = "richard.hull@destructuring-bind.org",
    description = ("A small library to drive an OLED device with either SSD1306 or SH1106 chipset"),
    license = "MIT",
    keywords = "raspberry pi rpi oled ssd1306 sh1106",
    url = "https://github.com/rm-hull/ssd1306",
    packages=['oled'],
)
