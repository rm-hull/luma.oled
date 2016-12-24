Introduction
------------
Interfacing `OLED matrix displays
<https://github.com/rm-hull/ssd1306/wiki/Usage-&-Benchmarking>`_ with the
SSD1306, SSD1331 or SH1106 driver in Python 2 or 3 using I2C/SPI on the
Raspberry Pi.

The SSD1306 display pictured below is 128 x 64 pixels, and the board is `tiny`,
and will fit neatly inside the RPi case (the SH1106 is slightly different, in
that it supports 132 x 64 pixels). My intention is to solder the wires directly
to the underside of the RPi GPIO pins (P5 header) so that the pins are still
available for other purposes, but the regular, top GPIO pins (P1 header) can
also be used of course.

.. image:: images/mounted_display.jpg
   :alt: mounted

.. seealso::
   Further technical information for the specific devices can be found in the
   datasheet: :download:`SSD1306 <tech-spec/SSD1306.pdf>`,
   :download:`SSD1325 <tech-spec/SSD1325.pdf>`,
   :download:`SSD1331 <tech-spec/SSD1331.pdf>` or
   :download:`SH1106 <tech-spec/SH1106.pdf>`

   Benchmarks for tested devices can be found in the
   `wiki <https://github.com/rm-hull/ssd1306/wiki/Usage-&-Benchmarking>`_.

As well as display drivers for SSD1306-, SSD1331- and SH1106-class OLED devices
there are emulators that run in real-time (with pygame) and others that can
take screenshots, or assemble animated GIFs, as per the examples below (source
code for these is available in the `examples <https://github.com/rm-hull/ssd1306/tree/master/examples>`_ directory:

.. image:: images/clock_anim.gif
   :alt: clock

.. image:: images/invaders_anim.gif
   :alt: invaders

.. image:: images/crawl_anim.gif
   :alt: crawl
