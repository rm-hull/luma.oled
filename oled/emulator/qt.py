# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2016 Richard Hull
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Qt device emulator.
"""

import sys

from PyQt5.QtWidgets import QWidget

from oled.serial import noop
from oled.device import device


class QtEmulator(device, QWidget):
    """
    Pseudo-device that acts like an OLED display, except that it renders
    to a QWidget. The frame rate is limited to 60FPS (much faster
    than a Raspberry Pi can achieve, but this can be overridden as necessary).

    While the capability of an OLED device is monochrome, there is no
    limitation here, and hence supports 24-bit color depth.

    :mod:`PyQt5` is used to render the emulated display window, and it's
    event loop is checked to see if the ESC key was pressed or the window
    was dismissed: if so :func:`sys.exit()` is called.
    """
    def __init__(self, width=128, height=64, mode="RGB", transform="scale2x",
                 scale=2, frame_rate=60, **kwargs):
        device.__init__(self, serial_interface=noop())

        super(QtEmulator, self).__init__()

        self._pygame.init()
        self._pygame.font.init()
        self._pygame.display.set_caption("OLED Emulator")
        self._clock = self._pygame.time.Clock()
        self._fps = frame_rate
        self._screen = self._pygame.display.set_mode((width * self.scale, height * self.scale))
        self._screen.fill((0, 0, 0))
        self._pygame.display.flip()

    def _abort(self):
        keystate = self._pygame.key.get_pressed()
        return keystate[self._pygame.K_ESCAPE] or self._pygame.event.peek(self._pygame.QUIT)

    def display(self, image):
        """
        Takes a :py:mod:`PIL.Image` and renders it to a pygame display surface.
        """
        assert(image.size[0] == self.width)
        assert(image.size[1] == self.height)

        self._clock.tick(self._fps)
        self._pygame.event.pump()

        if self._abort():
            self._pygame.quit()
            sys.exit()

        surface = self.to_surface(image)
        self._screen.blit(surface, (0, 0))
        self._pygame.display.flip()
