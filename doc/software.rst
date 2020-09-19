Software
========

Install the latest version of the library directly from
`PyPI <https://pypi.python.org/pypi?:action=display&name=luma.oled>`__
with::

  $ sudo -H pip install --upgrade luma.oled

This will normally retrieve all of the dependencies ``luma.oled`` requires and
install them automatically.

Installing Dependencies
-----------------------
If ``pip`` is unable to automatically install its dependencies you will have to
add them manually.

``luma.oled`` relies on the following packages.

.. csv-table::
  :header: "Package", "Description"
  :widths: 15, 25

    `luma.core <https://pypi.org/project/luma.core/>`_, "Component library supporting luma.lcd and luma.oled"
    `RPi.GPIO <https://pypi.org/project/RPi.GPIO/>`_, "Class to control the GPIO on a Raspberry Pi"
    `smbus2 <https://pypi.org/project/smbus2/>`_, "Interface to smbus (I2C) devices"
    `spidev <https://pypi.org/project/spidev/>`_, "Interface to SPI devices"
    `pyftdi <https://pypi.org/project/pyftdi/>`_, "FTDI device driver"
    `pyserial <https://pypi.org/project/pyserial/>`_, "Serial Port Extension"
    `pyusb <https://pypi.org/project/pyusb/>`_, "USB access module"
    `cbor2 <https://pypi.org/project/cbor2/>`_, "CBOR (de)serializer"
    `pillow <https://pypi.org/project/Pillow/>`_, "Imaging Library"

If you receive error messages when using pip to install ``luma.oled``
it is likely because one or more of these packages are missing
their dependencies on your system with the most likely culprit
being pillow.

To resolve the issues you will need to add the appropriate development
resources to continue.

If you are using Raspbian Stretch or Raspberry Pi OS (Buster) you should
be able to use the following commands to add the required packages::

$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
$ sudo -H pip3 install luma.oled

If you are not using Raspbian you will need to consult the documentation for
your Linux distribution to determine the correct procedure to install
the dependencies.  The individual installation instructions for each package
are available on their pypi pages.

.. tip::
  If your distribution includes a pre-packaged version of Pillow,
  use it instead of installing from pip.  On many distributions the correct
  package to install is ``python3-imaging``.  Another common package name for
  Pillow is ``python3-pil``.::

    $ sudo apt-get install python3-imaging

  or::

    $ sudo apt-get install python3-pil

Permissions
-----------
``luma.oled`` uses hardware interfaces that require permission to access.  After you
have successfully installed ``luma.oled`` you may want to add the user account that
your ``luma.oled`` program will run as to the groups that grant access to these
interfaces.::

  $ sudo usermod -a -G spi,gpio,i2c pi

Replace ``pi`` with the name of the account you will be using.
