#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from io import open

from setuptools import setup


def read_file(fpath):
    with open(fpath, encoding='utf-8') as r:
        return r.read()


def find_version(*file_paths):
    fpath = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = read_file(fpath)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    err_msg = 'Unable to find version string in {}'.format(fpath)
    raise RuntimeError(err_msg)


README = read_file('README.rst')
CONTRIB = read_file('CONTRIBUTING.rst')
CHANGES = read_file('CHANGES.rst')
version = find_version('luma', 'oled', '__init__.py')

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'mock;python_version<"3.3"',
    'pytest>=3.1',
    'pytest-cov'
]

setup(
    name="luma.oled",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description=("A small library to drive an OLED device with either "
                 "SSD1306, SSD1322, SSD1325, SSD1331, SSD1351 or SH1106 chipset"),
    long_description="\n\n".join([README, CONTRIB, CHANGES]),
    license="MIT",
    keywords=("raspberry pi rpi oled display screen "
              "rgb monochrome greyscale color "
              "ssd1306 ssd1322 ssd1325 ssd1331 ssd1351 sh1106 "
              "spi i2c 256x64 128x64 128x32 96x16"),
    url="https://github.com/rm-hull/luma.oled",
    download_url="https://github.com/rm-hull/luma.oled/tarball/" + version,
    namespace_packages=["luma"],
    packages=["luma.oled"],
    zip_safe=False,
    install_requires=["luma.core>=1.6.0"],
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
