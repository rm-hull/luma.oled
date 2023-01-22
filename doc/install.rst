Installation
============

The successful installation of a display module to your SBC requires a combination
of tasks to be completed before the display will operate correctly.

First, the device needs to be wired up correctly to your single-board computer
(SBC) and the interface that will be used needs to be enabled in the kernel
of the operating system of the SBC.  Instructions to for this are provided in
:doc:`hardware`.

Equally important, the ``luma.oled`` software needs to be installed including
the build dependencies that for the python modules it uses.  Instructions
to complete that task are provided in :doc:`software`.

Finally, you need to leverage the appropriate interface class and display
class for your device to implement your application.  Instructions for that
are included in :doc:`python-usage`.

.. note:: This library has been tested against Python 3.5, 3.6, 3.7 and 3.8.

  It was *originally* tested with Raspbian on a rev.2 model B, with a vanilla
  kernel version 4.1.16+, and has subsequently been tested on Raspberry Pi
  models A, B2, 3B, Zero, Zero W, OrangePi Zero (Armbian Jessie), and 4B with
  Raspberry Pi OS Jessie, Stretch, Buster and Bullseye operating systems.

.. note:: Upgrading
  If you are upgrading from a previous version, make sure to read the
  :doc:`upgrade <upgrade>` document.

.. _PyPI: https://pypi.python.org/pypi?:action=display&name=luma.oled
