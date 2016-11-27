Installation
------------
.. note:: The library has been tested against Python 2.7 and 3.4. 

   For **Python3** installation, substitute the following in the 
   instructions below.

   * ``pip`` ⇒ ``pip3``, 
   * ``python`` ⇒ ``python3``, 
   * ``python-dev`` ⇒ ``python3-dev``,
   * ``python-pip`` ⇒ ``python3-pip``.

.. note:: This was *originally* tested with Raspian on a rev.2 model
   B, with a vanilla kernel version 4.1.16+. It has subsequently tested
   on Raspberry Pi model A & model B2 (Debian Jessie) and OrangePi Zero 
   (Armbian Jessie). There have been unconfirmed reports of the library
   **not** working on Raspberry Pi model B3.

Pre-requisites
^^^^^^^^^^^^^^
Ensure that the I2C kernel driver is enabled::

  $ dmesg | grep i2c
  [    4.925554] bcm2708_i2c 20804000.i2c: BSC1 Controller at 0x20804000 (irq 79) (baudrate 100000)
  [    4.929325] i2c /dev entries driver

or::

  $ lsmod | grep i2c
  i2c_dev                 5769  0
  i2c_bcm2708             4943  0
  regmap_i2c              1661  3 snd_soc_pcm512x,snd_soc_wm8804,snd_soc_core

If you have no kernel modules listed and nothing is showing using ``dmesg`` then this implies
the kernel I2C driver is not loaded. Enable the I2C as follows:

#. Run ``sudo raspi-config``
#. Use the down arrow to select ``9 Advanced Options``
#. Arrow down to ``A7 I2C``
#. Select **yes** when it asks you to enable I2C
#. Also select **yes** when it asks about automatically loading the kernel module
#. Use the right arrow to select the **<Finish>** button
#. Select **yes** when it asks to reboot

After rebooting re-check that the ``dmesg | grep i2c`` command shows whether
I2C driver is loaded before proceeding.

Optionally, to improve permformance, increase the I2C baudrate from the default
of 100KHz to 400KHz by altering ``/boot/config.txt`` to include::

  dtparam=i2c_arm=on,i2c_baudrate=400000

Then reboot.

Then add your user to the i2c group::

  $ sudo adduser pi i2c

Install some packages (python2)::

  $ sudo apt-get install i2c-tools python-dev python-pip libfreetype6-dev libjpeg8-dev
  $ sudo pip install pillow

or (python3)::

  $ sudo apt-get install i2c-tools python3-dev python3-pip libfreetype6-dev libjpeg8-dev
  $ sudo pip3 install pillow

Next check that the device is communicating properly (if using a rev.1 board,
use 0 for the bus not 1)::

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

GPIO pin-outs
^^^^^^^^^^^^^
The SSD1306 device is an I2C device, so connecting to the RPi is very straightforward:

P1 Header
"""""""""
The P1 header pins should be connected as follows:

========== ====== ============ ======== ============== ========
Board Pin  Name   Remarks      RPi Pin  RPi Function   Colour
---------- ------ ------------ -------- -------------- --------
1          GND    Ground       P01-6    GND            Black
2          VCC    +3.3V Power  P01-1    3V3            White
3          SCL    Clock        P01-5    GPIO 3 (SCL)   Purple
4          SDA    Data         P01-3    GPIO 2 (SDA)   Grey
========== ====== ============ ======== ============== ========

P5 Header
"""""""""
You can also solder the wires directly to the underside of the RPi GPIO pins.

On rev.2 RPi's, right next to the male pins of the P1 header, there is a bare
P5 header which features I2C channel 0, although this doesn't appear to be
initially enabled and may be configured for use with the Camera module.

========== ====== ============ ======== ============== ========
Board Pin  Name   Remarks      RPi Pin  RPi Function   Colour
---------- ------ ------------ -------- -------------- --------
1          GND    Ground       P5-07    GND            Black
2          VCC    +3.3V Power  P5-02    3V3            White
3          SCL    Clock        P5-04    GPIO 29 (SCL)  Purple
4          SDA    Data         P5-03    GPIO 28 (SDA)  Grey
========== ====== ============ ======== ============== ========

Installing from the cheeseshop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note:: This is the preferred installation mechanism.

Install the latest version of the library directly from
`PyPI <https://pypi.python.org/pypi?:action=display&name=ssd1306>`_::

  $ sudo apt-get install python-dev python-pip
  $ sudo pip install --upgrade ssd1306

Installing from source
^^^^^^^^^^^^^^^^^^^^^^
For python2, from the bash prompt, enter::

  $ sudo apt-get install python-dev python-pip
  $ sudo python setup.py install

This will install the Python files in ``/usr/local/lib/python2.7``
making them ready for use in other programs.

Alternatively for python3, type::

  $ sudo apt-get install python3-dev python3-pip
  $ sudo python3 setup.py install
