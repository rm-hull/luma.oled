#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import datetime

from common import title_text, tiny_font


def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)


def digital(draw, width, height):
    margin = 3

    now = datetime.datetime.now()
    today_date = now.strftime("%d %b %y")
    current_time = now.strftime("%H:%m:%S")

    title_text(draw, margin, width, today_date)
    draw.text((margin + 10, 20), text=current_time, fill="white", font=tiny_font)


def analog(draw, width, height):
    now = datetime.datetime.now()
    today_date = now.strftime("%d %b %y")

    top = 16
    margin = 3

    cx = width / 2
    cy = top + ((height - top - margin) / 2)

    left = (width - (height - top - margin)) / 2
    right = width - left

    hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
    hrs = posn(hrs_angle, cx - 16)

    min_angle = 270 + (6 * now.minute)
    mins = posn(min_angle, cx - 10)

    sec_angle = 270 + (6 * now.second)
    secs = posn(sec_angle, cx - 10)

    draw.ellipse((left, top, right, height - margin), outline="white")
    draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill="white")
    draw.line((cx, cy, cx + mins[0], cy + mins[1]), fill="white")
    draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill="red")
    draw.ellipse((cx - 1, cy - 1, cx + 1, cy + 1), fill="white", outline="white")
    title_text(draw, margin, width, today_date)


def render(draw, width, height):
    clock = analog if height >= 64 else digital
    clock(draw, width, height)
