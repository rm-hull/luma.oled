# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Exceptions for this library.
"""


class Error(Exception):
    """
    Base class for exceptions in this library.
    """
    pass


class DeviceNotFoundError(Error):
    """
    Exception raised when a device cannot be found.
    """


class DevicePermissionError(Error):
    """
    Exception raised when permission to access the device is denied.
    """
