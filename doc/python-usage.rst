Python usage
------------
The screen can be driven with python using the ``oled/device.py`` script.
There are two device classes and usage is very simple if you have ever
used `Pillow <https://pillow.readthedocs.io/en/latest/>`_ or PIL.

First, import and initialise the device:

.. code:: python

  from oled.device import ssd1306, sh1106
  from oled.render import canvas
  from PIL import ImageFont, ImageDraw

  # substitute sh1106(...) below if using that device
  device = ssd1306(port=1, address=0x3C)  # rev.1 users set port=0

The display device should now be configured for use. The specific ``ssd1306`` or
``sh1106`` classes both expose a ``display()`` method which takes a 1-bit depth image.
However, for most cases, for drawing text and graphics primitives, the canvas class
should be used as follows:

.. code:: python

  with canvas(device) as draw:
      font = ImageFont.load_default()
      draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
      draw.text((30, 40), "Hello World", font=font, fill=255)

The ``canvas`` class automatically creates an :mod:`PIL.ImageDraw`
object of the correct dimensions and bit depth suitable for the device, so you
may then call the usual Pillow methods to draw onto the canvas.

As soon as the with scope is ended, the resultant image is automatically
flushed to the device's display memory and the :mod:`PIL.ImageDraw` object is
garbage collected.

Examples
^^^^^^^^
After installing the library, enter the ``examples`` directory and try running
the following examples:

=========== ========================================================
Example     Description
=========== ========================================================
demo.py     Use misc draw commands to create a simple image
bounce.py   Display a bouncing ball animation and frames per second
sys_info.py Display system information (as shown in the image above)
pi_logo.py  Display the Raspberry Pi logo (loads image as .png)
maze.py     Display a maze
=========== ========================================================

By default it will use port 1, address ``0x3C`` and the ``ssd1306`` driver.
If you need to use a different port, these can be specified on the command
line - each program can be invoked with a ``--help`` flag to show the options::

  $ python demo.py --help
  usage: demo.py [-h] [--port PORT] [--address ADDRESS] [--display DISPLAY]

  oled arguments

  optional arguments:
    -h, --help            show this help message and exit
    --port PORT, -p PORT  i2c bus number
    --address ADDRESS, -a ADDRESS
                          i2c display address
    --display DISPLAY, -d DISPLAY
                          display type, one of ssd1306 or sh1106

.. note::
   #. Substitute ``python3`` for ``python`` in the above examples if you are using python3.
   #. ``python-dev`` (apt-get) and ``psutil`` (pip/pip3) are required to run the ``sys_info.py`` example. See `install instructions <https://github.com/rm-hull/ssd1306/blob/master/examples/sys_info.py#L3-L7>`_ for the exact commands to use.
