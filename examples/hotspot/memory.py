#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
from common import bytes2human, right_text, title_text, tiny_font


def render(draw, width, height):
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    mem_used_pct = (mem.total - mem.available) * 100.0 / mem.total

    margin = 3

    title_text(draw, margin, width, text="Memory")
    draw.text((margin, 20), text="Used:", font=tiny_font, fill="white")
    draw.text((margin, 35), text="Phys:", font=tiny_font, fill="white")
    draw.text((margin, 45), text="Swap:", font=tiny_font, fill="white")

    right_text(draw, 20, width, margin, text="{0:0.1f}%".format(mem_used_pct))
    right_text(draw, 35, width, margin, text=bytes2human(mem.used))
    right_text(draw, 45, width, margin, text=bytes2human(swap.used))
