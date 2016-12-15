#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
#
# !!! Needs psutil (+ dependencies) installing:
#
#    $ sudo apt-get install python-dev
#    $ sudo pip install psutil
#

import os
import sys
import time
from datetime import datetime
if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

import psutil

from demo_opts import device
from oled.render import canvas
from PIL import ImageFont

# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
        % (av1, av2, av3, str(uptime).split('.')[0])


def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))


def stats(oled):
    # use custom font
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)

    with canvas(oled) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        if device.height >= 32:
            draw.text((0, 14), mem_usage(), font=font2, fill="white")

        if device.height >= 64:
            draw.text((0, 26), disk_usage('/'), font=font2, fill="white")
            try:
                draw.text((0, 38), network('wlan0'), font=font2, fill="white")
            except KeyError:
                # no wifi enabled/available
                pass


def main():
    while True:
        stats(device)
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
