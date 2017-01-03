# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

import os
import sys
import atexit
import logging
from PIL import Image
from oled.device import device
from oled.serial import noop

logger = logging.getLogger(__name__)


class emulator(device):
    """
    Base class for emulated OLED driver classes
    """
    def __init__(self, width, height, rotate, mode, transform, scale):
        super(emulator, self).__init__(serial_interface=noop())
        try:
            import pygame
        except:
            raise RuntimeError("Emulator requires pygame to be installed")
        self._pygame = pygame
        self.capabilities(width, height, rotate, mode)
        self.scale = 1 if transform == "none" else scale
        self._transform = getattr(transformer(pygame, width, height, scale),
                                  "none" if scale == 1 else transform)

    def cleanup(self):
        pass

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


class capture(emulator):
    """
    Pseudo-device that acts like an OLED display, except that it writes
    the image to a numbered PNG file when the :func:`display` method
    is called.

    While the capability of an OLED device is monochrome, there is no
    limitation here, and hence supports 24-bit color depth.
    """
    def __init__(self, width=128, height=64, rotate=0, mode="RGB",
                 transform="scale2x", scale=2, file_template="oled_{0:06}.png",
                 **kwargs):
        super(capture, self).__init__(width, height, rotate, mode, transform, scale)
        self._count = 0
        self._file_template = file_template

    def display(self, image):
        """
        Takes a :py:mod:`PIL.Image` and dumps it to a numbered PNG file.
        """
        assert(image.size == self.size)

        self._count += 1
        filename = self._file_template.format(self._count)
        image = self.preprocess(image)
        surface = self.to_surface(image)
        logger.debug("Writing: {0}".format(filename))
        self._pygame.image.save(surface, filename)


class gifanim(emulator):
    """
    Pseudo-device that acts like an OLED display, except that it collects
    the images when the :func:`display` method is called, and on exit,
    assembles them into an animated GIF image.

    While the capability of an OLED device is monochrome, there is no
    limitation here, and hence supports 24-bit color depth, albeit with
    an indexed color palette.
    """
    def __init__(self, width=128, height=64, rotate=0, mode="RGB",
                 transform="scale2x", scale=2, filename="oled_anim.gif",
                 duration=0.01, loop=0, max_frames=None, **kwargs):
        super(gifanim, self).__init__(width, height, rotate, mode, transform, scale)
        self._images = []
        self._count = 0
        self._max_frames = max_frames
        self._filename = filename
        self._loop = loop
        self._duration = duration
        atexit.register(self.write_animation)

    def display(self, image):
        """
        Takes an image, scales it according to the nominated transform, and
        stores it for later building into an animated GIF.
        """
        assert(image.size == self.size)

        image = self.preprocess(image)
        surface = self.to_surface(image)
        rawbytes = self._pygame.image.tostring(surface, "RGB", False)
        im = Image.frombytes("RGB", (self._w * self.scale, self._h * self.scale), rawbytes)
        self._images.append(im)

        self._count += 1
        logger.debug("Recording frame: {0}".format(self._count))

        if self._max_frames and self._count >= self._max_frames:
            sys.exit(0)

    def write_animation(self):
        logger.debug("Please wait... building animated GIF")
        with open(self._filename, "w+b") as fp:
            self._images[0].save(fp, save_all=True, loop=self._loop,
                                 duration=int(self._duration * 1000),
                                 append_images=self._images[1:],
                                 format="GIF")

        logger.debug("Wrote {0} frames to file: {1} ({2} bytes)".format(
            len(self._images), self._filename, os.stat(self._filename).st_size))


class pygame(emulator):
    """
    Pseudo-device that acts like an OLED display, except that it renders
    to an displayed window. The frame rate is limited to 60FPS (much faster
    than a Raspberry Pi can acheive, but this can be overridden as necessary).

    While the capability of an OLED device is monochrome, there is no
    limitation here, and hence supports 24-bit color depth.

    :mod:`pygame` is used to render the emulated display window, and it's
    event loop is checked to see if the ESC key was pressed or the window
    was dismissed: if so :func:`sys.exit()` is called.
    """
    def __init__(self, width=128, height=64, rotate=0, mode="RGB", transform="scale2x",
                 scale=2, frame_rate=60, **kwargs):
        super(pygame, self).__init__(width, height, rotate, mode, transform, scale)
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
        assert(image.size == self.size)

        image = self.preprocess(image)
        self._clock.tick(self._fps)
        self._pygame.event.pump()

        if self._abort():
            self._pygame.quit()
            sys.exit()

        surface = self.to_surface(image)
        self._screen.blit(surface, (0, 0))
        self._pygame.display.flip()


class dummy(emulator):
    """
    Pseudo-device that acts like an OLED display, except that it does nothing
    other than retain a copy of the displayed image. It is mostly useful for
    testing. While the capability of an OLED device is monochrome, there is no
    limitation here, and hence supports 24-bit color depth.
    """
    def __init__(self, width=128, height=64, rotate=0, mode="RGB", transform="scale2x",
                 scale=2, **kwargs):
        super(dummy, self).__init__(width, height, rotate, mode, transform, scale)
        self.image = None

    def display(self, image):
        """
        Takes a :py:mod:`PIL.Image` and makes a copy of it for later
        use/inspection.
        """
        assert(image.size == self.size)

        self.image = self.preprocess(image).copy()


class transformer(object):
    """
    Helper class used to dispatch transformation operations.
    """
    def __init__(self, pygame, width, height, scale):
        self._pygame = pygame
        self._output_size = (width * scale, height * scale)
        self.scale = scale

    def none(self, surface):
        """
        No-op transform - used when ``scale`` = 1
        """
        return surface

    def scale2x(self, surface):
        """
        Scales using the AdvanceMAME Scale2X algorithm which does a
        'jaggie-less' scale of bitmap graphics.
        """
        assert(self.scale == 2)
        return self._pygame.transform.scale2x(surface)

    def smoothscale(self, surface):
        """
        Smooth scaling using MMX or SSE extensions if available
        """
        return self._pygame.transform.smoothscale(surface, self._output_size)

    def identity(self, surface):
        """
        Fast scale operation that does not sample the results
        """
        return self._pygame.transform.scale(surface, self._output_size)
