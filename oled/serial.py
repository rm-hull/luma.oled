# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

import errno

import oled.error


class i2c(object):
    """
    Wrap an `I2C <https://en.wikipedia.org/wiki/I%C2%B2C>`_ interface to
    provide data and command methods.

    :param bus: I2C bus instance.
    :type bus:
    :param port: I2C port number.
    :type port: int
    :param address: I2C address.
    :type address:
    :raises oled.error.DeviceAddressError: I2C device address is invalid.
    :raises oled.error.DeviceNotFoundError: I2C device could not be found.
    :raises oled.error.DevicePermissionError: Permission to access I2C device
        denied.

    .. note::
       1. Only one of ``bus`` OR ``port`` arguments should be supplied;
          if both are, then ``bus`` takes precedence.
       2. If ``bus`` is provided, there is an implicit expectation
          that it has already been opened.
    """
    def __init__(self, bus=None, port=1, address=0x3C):
        import smbus2
        self._cmd_mode = 0x00
        self._data_mode = 0x40

        try:
            self._addr = int(str(address), 0)
        except ValueError:
            raise oled.error.DeviceAddressError(
                'I2C device address invalid: {}'.format(address))

        try:
            self._bus = bus or smbus2.SMBus(port)
        except (IOError, OSError) as e:
            if e.errno == errno.ENOENT:
                # FileNotFoundError
                raise oled.error.DeviceNotFoundError(
                    'I2C device not found: {}'.format(e.filename))
            elif e.errno == errno.EPERM or e.errno == errno.EACCES:
                # PermissionError
                raise oled.error.DevicePermissionError(
                    'I2C device permission denied: {}'.format(e.filename))
            else:
                raise

    def command(self, *cmd):
        """
        Sends a command or sequence of commands through to the I2C address
        - maximum allowed is 32 bytes in one go.
        """
        assert(len(cmd) <= 32)
        self._bus.write_i2c_block_data(self._addr, self._cmd_mode, list(cmd))

    def data(self, data):
        """
        Sends a data byte or sequence of data bytes through to the I2C
        address - maximum allowed in one transaction is 32 bytes, so if
        data is larger than this, it is sent in chunks.
        """
        i = 0
        n = len(data)
        write = self._bus.write_i2c_block_data
        while i < n:
            write(self._addr, self._data_mode, list(data[i:i + 32]))
            i += 32

    def cleanup(self):
        """
        Clean up I2C resources
        """
        self._bus.close()


class spi(object):
    """
    Wraps an `SPI <https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus>`_
    interface to provide data and command methods.

     * The DC pin (Data/Command select) defaults to GPIO 24 (BCM).
     * The RST pin (Reset) defaults to GPIO 25 (BCM).

    :raises oled.error.DeviceNotFoundError: SPI device could not be found.
    """
    def __init__(self, spi=None, gpio=None, port=0, device=0,
                 bus_speed_hz=8000000, bcm_DC=24, bcm_RST=25):
        self._gpio = gpio or self.__rpi_gpio__()
        self._spi = spi or self.__spidev__()

        try:
            self._spi.open(port, device)
        except (IOError, OSError) as e:
            if e.errno == errno.ENOENT:
                # FileNotFoundError
                raise oled.error.DeviceNotFoundError('SPI device not found')
            else:
                raise

        self._spi.max_speed_hz = bus_speed_hz
        self._bcm_DC = bcm_DC
        self._bcm_RST = bcm_RST
        self._cmd_mode = self._gpio.LOW    # Command mode = Hold low
        self._data_mode = self._gpio.HIGH  # Data mode = Pull high

        self._gpio.setmode(self._gpio.BCM)
        self._gpio.setup(self._bcm_DC, self._gpio.OUT)
        self._gpio.setup(self._bcm_RST, self._gpio.OUT)
        self._gpio.output(self._bcm_RST, self._gpio.HIGH)  # Keep RESET pulled high

    def __rpi_gpio__(self):
        # RPi.GPIO _really_ doesn't like being run on anything other than
        # a Raspberry Pi... this is imported here so we can swap out the
        # implementation for a mock
        import RPi.GPIO
        return RPi.GPIO

    def __spidev__(self):
        # spidev cant compile on macOS, so use a similar technique to
        # initialize (mainly so the tests run unhindered)
        import spidev
        return spidev.SpiDev()

    def command(self, *cmd):
        """
        Sends a command or sequence of commands through to the SPI device.
        """
        self._gpio.output(self._bcm_DC, self._cmd_mode)
        self._spi.xfer2(list(cmd))

    def data(self, data):
        """
        Sends a data byte or sequence of data bytes through to the SPI device.
        If the data is more than 4Kb in size, it is sent in chunks.
        """
        self._gpio.output(self._bcm_DC, self._data_mode)
        i = 0
        n = len(data)
        write = self._spi.xfer2
        while i < n:
            write(data[i:i + 4096])
            i += 4096

    def cleanup(self):
        """
        Clean up SPI & GPIO resources
        """
        self._spi.close()
        self._gpio.cleanup()


class noop(object):
    """
    Does nothing, used for pseudo-devices / emulators, which dont have a serial
    interface.
    """
    def command(self, *cmd):
        pass

    def data(self, data):
        pass

    def cleanup(self):
        pass
