Software
========

Before installing the library, create a
`virtual environment <https://docs.python.org/3/library/venv.html>`__ for your
project using::

  $ python3 -m venv ~/luma-env

This creates a virtual environment in the home directory called `luma-env`
and a Python executable at `~/luma-env/bin/python`.

Next, install the `latest version of the library <https://pypi.python.org/pypi?:action=display&name=luma.oled>`__
in the virtual environment directly with::

  $ ~/luma-env/bin/python -m pip install --upgrade luma.oled

This will normally retrieve all of the dependencies ``luma.oled`` requires and
install them automatically.

Installing Dependencies
-----------------------
If ``pip`` is unable to automatically install its dependencies you will have to
add them manually.  To resolve the issues you will need to add the appropriate
development packages to continue.

If you are using Raspberry Pi OS you should be able to use the following commands
to add the required packages::

$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y

If you are not using Raspberry Pi OS you will need to consult the documentation for
your Linux distribution to determine the correct procedure to install
the dependencies.

.. tip::
  If your distribution includes a pre-packaged version of Pillow,
  use it instead of installing from pip.  On many distributions the correct
  package to install is ``python3-imaging``.  Another common package name for
  Pillow is ``python3-pil``::

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
