#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

# Adapted from:
#  http://codentronix.com/2011/05/28/3d-starfield-made-using-python-and-pygame/

from random import randrange
from demo_opts import device
from luma.core.render import canvas


def init_stars(num_stars, max_depth):
    stars = []
    for i in range(num_stars):
        # A star is represented as a list with this format: [X,Y,Z]
        star = [randrange(-25, 25), randrange(-25, 25), randrange(1, max_depth)]
        stars.append(star)
    return stars


def move_and_draw_stars(stars, max_depth):
    origin_x = device.width // 2
    origin_y = device.height // 2

    with canvas(device) as draw:
        for star in stars:
            # The Z component is decreased on each frame.
            star[2] -= 0.19

            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if star[2] <= 0:
                star[0] = randrange(-25, 25)
                star[1] = randrange(-25, 25)
                star[2] = max_depth

            # Convert the 3D coordinates to 2D using perspective projection.
            k = 128.0 / star[2]
            x = int(star[0] * k + origin_x)
            y = int(star[1] * k + origin_y)

            # Draw the star (if it is visible in the screen).
            # We calculate the size such that distant stars are smaller than
            # closer stars. Similarly, we make sure that distant stars are
            # darker than closer stars. This is done using Linear Interpolation.
            if 0 <= x < device.width and 0 <= y < device.height:
                size = (1 - float(star[2]) / max_depth) * 4
                if (device.mode == "RGB"):
                    shade = (int(100 + (1 - float(star[2]) / max_depth) * 155),) * 3
                else:
                    shade = "white"
                draw.rectangle((x, y, x + size, y + size), fill=shade)


def main():
    max_depth = 32
    stars = init_stars(512, max_depth)
    while True:
        move_and_draw_stars(stars, max_depth)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
