SSD1306 / SH1106 OLED Driver
============================
.. image:: https://travis-ci.org/rm-hull/ssd1306.svg?branch=master
   :target: https://travis-ci.org/rm-hull/ssd1306

.. image:: https://coveralls.io/repos/github/rm-hull/ssd1306/badge.svg?branch=master
   :target: https://coveralls.io/github/rm-hull/ssd1306?branch=master

.. image:: https://img.shields.io/maintenance/yes/2016.svg?maxAge=2592000

.. image:: https://img.shields.io/pypi/v/ssd1306.svg
   :target: https://pypi.python.org/pypi/ssd1306

Python library interfacing OLED matrix displays with the SSD1306 (or SH1106) driver using
I2C/SPI on the Raspberry Pi.

Further technical details for the SSD1306 OLED display can be found in the
`datasheet <https://raw.githubusercontent.com/rm-hull/ssd1306/master/doc/tech-spec/SSD1306.pdf>`_.
See also the datasheet for the
`SH1106 chipset <https://raw.githubusercontent.com/rm-hull/ssd1306/sh1106-compat/doc/tech-spec/SH1106.pdf>`_.
A list of tested devices can be found in the
`wiki <https://github.com/rm-hull/ssd1306/wiki/Usage-&-Benchmarking>`_.

The SSD1306 display pictured below is 128 x 64 pixels, and the board is `tiny`,
and will fit neatly inside the RPi case (the SH1106 is slightly different, in
that it supports 132 x 64 pixels).

.. image:: https://raw.githubusercontent.com/rm-hull/ssd1306/master/doc/images/mounted_display.jpg
   :alt: mounted

As well as display drivers for SSD1306- and SH1106-class OLED devices there are
emulators that run in real-time (with pygame) and others that can take screenshots,
or assemble animated GIFs, as per the examples below (source code for these is 
available in the `examples <https://github.com/rm-hull/ssd1306/tree/master/examples>`_ directory:

.. image:: https://raw.githubusercontent.com/rm-hull/ssd1306/master/doc/images/clock_anim.gif
   :alt: clock

.. image:: https://raw.githubusercontent.com/rm-hull/ssd1306/master/doc/images/invaders_anim.gif
   :alt: invaders

Documentation
-------------
Full documentation with installation instructions and examples can be found on
https://ssd1306.readthedocs.io.

License
-------
The MIT License (MIT)

Copyright (c) 2016 Richard Hull

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
