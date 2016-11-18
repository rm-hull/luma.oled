#!/usr/bin/env python

# Ported from:
# https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py

import time
from PIL import Image, ImageDraw

from demo_opts import device
import demo


class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


def main():
    print("Testing basic canvas graphics...")
    image = Image.new('1', (device.width, device.height))
    draw = ImageDraw.Draw(image)
    demo.primitives(draw)

    for i in range(1000):
        with Timer() as t:
            device.display(image)
        print("{0}: time = {1} s".format(i, t.interval))

    del image


if __name__ == "__main__":
    main()
