# -*- coding: utf-8 -*-
# Copyright (c) 2020-2026 Richard Hull and contributors
# See LICENSE.rst for details.

import luma.core.framebuffer


class __framebuffer_mixin(object):
    """
    Helper class for initializing the framebuffer.

    :param framebuffer: Typically an instance of class full_frame() or diff_to_previous().

    .. versionadded:: 3.8.0
    """
    def init_framebuffer(self, framebuffer):
        self.framebuffer = framebuffer or luma.core.framebuffer.diff_to_previous()
