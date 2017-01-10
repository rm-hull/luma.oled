Python usage
------------
The screen can be driven with python using the ``oled/device.py`` script.
There are two device classes and usage is very simple if you have ever
used `Pillow <https://pillow.readthedocs.io/en/latest/>`_ or PIL.

First, import and initialise the device:

.. code:: python

  from luma.core.serial import i2c
  from luma.core.render import canvas
  from oled.device import ssd1306, ssd1331, sh1106

  # rev.1 users set port=0
  # substitute spi(device=0, port=0) below if using that interface
  serial = i2c(port=1, address=0x3C)

  # substitute ssd1331(...) or sh1106(...) below if using that device
  device = ssd1306(serial)

The display device should now be configured for use. The specific ``ssd1306``,
``ssd1331`` or ``sh1106`` classes all expose a ``display()`` method which takes
an image with attributes consistent with the capabilities of the device.
However, for most cases, for drawing text and graphics primitives, the canvas
class should be used as follows:

.. code:: python

  with canvas(device) as draw:
      draw.rectangle(device.bounding_box, outline="white", fill="black")
      draw.text((30, 40), "Hello World", fill="white")

The :class:`luma.core.render.canvas` class automatically creates an :mod:`PIL.ImageDraw`
object of the correct dimensions and bit depth suitable for the device, so you
may then call the usual Pillow methods to draw onto the canvas.

As soon as the with scope is ended, the resultant image is automatically
flushed to the device's display memory and the :mod:`PIL.ImageDraw` object is
garbage collected.

Color Model
^^^^^^^^^^^
Any of the standard :mod:`PIL.ImageColor` color formats may be used, but since
the SSD1306 and SH1106 OLEDs are monochrome, only the HTML color names
``"black"`` and ``"white"`` values should really be used; in fact, by default,
any value *other* than black is treated as white. The :py:class:`canvas` object
does have a ``dither`` flag which if set to True, will convert color drawings
to a dithered monochrome effect (see the *3d_box.py* example, below).

.. code:: python

  with canvas(device, dither=True) as draw:
      draw.rectangle((10, 10, 30, 30), outline="white", fill="red")

There is no such constraint on the SSD1331 OLED which features 16-bit RGB
colors: 24-bit RGB images are downsized to 16-bit using a 565 scheme.

The SSD1325 OLED supports 16 greyscale graduations: 24-bit RGB images are
downsized to 4-bit using a Luma conversion which is approximately calculated
as follows:

*Y'=0.299R'+0.587G'+0.114B'*

Landscape / Portrait Orientation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default the display will be oriented in landscape mode (128x64 pixels for
the SSD1306, for example). Should you have an application that requires the
display to be mounted in a portrait aspect, then add a ``rotate=N`` parameter
when creating the device:

.. code:: python

  from luma.core.serial import i2c
  from luma.core.render import canvas
  from luma.oled.device import ssd1306, ssd1331, sh1106

  serial = i2c(port=1, address=0x3C)
  device = ssd1306(serial, rotate=1)

  # Box and text rendered in portrait mode
  with canvas(device) as draw:
      draw.rectangle(device.bounding_box, outline="white", fill="black")
      draw.text((10, 40), "Hello World", fill="white")

*N* should be a value of 0, 1, 2 or 3 only, where 0 is no rotation, 1 is
rotate 90° clockwise, 2 is 180° rotation and 3 represents 270° rotation.

The ``device.size``, ``device.width`` and ``device.height`` properties reflect
the rotated dimensions rather than the physical dimensions.

Examples
^^^^^^^^
After installing the library, enter the ``examples`` directory and try running
the following examples:

=============== ========================================================
Example         Description
=============== ========================================================
3d_box.py       Rotating 3D box wireframe & color dithering
bounce.py       Display a bouncing ball animation and frames per second
carousel.py     Showcase viewport and hotspot functionality
clock.py        An analog clockface with date & time
colors.py       Color rendering demo
crawl.py        A vertical scrolling demo, which should be familiar
demo.py         Use misc draw commands to create a simple image
game_of_life.py Conway's game of life
grayscale.py    Greyscale rendering demo
invaders.py     Space Invaders demo
maze.py         Maze generator
perfloop.py     Simple benchmarking utility to measure performance
pi_logo.py      Display the Raspberry Pi logo (loads image as .png)
savepoint.py    Example of savepoint/restore functionality
starfield.py    3D starfield simulation
sys_info.py     Display basic system information
terminal.py     Simple println capabilities
tv_snow.py      Example image-blitting
welcome.py      Unicode font rendering & scrolling
=============== ========================================================

By default, all the examples will asume I2C port 1, address ``0x3C`` and the
``ssd1306`` driver.  If you need to use a different setting, these can be
specified on the command line - each program can be invoked with a ``--help``
flag to show the options::

    $ python pi_logo.py -h
    usage: pi_logo.py [-h] [--config CONFIG]
                      [--display {ssd1306,ssd1331,sh1106,capture,pygame,gifanim}]
                      [--width WIDTH] [--height HEIGHT] [--rotate {0,1,2,3}]
                      [--interface {i2c,spi}] [--i2c-port I2C_PORT]
                      [--i2c-address I2C_ADDRESS] [--spi-port SPI_PORT]
                      [--spi-device SPI_DEVICE] [--spi-bus-speed SPI_BUS_SPEED]
                      [--bcm-data-command BCM_DATA_COMMAND]
                      [--bcm-reset BCM_RESET]
                      [--transform {none,identity,scale2x,smoothscale}]
                      [--scale SCALE] [--mode {1,RGB,RGBA}] [--duration DURATION]
                      [--loop LOOP] [--max-frames MAX_FRAMES]

    oled arguments

    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG, -f CONFIG
                            Load configuration settings from a file (default:
                            None)
      --display {ssd1306,ssd1331,sh1106,capture,pygame,gifanim}, -d {ssd1306,ssd1331,sh1106,capture,pygame,gifanim}
                            Display type, supports real devices or emulators
                            (default: ssd1306)
      --width WIDTH         Width of the device in pixels (default: 128)
      --height HEIGHT       Height of the device in pixels (default: 64)
      --rotate {0,1,2,3}, -r {0,1,2,3}
                            Rotation factor (default: 0)
      --interface {i2c,spi}, -i {i2c,spi}
                            Serial interface type (default: i2c)
      --i2c-port I2C_PORT   I2C bus number (default: 1)
      --i2c-address I2C_ADDRESS
                            I2C display address (default: 0x3C)
      --spi-port SPI_PORT   SPI port number (default: 0)
      --spi-device SPI_DEVICE
                            SPI device (default: 0)
      --spi-bus-speed SPI_BUS_SPEED
                            SPI max bus speed (Hz) (default: 8000000)
      --bcm-data-command BCM_DATA_COMMAND
                            BCM pin for D/C RESET (SPI devices only) (default: 24)
      --bcm-reset BCM_RESET
                            BCM pin for RESET (SPI devices only) (default: 25)
      --transform {none,identity,scale2x,smoothscale}
                            Scaling transform to apply (emulator only) (default:
                            scale2x)
      --scale SCALE         Scaling factor to apply (emulator only) (default: 2)
      --mode {1,RGB,RGBA}   Colour mode (emulator only) (default: RGB)
      --duration DURATION   Animation frame duration (gifanim emulator only)
                            (default: 0.01)
      --loop LOOP           Repeat loop, zero=forever (gifanim emulator only)
                            (default: 0)
      --max-frames MAX_FRAMES
                            Maximum frames to record (gifanim emulator only)
                            (default: None)
.. note::
   #. Substitute ``python3`` for ``python`` in the above examples if you are using python3.
   #. ``python-dev`` (apt-get) and ``psutil`` (pip/pip3) are required to run the ``sys_info.py`` 
      example. See `install instructions <https://github.com/rm-hull/luma.oled/blob/master/examples/sys_info.py#L3-L7>`_ for the exact commands to use.

Emulators
^^^^^^^^^
There are various display emulators available for running code against, for debugging
and screen capture functionality:

* The :class:`oled.emulator.capture` device will persist a numbered PNG file to
  disk every time its ``display`` method is called.

* The :class:`oled.emulator.gifanim` device will record every image when its ``display``
  method is called, and on program exit (or Ctrl-C), will assemble the images into an
  animated GIF.

* The :class:`oled.emulator.pygame` device uses the :py:mod:`pygame` library to
  render the displayed image to a pygame display surface. 

Invoke the demos with::

  $ python examples/clock.py -d capture

or::

  $ python examples/clock.py -d pygame
  
.. note::
   *Pygame* is required to use any of the emulated devices, but it is **NOT**
   installed as a dependency by default, and so must be manually installed
   before using any of these emulation devices.
