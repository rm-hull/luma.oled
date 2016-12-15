#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

import time
import os.path
from demo_opts import device
from oled.render import canvas
from PIL import Image


with canvas(device) as draw:
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'pi_logo.png'))
    logo = Image.open(img_path)
    draw.bitmap((32, 0), logo, fill="white")

try:
    time.sleep(5)
except KeyboardInterrupt:
    pass
