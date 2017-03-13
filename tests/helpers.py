# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock  # noqa: F401


serial = Mock(unsafe=True)


def setup_function(function):
    """
    Called after a test finished.
    """
    serial.reset_mock()
    serial.command.side_effect = None
