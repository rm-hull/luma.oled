#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2015 Richard Hull
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import smbus2


class i2c(object):
    """
    Wrap an I2C interface to provide data and command methods

    Note: Only one of bus OR port arguments should be supplied; if both
    are, then bus takes precedence.
    """
    def __init__(self, bus=None, port=1, address=0x3C, cmd_mode=0x00,
		 data_mode=0x40):
	self.cmd_mode = cmd_mode
	self.data_mode = data_mode
	self.bus = bus or smbus2.SMBus(port)
	self.addr = address

    def command(self, *cmd):
	"""
	Sends a command or sequence of commands through to the I2C address
	- maximum allowed is 32 bytes in one go.
	"""
	assert(len(cmd) <= 32)
	self.bus.write_i2c_block_data(self.addr, self.cmd_mode, list(cmd))

    def data(self, data):
	"""
	Sends a data byte or sequence of data bytes through to the I2C
	address - maximum allowed in one transaction is 32 bytes, so if
	data is larger than this it is sent in chunks.
	"""
	i = 0
	n = len(data)
	while i < n:
	    self.bus.write_i2c_block_data(self.addr,
					  self.data_mode,
					  list(data[i:i + 32]))
	    i += 32


class spi(object):
    """
    Wraps an SPI interface to provide data and command methods.
    """
    def __init__(self):
	pass

    def command(self, *cmd):
	"""
	Sends a command or sequence of commands through the SPI
	"""
	raise NotImplementedError()

    def data(self, data):
	"""
	Sends a data byte or sequence of data bytes through the SPI
	"""
	raise NotImplementedError()
