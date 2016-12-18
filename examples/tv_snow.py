#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

import struct
import random
from demo_opts import device
from oled.render import canvas
from PIL import Image, ImageDraw

size = (60, 30)
# Calc offset to center text vertically and horizontally
offset = ((device.width - size[0]) // 2, (device.height - size[1]) // 2)
shadow_offset = (offset[0] + 1, offset[1] + 1)


def snow():
    data = [random.randint(0, 0xFFFFFF)
            for _ in range(device.width * device.height)]
    packed = struct.pack('i' * len(data), *data)
    background = Image.frombytes("RGBA", device.size, packed)

    draw = ImageDraw.Draw(background)
    draw.multiline_text(shadow_offset, "Please do\nnot adjust\nyour set", fill="black", align="center", spacing=-1)
    draw.multiline_text(offset, "Please do\nnot adjust\nyour set", fill="white", align="center", spacing=-1)

    return background.convert(device.mode)


def main():
    with canvas(device) as draw:
        draw.multiline_text(offset, "Please do\nnot adjust\nyour set", fill="white", align="center", spacing=-1)

    images = [snow() for _ in range(20)]
    while True:
        random.shuffle(images)
        for background in images:
            device.display(background)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
