# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Qt device emulator.
"""

import sys

from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget

from oled.emulator import emulator


class QtEmulator(emulator):
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

        super(QtEmulator, self).__init__(width, height, mode, transform, scale)

        self._fps = frame_rate

        # create screen
        self._screen = QWidget()
        self._screen.setGeometry(0, 0, width * self.scale, height * self.scale)

        # create timer
        self._clock = QTimer()

        # set black background
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.black)
        self._screen.setAutoFillBackground(True)
        self._screen.setPalette(pal)

    @property
    def widget(self):
        return self._screen

    def _abort(self):
        keystate = self._pygame.key.get_pressed()
        return keystate[self._pygame.K_ESCAPE] or self._pygame.event.peek(self._pygame.QUIT)

    def display(self, image):
        """
        Takes a :py:mod:`PIL.Image` and renders it to a pygame display surface.
        """
        assert(image.size[0] == self.width)
        assert(image.size[1] == self.height)

        #self._clock.tick(self._fps)
        #self._pygame.event.pump()

        #if self._abort():
        #self._pygame.quit()
        #sys.exit()

        surface = self.to_surface(image)
        #self._screen.blit(surface, (0, 0))
        #self._pygame.display.flip()

    def to_surface(self, image):
        """
        Converts a :py:mod:`PIL.Image` into a :class:`pygame.Surface`,
        transforming it according to the ``transform`` and ``scale``
        constructor arguments.
        """
        im = image.convert("RGB")
        mode = im.mode
        size = im.size
        data = im.tobytes()
        del im

        surface = self._pygame.image.fromstring(data, size, mode)
        return self._transform(surface)
