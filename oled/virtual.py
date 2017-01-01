# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

import time

from PIL import Image, ImageDraw, ImageFont

import oled.mixin as mixin
from oled.threadpool import threadpool


pool = threadpool(4)


def calc_bounds(xy, entity):
    """
    For an entity with width and height attributes, determine
    the bounding box if were positioned at (x, y).
    """
    left, top = xy
    right, bottom = left + entity.width, top + entity.height
    return [left, top, right, bottom]


def range_overlap(a_min, a_max, b_min, b_max):
    """
    Neither range is completely greater than the other
    """
    return (a_min < b_max) and (b_min < a_max)


class viewport(mixin.capabilities):

    def __init__(self, device, width, height):
        self.capabilities(width, height, rotate=0, mode=device.mode)
        self._device = device
        self._backing_image = Image.new(self.mode, self.size)
        self._position = (0, 0)
        self._hotspots = []

    def display(self, image):
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        self._backing_image.paste(image)
        self.refresh()

    def set_position(self, xy):
        self._position = xy
        self.refresh()

    def add_hotspot(self, hotspot, xy):
        """
        Add the hotspot at (x, y). The hotspot must fit inside the bounds
        of the virtual device. If it does not then an AssertError is raised.
        """
        (x, y) = xy
        assert(0 <= x <= self.width - hotspot.width)
        assert(0 <= y <= self.height - hotspot.height)

        # TODO: should it check to see whether hotspots overlap each other?
        # Is sensible to _allow_ them to overlap?
        self._hotspots.append((hotspot, xy))

    def remove_hotspot(self, hotspot, xy):
        """
        Remove the hotspot at (x, y): Any previously rendered image where the
        hotspot was placed is erased from the backing image, and will be
        "undrawn" the next time the virtual device is refreshed. If the
        specified hotspot is not found (x, y), a ValueError is raised.
        """
        self._hotspots.remove((hotspot, xy))
        eraser = Image.new(self.mode, hotspot.size)
        self._backing_image.paste(eraser, xy)

    def is_overlapping_viewport(self, hotspot, xy):
        """
        Checks to see if the hotspot at position (x, y)
        is (at least partially) visible according to the
        position of the viewport
        """
        l1, t1, r1, b1 = calc_bounds(xy, hotspot)
        l2, t2, r2, b2 = calc_bounds(self._position, self._device)
        return range_overlap(l1, r1, l2, r2) and range_overlap(t1, b1, t2, b2)

    def refresh(self):
        should_wait = False
        for hotspot, xy in self._hotspots:
            if hotspot.should_redraw() and self.is_overlapping_viewport(hotspot, xy):
                pool.add_task(hotspot.paste_into, self._backing_image, xy)
                should_wait = True

        if should_wait:
            pool.wait_completion()

        im = self._backing_image.crop(box=self._crop_box())
        self._device.display(im)
        del im

    def _crop_box(self):
        (left, top) = self._position
        right = left + self._device.width
        bottom = top + self._device.height

        assert(0 <= left <= right <= self.width)
        assert(0 <= top <= bottom <= self.height)

        return (left, top, right, bottom)


class hotspot(mixin.capabilities):
    """
    A hotspot (`a place of more than usual interest, activity, or popularity`)
    is a live display which may be added to a virtual viewport - if the hotspot
    and the viewport are overlapping, then the :func:`update` method will be
    automatically invoked when the viewport is being refreshed or its position
    moved (such that an overlap occurs).

    You would either:

        * create a ``hotspot`` instance, suppling a render function (taking an
          :py:mod:`PIL.ImageDraw` object, ``width`` & ``height`` dimensions. The
          render function should draw within a bounding box of (0, 0, width,
          height), and render a full frame.

        * sub-class ``hotspot`` and override the :func:``should_redraw`` and
          :func:`update` methods. This might be more useful for slow-changing
          values where it is not necessary to update every refresh cycle, or
          your implementation is stateful.
    """
    def __init__(self, width, height, draw_fn=None):
        self.capabilities(width, height, rotate=0)  # TODO: set mode?
        self._fn = draw_fn

    def paste_into(self, image, xy):
        im = Image.new(image.mode, self.size)
        draw = ImageDraw.Draw(im)
        self.update(draw)
        image.paste(im, xy)
        del draw
        del im

    def should_redraw(self):
        """
        Override this method to return true or false on some condition
        (possibly on last updated member variable) so that for slow changing
        hotspots they are not updated too frequently.
        """
        return True

    def update(self, draw):
        if self._fn:
            self._fn(draw, self.width, self.height)


class snapshot(hotspot):
    """
    A snapshot is a `type of` hotspot, but only updates once in a given
    interval, usually much less frequently than the viewport requests refresh
    updates.
    """
    def __init__(self, width, height, draw_fn=None, interval=1.0):
        super(snapshot, self).__init__(width, height, draw_fn)
        self.interval = interval
        self.last_updated = 0.0

    def should_redraw(self):
        """
        Only requests a redraw after ``interval`` seconds have elapsed
        """
        return time.time() - self.last_updated > self.interval

    def paste_into(self, image, xy):
        super(snapshot, self).paste_into(image, xy)
        self.last_updated = time.time()


class terminal(object):
    """
    Provides a terminal-like interface to a device (or a device-like object
    that has :class:`mixin.capabilities` characteristics).
    """
    def __init__(self, device, font=None, color="white", bgcolor="black", tabstop=4, line_height=None, animate=True):
        self._device = device
        self.font = font or ImageFont.load_default()
        self.color = color
        self.bgcolor = bgcolor
        self.animate = animate
        self.tabstop = tabstop

        self._cw, self._ch = (0, 0)
        for i in range(32, 128):
            w, h = self.font.getsize(chr(i))
            self._cw = max(w, self._cw)
            self._ch = max(h, self._ch)

        self._ch = line_height or self._ch
        self.width = device.width // self._cw
        self.height = device.height // self._ch
        self.size = (self.width, self.height)
        self._backing_image = Image.new(self._device.mode, self._device.size, self.bgcolor)
        self._canvas = ImageDraw.Draw(self._backing_image)
        self.clear()

    def clear(self):
        """
        Clears the display and resets the cursor position to (0, 0).
        """
        self._cx, self._cy = (0, 0)
        self._canvas.rectangle(self._device.bounding_box, fill=self.bgcolor)
        self.flush()

    def println(self, text=""):
        """
        Prints the supplied text to the device, scrolling where necessary.
        The text is always followed by a newline.
        """
        self.puts(text)
        self.newline()

    def puts(self, text):
        """
        Prints the supplied text, handling special character codes for carriage
        return (\\r), newline (\\n), backspace (\\b) and tab (\\t).

        If the ``animate`` flag was set to True (default), then each character
        is flushed to the device, giving the effect of 1970's teletype device.
        """
        for line in str(text).split("\n"):
            for char in line:
                if char == '\r':
                    self.carriage_return()

                elif char == '\n':
                    self.newline()

                elif char == '\b':
                    self.backspace()

                elif char == '\t':
                    self.tab()

                else:
                    self.putch(char, flush=self.animate)

    def putch(self, ch, flush=True):
        """
        Prints the specific character, which must be a valid printable ASCII
        value in the range 32..127 only.
        """
        assert(32 <= ord(ch) <= 127)

        w = self.font.getsize(ch)[0]
        if self._cx + w >= self._device.width:
            self.newline()

        self.erase()
        self._canvas.text((self._cx, self._cy), text=ch, font=self.font, fill=self.color)

        self._cx += w
        if flush:
            self.flush()

    def carriage_return(self):
        """
        Returns the cursor position to the left-hand side without advancing
        downwards.
        """
        self._cx = 0

    def tab(self):
        """
        Advances the cursor position to the next (soft) tabstop.
        """
        soft_tabs = self.tabstop - ((self._cx // self._cw) % self.tabstop)
        for _ in range(soft_tabs):
            self.putch(" ", flush=False)

    def newline(self):
        """
        Advances the cursor position ot the left hand side, and to the next
        line. If the cursor is on the lowest line, the displayed contents are
        scrolled, causing the top line to be lost.
        """
        self.carriage_return()

        if self._cy + (2 * self._ch) >= self._device.height:
            # Simulate a vertical scroll
            copy = self._backing_image.crop((0, self._ch, self._device.width, self._device.height))
            self._backing_image.paste(copy, (0, 0))
            self._canvas.rectangle((0, copy.height, self._device.width, self._device.height), fill=self.bgcolor)
        else:
            self._cy += self._ch

        self.flush()
        if self.animate:
            time.sleep(0.2)

    def backspace(self):
        """
        Moves the cursor one place to the left, erasing the character at the
        current position. Cannot move beyound column zero, nor onto the
        previous line
        """
        if self._cx + self._cw >= 0:
            self.erase()
            self._cx -= self._cw

        self.flush()

    def erase(self):
        """
        Erase the contents of the cursor's current postion without moving the
        cursor's position.
        """
        self._canvas.rectangle((self._cx, self._cy, self._cx + self._cw, self._cy + self._ch), fill=self.bgcolor)

    def flush(self):
        """
        Cause the current backing store to be rendered on the nominated device.
        """
        self._device.display(self._backing_image)


class history(mixin.capabilities):
    """
    Wraps a device (or emulator) to provide a facility to be able to make a
    savepoint (a point at which the screen display can be "rolled-back" to).

    This is mostly useful for displaying transient error/dialog messages
    which could be subsequently dismissed, reverting back to the previous
    display.
    """
    def __init__(self, device):
        self.capabilities(device.width, device.height, rotate=0, mode=device.mode)
        self._savepoints = []
        self._device = device
        self._last_image = None

    def display(self, image):
        self._last_image = image.copy()
        self._device.display(image)

    def savepoint(self):
        """
        Copies the last displayed image.
        """
        if self._last_image:
            self._savepoints.append(self._last_image)
            self._last_image = None

    def restore(self, drop=0):
        """
        Restores the last savepoint. If ``drop`` is supplied and greater than
        zero, then that many savepoints are dropped, and the next savepoint is
        restored.
        """
        assert(drop >= 0)
        while drop > 0:
            self._savepoints.pop()
            drop -= 1

        img = self._savepoints.pop()
        self.display(img)

    def __len__(self):
        """
        Indication of the number of savepoints retained.
        """
        return len(self._savepoints)
