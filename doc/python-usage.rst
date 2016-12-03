Python usage
------------
The screen can be driven with python using the ``oled/device.py`` script.
There are two device classes and usage is very simple if you have ever
used `Pillow <https://pillow.readthedocs.io/en/latest/>`_ or PIL.

First, import and initialise the device:

.. code:: python

  from oled.serial import i2c
  from oled.device import ssd1306, sh1106
  from oled.render import canvas
  from PIL import ImageFont, ImageDraw

  # rev.1 users set port=0
  serial = i2c(port=1, address=0x3C)

  # substitute sh1106(...) below if using that device
  device = ssd1306(serial)

The display device should now be configured for use. The specific ``ssd1306`` or
``sh1106`` classes both expose a ``display()`` method which takes a 1-bit depth image.
However, for most cases, for drawing text and graphics primitives, the canvas class
should be used as follows:

.. code:: python

  with canvas(device) as draw:
      font = ImageFont.load_default()
      draw.rectangle((0, 0, device.width, device.height), outline="white", fill="black")
      draw.text((30, 40), "Hello World", font=font, fill="white")

The :class:`oled.render.canvas` class automatically creates an :mod:`PIL.ImageDraw`
object of the correct dimensions and bit depth suitable for the device, so you
may then call the usual Pillow methods to draw onto the canvas.

As soon as the with scope is ended, the resultant image is automatically
flushed to the device's display memory and the :mod:`PIL.ImageDraw` object is
garbage collected.

.. note::
   Any of the standard :mod:`PIL.ImageColor` color formats may be used, but since
   the OLED is monochrome, only the HTML color names ``"black"`` and ``"white"`` 
   values should really be used. 

Examples
^^^^^^^^
After installing the library, enter the ``examples`` directory and try running
the following examples:

============ ========================================================
Example      Description
============ ========================================================
bounce.py    Display a bouncing ball animation and frames per second
clock.py     An analog clockface with date & time
demo.py      Use misc draw commands to create a simple image
invaders.py  Space Invaders demo
maze.py      Maze generator
perfloop.py  Simpel benchmarking utility to measure performance
pi_logo.py   Display the Raspberry Pi logo (loads image as .png)
sys_info.py  Display system information (as shown in the image above)
============ ========================================================

By default, all the examples will asume I2C port 1, address ``0x3C`` and the
``ssd1306`` driver.  If you need to use a different setting, these can be
specified on the command line - each program can be invoked with a ``--help``
flag to show the options::

    $ python pi_logo.py -h
    usage: pi_logo.py [-h] [--display DISPLAY] [--interface INTERFACE]
                      [--i2c-port I2C_PORT] [--i2c-address I2C_ADDRESS]
                      [--spi-port SPI_PORT] [--spi-device SPI_DEVICE]
                      [--spi-bus-speed SPI_BUS_SPEED]
                      [--bcm-data-command BCM_DATA_COMMAND]
                      [--bcm-reset BCM_RESET] [--transform TRANSFORM]
                      [--scale SCALE]

    oled arguments

    optional arguments:
    -h, --help            show this help message and exit
    --display DISPLAY, -d DISPLAY
                          display type, one of: ssd1306, sh1106, capture, pygame
    --interface INTERFACE, -i INTERFACE
                          serial interface type, one of: i2c, spi
    --i2c-port I2C_PORT   I2C bus number
    --i2c-address I2C_ADDRESS
                          I2C display address
    --spi-port SPI_PORT   SPI port number
    --spi-device SPI_DEVICE
                          SPI device
    --spi-bus-speed SPI_BUS_SPEED
                          SPI max bus speed (Hz)
    --bcm-data-command BCM_DATA_COMMAND
                          BCM pin for D/C RESET (SPI devices only)
    --bcm-reset BCM_RESET
                          BCM pin for RESET (SPI devices only)
    --transform TRANSFORM
                          Scaling transform to apply, one of: none, scale,
                          scale2x, smoothscale (emulator only)
    --scale SCALE         Scaling factor to apply (emulator only)

.. note::
   #. Substitute ``python3`` for ``python`` in the above examples if you are using python3.
   #. ``python-dev`` (apt-get) and ``psutil`` (pip/pip3) are required to run the ``sys_info.py`` 
      example. See `install instructions <https://github.com/rm-hull/ssd1306/blob/master/examples/sys_info.py#L3-L7>`_ for the exact commands to use.

Emulators
^^^^^^^^^
There are two display emulators available for running code against, for debugging
and screen capture functionality:

* The :class:`oled.device.capture` device will persist a numbered PNG file to
  disk every time its ``display`` method is called.

* The :class:`oled.device.pygame` device uses the :py:mod:`pygame` library to
  render the displayed image to a pygame display surface. Note however that
  pygame is NOT installed as a dependency, and so must be manually installed
  before using this device.

Invoke the demos with::

  $ python examples/clock.py -d capture

or::

  $ python examples/clock.py -d pygame
