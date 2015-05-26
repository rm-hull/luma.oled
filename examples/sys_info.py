#!/usr/bin/env python
#
# !!! Needs psutil installing:
#
#    $ sudo pip install psutil
#
# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram

# Stdlib.
import datetime
import os
import socket
import sys

if os.name != 'posix':
    sys.exit('platform not supported')
    
# 3rd party.
try:
    import psutil
except ImportError:
    print 'Need psutil. Try: sudo pip install psutil'
    sys.exit(1)

from PIL import ImageFont

# Allow running example without installing library.
sys.path.append('..')

import oled.device
import oled.render

# Select serial interface to match your OLED device.
# The defaults for the arguments are shown. No arguments are required.
#serial_interface = oled.device.I2C(port=1, address=0x3C, cmd_mode=0x00, data_mode=0x40)
serial_interface = oled.device.SPI(port=0, spi_bus_speed_hz=32000000, gpio_command_data_select=24, gpio_reset=25)
# Select controller chip to match your OLED device.
device = oled.device.sh1106(serial_interface)
#device = oled.device.ssd1306(serial_interface)


def main():
    # Nicer font, only availalable if Pillow was compiled with TrueType support.
    ttf_path = os.path.join(os.path.dirname(__file__), 'fonts', 'C&C Red Alert [INET].ttf')
    try:
      font = ImageFont.truetype(ttf_path, 12)
    except ImportError, EnvironmentError:
      # Fall back to default font.
      font = ImageFont.load_default()

    pos = 0
    with oled.render.canvas(device) as draw:
        pos += print_line(draw, font, pos, hostname())
        pos += print_line(draw, font, pos, cpu_usage())
        pos += print_line(draw, font, pos, mem_usage())
        pos += print_line(draw, font, pos, disk_usage('/'))
        pos += print_line(draw, font, pos, network('eth0'))
        pos += print_line(draw, font, pos, network('wlan0'))

def print_line(draw, font, pos, msg):
    draw.text((0, pos), msg, font=font, fill=255)
    return font.getsize(msg)[1]

def hostname():
    return "Host: {}".format(socket.gethostname())

def cpu_usage():
    # load average, uptime
    return "Ld: {:.1f} {:.1f} {:.1f}".format(*os.getloadavg())

def uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.BOOT_TIME)
    return 'Up: {}'.format(datetime.timedelta(uptime))

def mem_usage():
    usage = psutil.phymem_usage()
    return "Mem: {} {:.0f}%".format(bytes2human(usage.used), 100 - usage.percent)

def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  {} {:.0f}%".format(bytes2human(usage.used), usage.percent)

def network(iface):
    try:
      stat = psutil.network_io_counters(pernic=True)[iface]
    except KeyError:
      return "{}: <not present>".format(iface)
    else:
      return "{}: Tx {}, Rx {}".format(iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

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
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

if __name__ == "__main__":
    main()
