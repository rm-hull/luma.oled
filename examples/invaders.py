#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ported from:
# https://gist.github.com/rm-hull/f18a92207960f250e1d2adcba36a5926#file-invaders-py

import os.path
import time
import random
from demo_opts import device
from oled.render import canvas
from PIL import Image

arrow = [0x04, 0x02, 0x01, 0x02, 0x04]
alien1 = [0x4C, 0x1A, 0xB6, 0x5F, 0x5F, 0xB6, 0x1A, 0x4C]
alien2 = [0x18, 0xFD, 0xA6, 0x3C, 0x3C, 0xA6, 0xFD, 0x18]
alien3 = [0xFC, 0x98, 0x35, 0x7E, 0x7E, 0x35, 0x98, 0xFC]
ARMY_SIZE_ROWS = 2
ARMY_SIZE_COLS = 6


class bullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False

    def render(self, draw):
        if self.alive:
            draw.line((self.x, self.y, self.x, self.y + 2), fill="white")

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        return

    def update(self, direction):
        if self.alive:
            self.y = self.y + (direction * 4)
            if self.y < 10:
                self.alive = False


class player(object):
    def __init__(self):
        self.x = 48
        self.y = 54
        self.bullets = [bullet(0, 0) for _ in range(4)]

    def render(self, draw):
        for i in range(len(arrow)):
            line = arrow[i]
            for j in range(3):
                if line & 0x1:
                    draw.point((self.x - 2 + i, self.y + j), fill="white")
                line >>= 1

        for bullet in self.bullets:
            bullet.render(draw)

    def update(self, direction):
        t = self.x + (direction * 2)
        if t > 4 and t < 92:
            self.x = t
        for bullet in self.bullets:
            bullet.update(-1)

    def shoot(self):
        for bullet in self.bullets:
            if not bullet.alive:
                bullet.reset(self.x, self.y)
                break


class invader(object):
    def __init__(self, minx, maxx, x, y):
        self.x = x
        self.y = y
        self._direction = 1
        self.alive = True
        self.score = 10
        self._minx = minx
        self._maxx = maxx
        return

    def render(self, draw):
        if self.alive:
            for i in range(len(alien2)):
                line = alien2[i]
                for j in range(8):
                    if line & 0x1:
                        draw.point((self.x - 4 + i, self.y - 4 + j), "green")
                    line >>= 1

    def update(self):
        invaded = False
        if self.alive:
            t = self.x + self._direction
            if t > self._minx and t < self._maxx:
                self.x = self.x + self._direction
            else:
                self._direction = self._direction * -1
                self.y = self.y + 2
                if self.y > 44:
                    invaded = True
        return invaded


class army(object):
    def __init__(self):
        self.invaded = False
        self.invaders = []
        for i in range(ARMY_SIZE_ROWS):
            for j in range(ARMY_SIZE_COLS):
                minx = 4 + (j * 12)
                maxx = 30 + (j * 12)
                x = 4 + (j * 12)
                y = 14 + (i * 12)
                self.invaders.append(invader(minx, maxx, x, y))

    def render(self, draw):
        for invader in self.invaders:
            invader.render(draw)

    def update(self, bullets):
        for invader in self.invaders:
            if invader.update():
                self.invaded = True

        for invader in self.invaders:
            if invader.alive:
                for bullet in bullets:
                    if bullet.alive:
                        t = (invader.x - bullet.x) * (invader.x - bullet.x) + (invader.y - bullet.y) * (invader.y - bullet.y)
                        # if point is in circle
                        if t < 25:  # 5 * 5 = r * r
                            invader.alive = False
                            bullet.alive = False

    def size(self):
        size = 0
        for invader in self.invaders:
            if invader.alive:
                size += 1
        return size

    def score(self):
        score = 0
        for invader in self.invaders:
            if not invader.alive:
                score += invader.score
        return score


def ai_logic_shoot(army, plyr):
    for invader in army.invaders:
        if invader.alive:
            if plyr.x > (invader.x - 2) and plyr.x < (invader.x + 2):
                if random.random() < 0.75:
                    plyr.shoot()
                    return


def ai_logic_move(army, plyr, rows):
    for i in rows:
        invader = army.invaders[i]
        if invader.alive:
            if plyr.x < invader.x:
                plyr.update(1)
                return
            elif plyr.x > invader.x:
                plyr.update(-1)
                return
        i += 1


if __name__ == '__main__':

    if device.size not in ((128, 64), (96, 64)):
        raise ValueError("Unsupported mode: {0}x{1}".format(device.width, device.height))

    plyr = player()
    army = army()
    rows = random.sample(range(12), 12)

    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'splash.bmp'))
    splash = Image.open(img_path) \
        .transform((device.width, device.height), Image.AFFINE, (1, 0, 0, 0, 1, 0), Image.BILINEAR) \
        .convert(device.mode)

    # Double buffering in pygame?
    device.display(splash)
    device.display(splash)

    time.sleep(3)
    device.clear()

    while not army.invaded and army.size() > 0:
        with canvas(device) as draw:
            draw.line((0, 61, 95, 61), fill="white")
            draw.line((0, 63, 95, 63), fill="white")

            ai_logic_shoot(army, plyr)
            ai_logic_move(army, plyr, rows)

            army.update(plyr.bullets)

            army.render(draw)
            plyr.render(draw)

            draw.text((8, 0), text="Score: {0}".format(army.score()), fill="blue")

    # Double buffering in pygame?
    for i in range(2):
        with canvas(device) as draw:
            if army.size() == 0:
                draw.text((27, 28), text="Victory", fill="blue")
            else:
                draw.text((30, 28), text="Defeat", fill="red")

    time.sleep(10)
