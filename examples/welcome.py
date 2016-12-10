#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
from demo_opts import device
from oled.virtual import viewport, snapshot, range_overlap
from PIL import ImageFont

welcome = [
    u"Бзиала шәаабеит",
    u"Къеблагъ",
    u"Welkom",
    u"Maayong pag-abot",
    u"Mayad-ayad nga pad-abot",
    u"Mir se vjên",
    u"እንኳን ደህና መጣህ።",
    u"Willkumme",
    u"أهلاً و سهل",
    u"مرحابة",
    u"Bienvenius",
    u"Բարի գալուստ!",
    u"আদৰণি",
    u"歡迎光臨",
    u"ᑕᑕᐊᐧᐤ",
    u"Woé zɔ",
    u"Bula",
    u"Vælkomin",
    u"Buiti achüluruni",
    u"પધારો",
    u"ברוך הבא",
    u"Üdvözlet",
    u"ಸುಸ್ವಾಗತ",
    u"Приємаєме"
    u"Xoş gəlmişsiniz!",
    u"Salamat datang",
    u"Сәләм бирем!",
    u"Ongi etorri",
    u"Menjuah-juah!",
    u"স্বাগতম",
    u"සාදරයෙන් පිලිගන්නවා",
    u"Добре дошли",
    u"வாருங்கள்",
    u"Kíimak 'oolal",
    u"Märr-ŋamathirri",
    u"Benvinguts",
    u"Марша дагIийла шу",
    u"歡迎",
    u"Velkommen",
    u"Welcome",
    u"Wäljkiimen",
    u"კეთილი იყოს თქვენი",
    u"Καλώς Όρισες",
    u"Eguahé porá",
    u"Sannu da zuwa",
    u"Aloha",
    u"सवागत हैं",
    u"Selamat datang",
    u"Fáilte",
    u"ようこそ",
    u"Ирхитн эрҗәнәвидн",
    u"Witôj",
    u"សូម​ស្វាគមន៍",
    u"환영합니다",
    u"ຍິນດີຕ້ອນຮັບ",
    u"Swagatam",
    u"Haere mai",
    u"Тавтай морилогтун",
    u"خوش آمدید",
    u"Witam Cię",
    u"ਜੀ ਆਇਆ ਨੂੰ।",
    u"Bon vinuti",
    u"ยินดีต้อนรับ",
    u"Hoş geldiniz",
    u"Croeso",
    u"Bonvenon"
]


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def lerp_1d(start, end, n):
    delta = float(end - start) / float(n)
    for i in range(n):
        yield int(round(start + (i * delta)))
    yield end


def lerp_2d(start, end, n):
    x = lerp_1d(start[0], end[0], n)
    y = lerp_1d(start[1], end[1], n)

    try:
        while True:
            yield x.next(), y.next()
    except StopIteration:
        pass


def pairs(generator):
    try:
        last = generator.next()
        while True:
            curr = generator.next()
            yield last, curr
            last = curr
    except StopIteration:
        pass


def infinite_shuffle(arr):
    copy = list(arr)
    while True:
        random.shuffle(copy)
        for elem in copy:
            yield elem


def make_snapshot(width, height, text, font=None, color="white"):

    def render(draw, width, height):
        t = text
        size = draw.multiline_textsize(t, font)
        if size[0] > width:
            t = text.replace(" ", "\n")
            size = draw.multiline_textsize(t, font)

        left = (width - size[0]) // 2
        top = (height - size[1]) // 2
        draw.multiline_text((left, top), text=t, font=font, fill=color,
                            align="center", spacing=-2)

    return snapshot(width, height, render, interval=10)


def random_point(maxx, maxy):
    return random.randint(0, maxx), random.randint(0, maxy)


def overlapping(pt_a, pt_b, w, h):
    la, ta = pt_a
    ra, ba = la + w, ta + h
    lb, tb = pt_b
    rb, bb = lb + w, tb + h
    return range_overlap(la, ra, lb, rb) and range_overlap(ta, ba, tb, bb)


def main():
    font = make_font("code2000.ttf", 20)
    w, h = 256, 256
    for welcome_a, welcome_b in pairs(infinite_shuffle(welcome)):

        virtual = viewport(device, w, h)

        widget_a = make_snapshot(device.width, device.height, welcome_a, font=font)
        widget_b = make_snapshot(device.width, device.height, welcome_b, font=font)

        posn_a = random_point(w - device.width, h - device.height)
        posn_b = random_point(w - device.width, h - device.height)

        while overlapping(posn_a, posn_b, device.width, device.height):
            posn_b = random_point(w - device.width, h - device.height)

        virtual.add_hotspot(widget_a, posn_a)
        virtual.add_hotspot(widget_b, posn_b)

        for _ in range(10):
            virtual.set_position(posn_a)
            time.sleep(0.3)

        for posn in lerp_2d(posn_a, posn_b, 30):
            virtual.set_position(posn)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
