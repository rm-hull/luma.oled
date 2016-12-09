#!/usr/bin/env python

import os
from setuptools import setup

import oled

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
version = oled.__version__

setup(
    name="ssd1306",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description=("A small library to drive an OLED device with either "
                 "SSD1306 or SH1106 chipset"),
    long_description=README,
    license="MIT",
    keywords="raspberry pi rpi oled display screen ssd1306 sh1106 spi i2c 128x64 128x32 96x16",
    url="https://github.com/rm-hull/ssd1306",
    download_url="https://github.com/rm-hull/ssd1306/tarball/" + version,
    packages=["oled"],
    install_requires=["pillow", "smbus2", "spidev", "RPi.GPIO"],
    setup_requires=["pytest-runner"],
    tests_require=["mock", "pytest", "pytest-cov", "python-coveralls"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
