#!/usr/bin/env python

# Ported from:
# https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py

import time
import datetime
from demo_opts import device
from oled.render import canvas


def primitives(draw):
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 2
    shape_width = 20
    top = padding
    bottom = device.height - padding - 1
    # Draw a rectangle of the same size of screen
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    # Move left to right keeping track of the current x position for drawing shapes.
    x = padding
    # Draw an ellipse.
    draw.ellipse((x, top, x + shape_width, bottom), outline="white", fill="black")
    x += shape_width + padding
    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, bottom), outline="white", fill="black")
    x += shape_width + padding
    # Draw a triangle.
    draw.polygon([(x, bottom), (x + shape_width / 2, top), (x + shape_width, bottom)], outline="white", fill="black")
    x += shape_width + padding
    # Draw an X.
    draw.line((x, bottom, x + shape_width, top), fill="white")
    draw.line((x, top, x + shape_width, bottom), fill="white")
    x += shape_width + padding
    # Write two lines of text.
    draw.text((x, top),    'Hello', fill="white")
    draw.text((x, top + 20), 'World!', fill="white")


def main():
    print("Testing basic canvas graphics...")
    with canvas(device) as draw:
        primitives(draw)

    time.sleep(10)

    print("Testing display ON/OFF...")
    for _ in range(5):
        time.sleep(0.5)
        device.hide()

        time.sleep(0.5)
        device.show()

    print("Testing clear display...")
    time.sleep(2)
    device.clear()

    print("Testing screen updates...")
    time.sleep(2)
    for x in range(40):
        with canvas(device) as draw:
            now = datetime.datetime.now()
            draw.text((x, 10), str(now.date()), fill="white")
            draw.text((10, 24), str(now.time()), fill="white")
            time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
