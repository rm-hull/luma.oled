Introduction
------------
Interfacing OLED matrix displays with the SSD1306 (or SH1106) driver in Python 2 or 3 using
I2C on the Raspberry Pi. The particular kit I bought can be acquired for
a few pounds from `eBay <http://www.ebay.co.uk/itm/191279261331>`_. Further
technical details for the SSD1306 OLED display can be found in the
:download:`datasheet <tech-spec/SSD1306.pdf>`.
See also the datasheet for the :download:`SH1106 chipset <tech-spec/SH1106.pdf>`.

The SSD1306 display pictured below is 128x64 pixels, and the board is `tiny`, and will fit neatly
inside the RPi case (the SH1106 is slightly different, in that it supports 132 x 64
pixels). My intention is to solder the wires directly to the underside
of the RPi GPIO pins (P5 header) so that the pins are still available for other purposes, but
the regular, top GPIO pins (P1 header) can also be used of course.

.. image:: images/mounted_display.jpg
   :alt: mounted
