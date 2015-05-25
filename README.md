# SSD1306 / SH1106 OLED Driver

Interfacing OLED matrix displays with the SSD1306 or SH1106 driver in Python
using I2C or 4-wire SPI on the Raspberry Pi.

These displays are available for a few pounds from eBay. The I2C interface has
been tested with
[this display](http://www.ebay.co.uk/itm/191279261331)
and the SPI interface has been tested with
[this display](http://www.ebay.com/itm/281648238188)
.

Technical details for the supported OLED displays can be found in the datasheets
for the
[SSD1306](/doc/tech-spec/SSD1306.pdf?raw=true)
and
[SH1106](/doc/tech-spec/SH1106.pdf)
OLED controllers.

These 128x64 pixel OLED displays are tiny and fit neatly inside a transparent
RPi case:

![I2C OLED](/doc/display_inside_i2c.jpg?raw=true)

Or fastened with double sided tape on the outside:

![SPI OLED](/doc/display_outside_spi.jpg?raw=true)


## Identifying your serial interface

You can determine if you have an I2C or a SPI interface by counting the number
of pins on your card. An I2C display will have 4 pins while an SPI interface
will have 6 or 7 pins.

If you have a SPI display, check the back of your display for a configuration
such as this:

![SPI configuration table](/doc/serial_config.jpg?raw=true)

For this display, the two 0 ohm (jumper) resistors have been connected to "0"
and the table shows that "0 0" is 4-wire SPI. That is the type of connection
that is currently supported by the SPI mode of this library.

3-wire SPI eliminates the separate Data/Command line by sending an extra bit
with each byte, which causes a small amount of overhead. Supporting 3-wire SPI
would be trivial but has not been implemented yet (no devices to test with).

## I2C

How to connect a I2C serial interface display.

### GPIO pin-outs

The SSD1306 device is an I2C device, so connecting to the RPi is very
straightforward:

#### P1 Header

For prototyping, the P1 header pins should be connected as follows:

| Board Pin | Name  | Remarks     | RPi Pin | RPi Function | Colour |
|----------:|:------|:------------|--------:|--------------|--------|
| 1         | GND   | Ground      | P01-6   | GND          | Black  |
| 2         | VCC   | +3.3V Power | P01-1   | 3V3          | White  |
| 3         | SCL   | Clock       | P01-5   | GPIO 3 (SCL) | Purple |
| 4         | SDA   | Data        | P01-3   | GPIO 2 (SDA) | Grey   |

![GPIOS](/doc/GPIOs.png?raw=true)

[Attribution: http://elinux.org/Rpi_Low-level_peripherals]

#### P5 Header

On rev.2 RPi's, right next to the male pins of the P1 header, there is a bare P5
header which features I2C channel 0, although this doesn't appear to be
initially enabled and may be configured for use with the Camera module. 

| Board Pin | Name  | Remarks     | RPi Pin | RPi Function  | Colour |
|----------:|:------|:------------|--------:|---------------|--------|
| 1         | GND   | Ground      | P5-07   | GND           | Black  |
| 2         | VCC   | +3.3V Power | P5-02   | 3V3           | White  |
| 3         | SCL   | Clock       | P5-04   | GPIO 29 (SCL) | Purple |
| 4         | SDA   | Data        | P5-03   | GPIO 28 (SDA) | Grey   |

![P5 Header](/doc/RPi_P5_header.png?raw=true)

[Attribution: http://elinux.org/Rpi_Low-level_peripherals]

### Pre-requisites

This was tested with Raspian on a rev.2 model B, with a vanilla kernel version
3.12.28+. Ensure that the I2C kernel driver is enabled:

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

If you dont see the I2C drivers, alter */etc/modules* and add the following two
lines:

    i2c-bcm2708
    i2c-dev

And alter */etc/modprobe.d/raspi-blacklist.conf* and comment out the line:

   blacklist i2c-bcm2708

Then reboot.

Then add your user to the i2c group:

    $ sudo adduser pi i2c

Install some packages:

    $ sudo apt-get install i2c-tools python-smbus python-pip
    $ sudo pip install pillow

Next check that the device is communicating properly (if using a rev.1 board,
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

According to the manual, "UU" means that probing was skipped, because the
address was in use by a driver. It suggest that there is a chip at that address.
Indeed the documentation for the device indicates it uses two addresses.

# Installing the Python Package

From the bash prompt, enter:

    $ sudo python setup.py install

This will install the python files in `/usr/local/lib/python2.7` making them
ready for use in other programs.

## SPI

How to connect a 4-wire SPI serial interface display.

### Wiring

The GPIO pins used for this SPI connection are the same for all versions of the
Raspberry Pi, up to and including the Raspberry Pi 2 B.

| OLED Pin  | Name  | Remarks     | RPi Pin | RPi Function |
|----------:|:------|:------------|--------:|--------------|
| 1         | VCC   | +3.3V Power | P01-17  | 3V3          |
| 2         | GND   | Ground      | P01-20  | GND          |
| 3         | D0    | Clock       | P01-23  | GPIO 11      |
| 4         | D1    | MOSI        | P01-19  | GPIO 10      |
| 5         | RST   | Reset       | P01-22  | GPIO 25      |
| 6         | DC    | Data/Command| P01-18  | GPIO 24      |
| 7         | CS    | Chip Select | P01-24  | GPIO 8 (CE0) |

Notes:

* When using the 4-wire SPI connection, Data/Command is an "out of band" signal
  that tells the controller if you're sending commands or display data. With
  3-wire SPI and I2C, the signal is sent "in band". If you're already using the
  listed GPIO pin, you can select another and just pass an
  `gpio_command_data_select` argument specifying the new pin number in your
  serial interface create call.
  
* Because CS is connected to CE0, the display is available on SPI port 0. You
  can connect it to CE1 to have it available on port 1. If so, pass `port=1` in
  your serial interface create call.

* The Reset connection is not strictly necessary. It's useful if the display
  gets into an undefined state. Without Reset connected, you'll have to
  disconnect and reconnect the Raspberry Pi power if it becomes necessary to
  reset the display.

### Setup

Enable the SPI port:

    $ sudo raspi-config
    > Advanced Options > A6 SPI

If raspi-config is not available, this can be done manually. Search the web.

Install dependencies:

    $ sudo pip install wiringpi2

# Software Display Driver

The screen can be driven with python using the _oled/device.py_ script. There
are two device classes and usage is very simple if you have ever used
[Pillow](http://pillow.readthedocs.org/en/latest/) or PIL.

First, import and initialise the device:

```python
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont, ImageDraw

# substitute sh1106(...) below if using that device
device = ssd1306(port=1, address=0x3C)  # rev.1 users set port=0
```

The display device should now be configured for use. The specific `ssd1306` or 
`sh1106` classes both expose a `display()` method which takes a 1-bit depth image. 
However, for most cases, for drawing text and graphics primitives, the canvas class
should be used as follows:

```python
with canvas(device) as draw:
    font = ImageFont.load_default()
    draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
    draw.text(30, 40, "Hello World", font=font, fill=255)
```

The `canvas` class automatically creates an [ImageDraw](http://pillow.readthedocs.org/en/latest/reference/ImageDraw.html) 
object of the correct dimensions and bit depth suitable for the device, so you
may then call the usual Pillow methods to draw onto the canvas.

As soon as the with scope is ended, the resultant image is automatically
flushed to the device's display memory and the ImageDraw object is
garbage collected.

## Examples
    
After installing the library, enter the `examples` directory and edit the
examples to select your serial interface and controller chip type and
parameters, then run them.

| bounce.py        | Display a bouncing ball animation and frames per second  |
| draw_commands.py | Use misc draw commands to create a simple image          |
| sys_info.py      | Display system information (as shown in the image above) |
| pi_logo.py       | Display an image of the Raspberry Pi logo                |
| maze.py          | Display a maze                                           |

# References

* https://learn.adafruit.com/monochrome-oled-breakouts
* https://github.com/adafruit/Adafruit_Python_SSD1306
* http://www.dafont.com/bitmap.php
* http://raspberrypi.znix.com/hipidocs/topic_i2cbus_2.htm
* http://martin-jones.com/2013/08/20/how-to-get-the-second-raspberry-pi-i2c-bus-to-work/

# License

The MIT License (MIT)

Copyright (c) 2015 Richard Hull

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
