#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as r:
        return r.read()


README = read_file("README.rst")
CONTRIB = read_file("CONTRIBUTING.rst")
CHANGES = read_file("CHANGES.rst")
version = read_file("VERSION.txt").strip()

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'mock;python_version<"3.3"',
    "pytest>=3.1",
    "pytest-cov"
]

setup(
    name="luma.oled",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description=("A small library to drive an OLED device with either "
                 "SSD1306, SSD1322, SSD1325, SSD1331 or SH1106 chipset"),
    long_description="\n\n".join([README, CONTRIB, CHANGES]),
    license="MIT",
    keywords=("raspberry pi rpi oled display screen "
              "rgb monochrome greyscale color "
              "ssd1306 ssd1322 ssd1325 ssd1331 sh1106 "
              "spi i2c 256x64 128x64 128x32 96x16"),
    url="https://github.com/rm-hull/luma.oled",
    download_url="https://github.com/rm-hull/luma.oled/tarball/" + version,
    namespace_packages=["luma"],
    packages=["luma.oled"],
    zip_safe=False,
    install_requires=["luma.core>=1.0.0"],
    setup_requires=pytest_runner,
    tests_require=test_deps,
    extras_require={
        'docs': [
            'sphinx >= 1.5.1'
        ],
        'qa': [
            'rstcheck',
            'flake8'
        ],
        'test': test_deps
    },
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
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
