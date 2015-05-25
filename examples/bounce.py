#!/usr/bin/env python

# Display a bouncing ball animation and frames per second.

# Stdlib.
import os
import time
import random
import sys

# Allow running example without installing library.
sys.path.append('..')

# 3rd party.
from PIL import ImageFont

import oled.device
import oled.render

# Select serial interface to match your OLED device.
# The defaults for the arguments are shown. No arguments are required.
#serial_interface = oled.device.I2C(port=1, address=0x3C, cmd_mode=0x00, data_mode=0x40)
serial_interface = oled.device.SPI(port=0, spi_bus_speed_hz=32000000, gpio_command_data_select=24, gpio_reset=25)
# Select controller chip to match your OLED device.
device = oled.device.sh1106(serial_interface)
#device = oled.device.ssd1306(serial_interface)


class Ball(object):
    def __init__(self, w, h, radius):
        self._w = w
        self._h = h
        self._radius = radius
        self._x_speed = (random.random() - 0.5) * 10
        self._y_speed = (random.random() - 0.5) * 10
        self._x_pos = self._w / 2.0
        self._y_pos = self._h / 2.0
        
    def update_pos(self):
        if self._x_pos + self._radius > self._w:
            self._x_speed = -abs(self._x_speed)
        elif self._x_pos - self._radius < 0.0:
            self._x_speed = abs(self._x_speed)
            
        if self._y_pos + self._radius > self._h:
            self._y_speed = -abs(self._y_speed)
        elif self._y_pos - self._radius < 0.0:
            self._y_speed = abs(self._y_speed)

        self._x_pos += self._x_speed
        self._y_pos += self._y_speed
        
    def draw(self, canvas):
        canvas.ellipse((self._x_pos - self._radius, self._y_pos - self._radius,
                   self._x_pos + self._radius, self._y_pos + self._radius), fill=255)
        #canvas.text((self._x_pos, self._y_pos), "{}".format(self._x_pos), font=font, fill=255)
        
        
def main():    
    font = ImageFont.load_default()

    start_time = time.time()
    
    balls = []
    for i in range(10):
        balls.append(Ball(device.width, device.height, i * 1.5))
    frame_count = 0
    while True:
        frame_count += 1
        with oled.render.canvas(device) as c:
            for b in balls:
                b.update_pos()
                b.draw(c)
            c.text((0, 0), "FPS: {}".format(frame_count / (time.time() - start_time)), font=font, fill=255)

if __name__ == '__main__':
    main()
