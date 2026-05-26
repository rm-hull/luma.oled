# -*- coding: utf-8 -*-
# Copyright (c) 2020 Richard Hull and contributors
# See LICENSE.rst for details.

import luma.core.framebuffer


class __framebuffer_mixin(object):
    """
    Helper class for initializing the framebuffer. 

    .. versionadded:: 3.8.0
    """

    def init_framebuffer(self, framebuffer):
        if framebuffer is None:
            self.framebuffer = luma.core.framebuffer.diff_to_previous()
        else:
            self.framebuffer = framebuffer
