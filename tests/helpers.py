# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

from unittest.mock import Mock
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
    assert f"Unsupported display mode: {width} x {height}" in str(ex.value)
