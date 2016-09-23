#!/usr/bin/env python

from demo_opts import device
from oled.render import canvas
from PIL import Image


with canvas(device) as draw:
    logo = Image.open('examples/images/pi_logo.png')
    draw.bitmap((32, 0), logo, fill=1)
