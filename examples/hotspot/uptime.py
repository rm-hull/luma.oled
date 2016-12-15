#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import psutil
from common import title_text, right_text


def render(draw, width, height):
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    elapsed = datetime.now() - boot_time
    margin = 3
    title_text(draw, margin, width, "Uptime")
    right_text(draw, 20, width, margin, text="{0} s".format(int(elapsed.total_seconds())))
