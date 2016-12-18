#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
from hotspot.common import bytes2human, right_text, title_text, tiny_font


def stats(interface):

    def render(draw, width, height):
        margin = 3
        title_text(draw, margin, width, text="Net:{0}".format(interface))
        try:
            address = psutil.net_if_addrs()[interface][0].address
            counters = psutil.net_io_counters(pernic=True)[interface]

            draw.text((margin, 20), text=address, font=tiny_font, fill="white")
            draw.text((margin, 35), text="Rx:", font=tiny_font, fill="white")
            draw.text((margin, 45), text="Tx:", font=tiny_font, fill="white")

            right_text(draw, 35, width, margin, text=bytes2human(counters.bytes_recv))
            right_text(draw, 45, width, margin, text=bytes2human(counters.bytes_sent))
        except:
            draw.text((margin, 20), text="n/a", font=tiny_font, fill="white")

    return render
