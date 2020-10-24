#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from io import open
from setuptools import setup, find_packages


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
project_url = 'https://github.com/rm-hull/luma.oled'

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'pytest<=4.5',
    'pytest-cov',
    'pytest-timeout'
]

setup(
    name="luma.oled",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description=("A small library to drive an OLED device with either "
                 "SSD1306, SSD1309, SSD1322, SSD1325, SSD1327, SSD1331, "
                 "SSD1351, SSD1362, SH1106 or WS0010 chipset"),
    long_description="\n\n".join([README, CONTRIB, CHANGES]),
    long_description_content_type="text/x-rst",
    python_requires='>=3.6, <4',
    license="MIT",
    keywords=("raspberry pi rpi oled display screen "
              "rgb monochrome greyscale color "
              "ssd1306 ssd1309 ssd1322 ssd1325 ssd1327 ssd1331 ssd1351 sh1106 "
              "ws0010 WEH001602A WEG010016A "
              "spi i2c parallel 6800 pcf8574 "),

    url=project_url,
    download_url=project_url + "/tarball/" + version,
    project_urls={
        'Documentation': 'https://luma-oled.readthedocs.io',
        'Source': project_url,
        'Issue Tracker': project_url + '/issues',
    },
    packages=find_packages(),
    namespace_packages=["luma"],
    zip_safe=False,
    install_requires=["luma.core>=1.16.2,<2.0.0"],
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
