#!/usr/bin/env python

import os
from distutils.core import setup, Extension

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name = "ssd1306",
    version = "0.2.0",
    author = "Richard Hull",
    author_email = "richard.hull@destructuring-bind.org",
    description = "A small library to drive an OLED device with either SSD1306 or SH1106 chipset",
    long_description = README,
    license = "MIT",
    keywords = "raspberry pi rpi oled ssd1306 sh1106",
    url = "https://github.com/rm-hull/ssd1306",
    packages=['oled'],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)
