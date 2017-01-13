Luma.OLED: Display drivers for SSD1306 / SSD1325 / SSD1331 / SH1106
===================================================================
.. image:: https://travis-ci.org/rm-hull/luma.oled.svg?branch=master
   :target: https://travis-ci.org/rm-hull/luma.oled

.. image:: https://coveralls.io/repos/github/rm-hull/luma.oled/badge.svg?branch=master
   :target: https://coveralls.io/github/rm-hull/luma.oled?branch=master

.. image:: https://img.shields.io/maintenance/yes/2017.svg?maxAge=2592000

.. image:: https://readthedocs.org/projects/luma-oled/badge/?version=latest
   :target: http://luma-oled.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/luma.oled.svg
   :target: https://pypi.python.org/pypi/luma.oled

.. image:: https://img.shields.io/pypi/v/luma.oled.svg
   :target: https://pypi.python.org/pypi/luma.oled

Python library interfacing OLED matrix displays with the SSD1306, SSD1325, SSD1331 or 
SH1106 driver using I2C/SPI on the Raspberry Pi and other linux-based single-board computers - 
it provides a Pillow-compatible drawing canvas, and other functionality to support:

* scrolling/panning capability,
* terminal-style printing,
* state management,
* color/greyscale (where supported),
* dithering to monochrome

A list of tested devices can be found in the
`wiki <https://github.com/rm-hull/luma.oled/wiki/Usage-&-Benchmarking>`_.

The SSD1306 display pictured below is 128 x 64 pixels, and the board is `tiny`,
and will fit neatly inside the RPi case.

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/mounted_display.jpg
   :alt: mounted

As well as display drivers for various physical OLED devices, there are emulators that run in real-time 
(with pygame) and others that can take screenshots, or assemble animated GIFs, as per the examples below (source
code for these is available in the `examples <https://github.com/rm-hull/luma.oled/tree/master/examples>`_ directory:

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/clock_anim.gif?raw=true
   :alt: clock

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/invaders_anim.gif?raw=true
   :alt: invaders

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/crawl_anim.gif?raw=true
   :alt: crawl

Documentation
-------------
Full documentation with installation instructions and examples can be found on
https://ssd1306.readthedocs.io.

License
-------
The MIT License (MIT)

Copyright (c) 2014-17 Richard Hull & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
