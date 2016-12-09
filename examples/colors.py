#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import time
import random
import os.path
from demo_opts import device
from oled.render import canvas
from PIL import Image


def main():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'balloon.png'))
    balloon = Image.open(img_path).convert("RGB")
    while True:
        # Image display
        device.display(balloon)
        time.sleep(5)

        # Cycle through some primary colours
        for color in ["black", "white", "red", "orange", "yellow", "green", "blue", "indigo", "violet"]:
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, fill=color)
                size = draw.textsize(color)
                left = (device.width - size[0]) / 2
                top = (device.height - size[1]) / 2
                right = left + size[0]
                bottom = top + size[1]
                draw.rectangle((left - 1, top, right, bottom), fill="black")
                draw.text((left, top), text=color, fill="white")

            time.sleep(3)

        # Rainbow
        w = 4
        with canvas(device) as draw:
            for i in range(device.width / w):
                r = int(math.sin(0.3 * i + 0) * 127) + 128
                g = int(math.sin(0.3 * i + 2) * 127) + 128
                b = int(math.sin(0.3 * i + 4) * 127) + 128
                rgb = (r << 16) | (g << 8) | b
                draw.rectangle((i * w, 0, (i + 1) * w, device.height), fill=rgb)
        time.sleep(5)

        # Random blocks
        w = device.width / 12
        h = device.height / 8
        for _ in range(40):
            with canvas(device) as draw:
                for x in range(12):
                    for y in range(8):
                        color = random.randint(0, 2 ** 24)
                        left = x * w
                        right = (x + 1) * w
                        top = y * h
                        bottom = (y + 1) * h
                        draw.rectangle((left, top, right - 2, bottom - 2), fill=color)

                time.sleep(0.25)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
