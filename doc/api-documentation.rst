API Documentation
-----------------
.. automodule:: luma.oled
    :members:
    :undoc-members:
    :show-inheritance:

.. inheritance-diagram:: luma.core.device luma.core.mixin luma.core.virtual luma.oled.device

Breaking changes
""""""""""""""""
.. warning::
   Version 2.0.0 was released on 11 January 2017: this came with a rename of the
   project in github from **ssd1306** to **luma.oled** to reflect the changing
   nature of the codebase. It introduces some structural changes to the package
   structure, namely breaking the library up into smaller components and renaming
   existing packages.

   This should largely be restricted to having to update import statements only.
   To upgrade any existing code that uses the old package structure:

   * rename instances of ``oled.device`` to ``luma.oled.device``.
   * rename any other usages of ``oled.*`` to ``luma.core.*``.

   This breaking change was necessary to be able to add different classes of
   devices, so that they could reuse core components.

:mod:`luma.oled.device`
"""""""""""""""""""""""
.. automodule:: luma.oled.device
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:
