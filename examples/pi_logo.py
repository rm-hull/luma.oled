#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

import os.path
from demo_opts import device
from PIL import Image


def main():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'images', 'pi_logo.png'))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)

    background = Image.new("RGBA", device.size, "white")
    posn = ((device.width - logo.width) // 2, 0)

    while True:
        for angle in range(0, 360, 2):
            rot = logo.rotate(angle, resample=Image.BILINEAR)
            img = Image.composite(rot, fff, rot)
            background.paste(img, posn)
            device.display(background.convert(device.mode))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
