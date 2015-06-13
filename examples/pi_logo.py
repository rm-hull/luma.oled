#!/usr/bin/env python

# Stdlib.
import os
import sys

# Allow running example without installing library.
sys.path.append('..')

# 3rd party.
from PIL import Image

import oled.device
import oled.render

# Select serial interface to match your OLED device.
# The defaults for the arguments are shown. No arguments are required.
#serial_interface = oled.device.I2C(port=1, address=0x3C, cmd_mode=0x00, data_mode=0x40)
serial_interface = oled.device.SPI(port=0, spi_bus_speed_hz=32000000, gpio_command_data_select=24, gpio_reset=25)
# Select controller chip to match your OLED device.
device = oled.device.sh1106(serial_interface)
#device = oled.device.ssd1306(serial_interface)

with oled.render.canvas(device) as draw:
    logo = Image.open(os.path.join(os.path.dirname(__name__), 'images/pi_logo.png'))
    draw.bitmap((32, 0), logo, fill=1)
