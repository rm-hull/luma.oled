# SH1106 / SSD1306 OLED Driver (only tested with SH1106).

I forked the original and made some minor changes, to make it work with a BPi-M1.

Interfacing OLED matrix displays with the SH1106 (or SSD1306) driver in Python using
I2C on the Banana Pi. The particular kit I bought from Amazon: <a href="http://www.amazon.de/SainSmart-Serial-128X64-Module-Arduino/dp/B00MQK264K?ie=UTF8&psc=1&redirect=true&ref_=oh_aui_detailpage_o09_s00">SainSmart 1.3" I2C IIC Serial 128X64 OLED</a>.

The SH1106 display is 128x64 pixels, and the board is _tiny_, and will fit neatly
inside my BPi Case.

<img src="http://blog.gizu.de/content/images/2016/03/vorne.JPG">

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
two lines:

    i2c-bcm2708
    i2c-dev

And alter */etc/modprobe.d/raspi-blacklist.conf* and comment out the line:

   blacklist i2c-bcm2708

Increase the I2C baudrate from the default of 100KHz to 400KHz by altering
*/boot/config.txt* to include:

    dtparam=i2c_arm=on,i2c_baudrate=400000

Then reboot.

Then add your user to the i2c group:

    $ sudo adduser pi i2c

Install some packages:

    $ sudo apt-get install i2c-tools python-smbus python-pip
    $ sudo pip install pillow

Next check that the device is communicating properly (if using a rev.1 board, 
use 0 for the bus not 1. For the Banana Pi use 2):

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

# Installing the Python Package

From the bash prompt, enter:

    $ sudo python setup.py install

This will install the python files in `/usr/local/lib/python2.7`
making them ready for use in other programs.

# Software Display Driver

The screen can be driven with python using the _oled/device.py_ script.
There are two device classes and usage is very simple if you have ever
used [Pillow](http://pillow.readthedocs.org/en/latest/) or PIL.

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

Run the demos in the example directory:

    $ python examples/demo.py
    $ python examples/sys_info.py
    $ python examples/pi_logo.py
    $ python examples/maze.py

Note that `python-dev` (apt-get) and `psutil` (pip) are required to run the `sys_info.py`
example. See [install instructions](https://github.com/rm-hull/ssd1306/blob/master/examples/sys_info.py#L3-L7)
for the exact commands to use.

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
