# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock  # noqa: F401

import pytest

import luma.core.error

serial = Mock(unsafe=True)


def setup_function(function):
    """
    Called after a test finished.
    """
    serial.reset_mock()
    serial.command.side_effect = None


def assert_invalid_dimensions(deviceType, serial_interface, width, height):
    """
    Assert an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    with pytest.raises(luma.core.error.DeviceDisplayModeError) as ex:
        deviceType(serial_interface, width=width, height=height)
    assert "Unsupported display mode: {} x {}".format(width, height) in str(ex.value)
