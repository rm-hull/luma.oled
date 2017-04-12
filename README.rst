`luma.core <https://github.com/rm-hull/luma.core>`__ **|** 
`luma.docs <https://github.com/rm-hull/luma.docs>`__ **|** 
`luma.emulator <https://github.com/rm-hull/luma.emulator>`__ **|** 
`luma.examples <https://github.com/rm-hull/luma.examples>`__ **|** 
`luma.lcd <https://github.com/rm-hull/luma.lcd>`__ **|** 
`luma.led_matrix <https://github.com/rm-hull/luma.led_matrix>`__ **|** 
luma.oled

Luma.OLED
---------
**Display drivers for SSD1306 / SSD1322 / SSD1325 / SSD1331 / SH1106**

.. image:: https://travis-ci.org/rm-hull/luma.oled.svg?branch=master
   :target: https://travis-ci.org/rm-hull/luma.oled

.. image:: https://coveralls.io/repos/github/rm-hull/luma.oled/badge.svg?branch=master
   :target: https://coveralls.io/github/rm-hull/luma.oled?branch=master

.. image:: https://readthedocs.org/projects/luma-oled/badge/?version=latest
   :target: http://luma-oled.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/pyversions/luma.oled.svg
   :target: https://pypi.python.org/pypi/luma.oled

.. image:: https://img.shields.io/pypi/v/luma.oled.svg
   :target: https://pypi.python.org/pypi/luma.oled

.. image:: https://img.shields.io/maintenance/yes/2017.svg?maxAge=2592000

Python library interfacing OLED matrix displays with the SSD1306, SSD1322,
SSD1325, SSD1331 or SH1106 driver using I2C/SPI on the Raspberry Pi and other
linux-based single-board computers - it provides a Pillow-compatible drawing
canvas, and other functionality to support:

* scrolling/panning capability,
* terminal-style printing,
* state management,
* color/greyscale (where supported),
* dithering to monochrome

Documentation
-------------
Full documentation with installation instructions and examples can be found on
https://luma-oled.readthedocs.io.

A list of tested devices can be found in the
`wiki <https://github.com/rm-hull/luma.oled/wiki/Usage-&-Benchmarking>`_.

The SSD1306 display pictured below is 128 x 64 pixels, and the board is `tiny`,
and will fit neatly inside the RPi case.

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/mounted_display.jpg
   :alt: mounted

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/ssd1322.jpg
   :alt: ssd1322

As well as display drivers for various physical OLED devices, there are
emulators that run in real-time (with pygame) and others that can take
screenshots, or assemble animated GIFs, as per the examples below (source code
for these is available in the `luma.examples <https://github.com/rm-hull/luma.examples>`_ 
git repository:

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/clock_anim.gif?raw=true
   :alt: clock

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/invaders_anim.gif?raw=true
   :alt: invaders

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/crawl_anim.gif?raw=true
   :alt: crawl

Breaking changes
----------------
Version 2.0.0 was released on 11 January 2017: this came with a rename of the
github project from **ssd1306** to **luma.oled** to reflect the changing nature
of the codebase.

Some core functionality has been moved out to another git repository,
`luma.core <https://github.com/rm-hull/luma.core>`_: this has enabled
another project to have a facelift: **pcd8544** has now been reborn as
`luma.lcd <https://github.com/rm-hull/luma.lcd>`_: the same API can now be
used across both projects. Likewise **max7219** has been renamed to
`luma.led_matrix <https://github.com/rm-hull/luma.led_matrix>`_ so
it can also take advantage of the common API.

The consequence is that any existing code that uses the old **ssd1306** package
will need to be updated. The changes should be limited to altering import
statements only, and are described in the 
`API documentation <https://luma-oled.readthedocs.io/en/latest/api-documentation.html>`_.

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
