#!/usr/bin/env python

# Ported from:
# https://gist.github.com/TheRayTracer/dd12c498e3ecb9b8b47f#file-clock-py

import math
import time
import datetime
from demo_opts import device
from oled.render import canvas


def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)


def main():
    today_last_time = "Unknown"
    while True:
        now = datetime.datetime.now()
        today_date = now.strftime("%d %b %y")
        today_time = now.strftime("%H:%M:%S")
        if today_time != today_last_time:
            with canvas(device) as draw:
                hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
                hrs = posn(hrs_angle, 12)

                min_angle = 270 + (6 * now.minute)
                mins = posn(min_angle, 18)

                sec_angle = 270 + (6 * now.second)
                secs = posn(sec_angle, 18)

                draw.ellipse((10, 12, 50, 52), outline="white")
                draw.line((30, 32, 30 + hrs[0], 32 + hrs[1]), fill="white")
                draw.line((30, 32, 30 + mins[0], 32 + mins[1]), fill="white")
                draw.line((30, 32, 30 + secs[0], 32 + secs[1]), fill="red")
                draw.ellipse((29, 31, 31, 33), fill="white", outline="white")
                draw.text((60, 24), today_date, fill="white")
                draw.text((60, 32), today_time, fill="white")
                today_last_time = today_time
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
