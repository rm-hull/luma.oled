Python usage
============
OLED displays can be driven with python using the various implementations in the
:py:mod:`luma.oled.device` package.  There are several device classes available
and usage is very simple if you have ever used `Pillow
<https://pillow.readthedocs.io/en/latest/>`_ or PIL.

To begin you must import the device class you will be using and the interface
class that you will use to communicate with your device:

In this example, we are using an I2C interface with a ssd1306 display.

.. code:: python

  from luma.core.interface.serial import i2c, spi, pcf8574
  from luma.core.interface.parallel import bitbang_6800
  from luma.core.render import canvas
  from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010

  # rev.1 users set port=0
  # substitute spi(device=0, port=0) below if using that interface
  # substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
  serial = i2c(port=1, address=0x3C)

  # substitute ssd1331(...) or sh1106(...) below if using that device
  device = ssd1306(serial)

The display device should now be configured for use.

The device classes all expose a ``display()`` method which takes an image with
attributes consistent with the capabilities of the device. However, for most
cases when drawing text and graphics primitives, the canvas class should be used
as follows:

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

.. note::
  When a program ends, the display is automatically cleared. This means that a
  fast program that ends quickly may never display a visible image.

Color Model
-----------
Any of the standard :mod:`PIL.ImageColor` color formats may be used, but since
the SSD1306, SH1106, SH1107 and WS0010 OLEDs are monochrome, only the HTML color names
``"black"`` and ``"white"`` values should really be used; in fact, by default,
any value *other* than black is treated as white. The :py:class:`luma.core.render.canvas`
object does have a ``dither`` flag which if set to ``True``, will convert color drawings
to a dithered monochrome effect (see the *3d_box.py* example, below).

.. code:: python

  with canvas(device, dither=True) as draw:
      draw.rectangle((10, 10, 30, 30), outline="white", fill="red")

There is no such constraint on the SSD1331 or SSD1351 OLEDs, which features
16-bit RGB colors: 24-bit RGB images are downsized to 16-bit using a 565 scheme.

The SSD1322, SSD1325 and SSD1362 OLEDs all support 16 greyscale graduations:
24-bit RGB images are downsized to 4-bit using a Luma conversion which is
approximately calculated as follows:

.. code::

    Y' = 0.299 R' + 0.587 G' + 0.114 B'

Landscape / Portrait Orientation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default the display will be oriented in landscape mode (128x64 pixels for
the SSD1306, for example). Should you have an application that requires the
display to be mounted in a portrait aspect, then add a ``rotate=N`` parameter
when creating the device:

.. code:: python

  from luma.core.interface.serial import i2c
  from luma.core.render import canvas
  from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
  from time import sleep

  serial = i2c(port=1, address=0x3C)
  device = ssd1306(serial, rotate=1)

  # Box and text rendered in portrait mode
  with canvas(device) as draw:
      draw.rectangle(device.bounding_box, outline="white", fill="black")
      draw.text((10, 40), "Hello World", fill="white")
  sleep(10)

*N* should be a value of 0, 1, 2 or 3 only, where 0 is no rotation, 1 is
rotate 90° clockwise, 2 is 180° rotation and 3 represents 270° rotation.

The ``device.size``, ``device.width`` and ``device.height`` properties reflect
the rotated dimensions rather than the physical dimensions.

Examples
^^^^^^^^
After installing the library see the `luma.examples <https://github.com/rm-hull/luma.examples>`_
repository. Details of how to run the examples is shown in the example repo's README.
