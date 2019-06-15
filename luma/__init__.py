# -*- coding: utf-8 -*-
# Copyright (c) 2014-2019 Richard Hull and contributors
# See LICENSE.rst for details.

try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)
