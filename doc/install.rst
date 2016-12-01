Installation
------------
.. warning::
   Ensure that the pre-requisites from the previous section have been performed
   and checked/tested before proceeding.

.. note:: The library has been tested against Python 2.7 and 3.4.

   For **Python3** installation, substitute the following in the
   instructions below.

   * ``pip`` ⇒ ``pip3``, 
   * ``python`` ⇒ ``python3``, 
   * ``python-dev`` ⇒ ``python3-dev``,
   * ``python-pip`` ⇒ ``python3-pip``.

   It was *originally* tested with Raspian on a rev.2 model B, with a vanilla
   kernel version 4.1.16+, and has subsequently tested on Raspberry Pi model A
   & model B2 (Debian Jessie) and OrangePi Zero (Armbian Jessie).

from PyPI
^^^^^^^^^
.. note:: This is the preferred installation mechanism.

Install the latest version of the library directly from
`PyPI <https://pypi.python.org/pypi?:action=display&name=ssd1306>`_::

  $ sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg8-dev
  $ sudo pip install --upgrade ssd1306

from source
^^^^^^^^^^^
For python2, from the bash prompt, enter::

  $ sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg8-dev
  $ sudo python setup.py install
