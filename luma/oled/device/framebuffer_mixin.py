import luma.core.framebuffer


class __framebuffer_mixin(object):
    """
    Helper class for initializing the framebuffer. Its only purpose is to
    log a deprecation warning if a string framebuffer is specified.

    .. note::
        Specifying the framebuffer as a string will be removed at the next
        major release, and hence this mixin will become redundant and will
        also be removed at that point.
    """

    def init_framebuffer(self, framebuffer):
        if isinstance(framebuffer, str):
            import warnings
            warnings.warn(
                "Specifying framebuffer as a string is now deprecated; Supply an instance of class full_frame() or diff_to_previous() instead",
                DeprecationWarning
            )
            self.framebuffer = getattr(luma.core.framebuffer, framebuffer)()
        else:
            self.framebuffer = framebuffer
