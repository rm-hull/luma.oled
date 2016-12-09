#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ported from:
# https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py
import sys
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
    elapsed_time = 0
    count = 0
    print("Testing OLED dislay rendering performance")
    print("Press Ctrl-C to abort test\n")

    image = Image.new('1', (device.width, device.height))
    draw = ImageDraw.Draw(image)
    demo.primitives(draw)

    for i in range(5, 0, -1):
        sys.stdout.write("Starting in {0} seconds...\r".format(i))
        sys.stdout.flush()
        time.sleep(1)

    try:
        while True:
            with Timer() as t:
                device.display(image)

            elapsed_time += t.interval
            count += 1

            if count % 31 == 0:
                avg_transit_time = elapsed_time * 1000 / count
                avg_fps = count / elapsed_time

                sys.stdout.write("#### iter = {0:6d}: render time = {1:.2f} ms, frame rate = {2:.2f} FPS\r".format(count, avg_transit_time, avg_fps))
                sys.stdout.flush()

    except KeyboardInterrupt:
        del image


if __name__ == "__main__":
    main()
