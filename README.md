# SSD1306 OLED Driver

Interfacing OLED matrix displays with the SSD1306 driver in Python using
I2C on the Raspberry Pi. The particular kit I bought can be acquired for 
a few pounds from eBay: http://www.ebay.co.uk/itm/191279261331

The display is 128x96 pixels, and the board is _tiny_, and will fit neatly
inside the RPi case. My intention is to solder wires directly to the underside
of the RPi GPIO pins so that the pins are still available for other purposes.

## GPIO pin-outs

The SSD1306 device is an I2C device, so connecting to the RPi is very straightforward:

| Board Pin | Name  | Remarks     | RPi Pin | RPi Function |
|----------:|:------|:------------|--------:|--------------|
| 1         | GND   | Ground      | 6       | GND          |
| 2         | VCC   | +3.3V Power | 1       | 3V3          |
| 3         | SCL   | Clock       | 5       | GPIO 3 (SCL) |
| 4         | SDA   | Data        | 3       | GPIO 2 (SDA) |

![GPIO_header](https://raw.githubusercontent.com/rm-hull/ssd1306/master/doc/tech-spec/images/GPIOs.png) [Attribution: http://elinux.org/Rpi_Low-level_peripherals]

## Pre-requisites

This was tested with Raspian on a rev.2 model B, with a vanilla kernel version 3.12.28+. 
Ensure that the I2C kernel driver is enabled:

    $ dmesg | grep i2c
    [   19.310456] bcm2708_i2c_init_pinmode(1,2)
    [   19.323643] bcm2708_i2c_init_pinmode(1,3)
    [   19.333772] bcm2708_i2c bcm2708_i2c.1: BSC1 Controller at 0x20804000 (irq 79) (baudrate 100000)
    [   19.501285] i2c /dev entries driver

or

    $ lsmod | grep i2c
    i2c_dev                 5769  0 
    i2c_bcm2708             4943  0 
    regmap_i2c              1661  3 snd_soc_pcm512x,snd_soc_wm8804,snd_soc_core

If you dont see the I2C drivers, alter */etc/modules* and add the following 
two lines and reboot:

    i2c-bcm2708
    i2c-dev

And that the device is communicating properly (if using a rev.1 board, 
use 0 for the bus not 1):

    $ i2cdetect -y 1
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- UU 3c -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --

According to the manual, "UU" means that probing was skipped, 
because the address was in use by a driver. It suggest that
there is a chip at that address. Indeed the documentation for
the device indicates it uses two addresses.

# References

* https://learn.adafruit.com/monochrome-oled-breakouts
* https://github.com/adafruit/Adafruit_Python_SSD1306

# License

The MIT License (MIT)

Copyright (c) 2014 Richard Hull

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
