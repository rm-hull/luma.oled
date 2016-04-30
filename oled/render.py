#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2015 Richard Hull
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Example usage:
#
#   from oled.device import ssd1306, sh1106
#   from oled.render import canvas
#   from PIL import ImageFont, ImageDraw
#
#   font = ImageFont.load_default()
#   device = sh1106(port=1, address=0x3C)
#
#   with canvas(device) as draw:
#      draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
#      draw.text(30, 40, "Hello World", font=font, fill=255)
#
# As soon as the with-block scope level is complete, the graphics primitives
# will be flushed to the device.
#
# Creating a new canvas is effectively 'carte blanche': If you want to retain
# an existing canvas, then make a reference like:
#
#    c = canvas(device)
#    for X in ...:
#        with c as draw:
#            draw.rectangle(...)
#
# As before, as soon as the with block completes, the canvas buffer is flushed
# to the device

from PIL import Image, ImageDraw


class canvas(object):
    """
    A canvas returns a properly-sized `ImageDraw` object onto which the caller
    can draw upon. As soon as the with-block completes, the resultant image is
    flushed onto the device.
    """
    def __init__(self, device):
        self.draw = None
        self.image = Image.new('1', (device.width, device.height))
        self.device = device

    def __enter__(self):
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def __exit__(self, type, value, traceback):
        if type is None:
            # do the drawing onto the device
            self.device.display(self.image)

        del self.draw   # Tidy up the resources
        return False    # Never suppress exceptions
