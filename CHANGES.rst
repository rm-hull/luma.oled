ChangeLog
---------

+------------+---------------------------------------------------------------------+------------+
| Version    | Description                                                         | Date       |
+============+=====================================================================+============+
| *Upcoming* | * Support for 16-bit color OLED (SSD1331)                           |            |
|            | * Viewport/scrolling support                                        |            |
|            | * Remove pygame as an install dependency in setup                   |            |
|            | * Ensure SH1106 device collapses color images to monochrome         |            |
|            | * Fix for emulated devices: do not need cleanup                     |            |
|            | * Fix to allow gifanim emulator to process 1-bit images             |            |
|            | * Establish a single threadpool for all virtual viewports           |            |
|            | * Fix issue that prevents multiple threads from running concurently |            |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
| **1.2.0**  | * Add support for 128x32, 96x16 OLED screens (SSD1306 chipset only) | 2016/12/08 |
|            | * Fix boundary condition error when supplying max-frames to gifanim |            |
|            | * Bit pattern calc rework when conveting color -> monochrome        |            |
|            | * Approx 20% performance improvement in ``display`` method          |            |
+------------+---------------------------------------------------------------------+------------+
| **1.1.0**  | * Add animated-GIF emulator                                         | 2016/12/05 |
|            | * Add color-mode flag to emulator                                   |            |
|            | * Fix regression in SPI interface                                   |            |
|            | * Rename emulator transform option 'scale' to 'identity'            |            |
+------------+---------------------------------------------------------------------+------------+
| **1.0.0**  | * Add HQX scaling to capture and pygame emulators                   | 2016/12/03 |
|            | * SPI support (**NOTE:** contains breaking changes)                 |            |
|            | * Improve benchmarking examples                                     |            |
|            | * Fix resource leakage & noops on emulated devices                  |            |
|            | * Additional tests                                                  |            |
+------------+---------------------------------------------------------------------+------------+
| **0.3.5**  | * Pygame-based device emulator & screen capture device emulator     | 2016/11/30 |
|            | * Add bouncing balls demo, clock & Space Invaders examples          |            |
|            | * Auto cleanup on exit                                              |            |
|            | * Add ``bounding_box`` attribute to devices                         |            |
|            | * Demote buffer & pages attributes to "internal use" only           |            |
|            | * Replaced SH1106 data sheet with version that is not "preliminary" |            |
|            | * Add font attribution                                              |            |
|            | * Tests for SSD1306 & SSH1106 devices                               |            |
|            | * Add code coverage & upload to coveralls.io                        |            |
|            | * flake8 code compliance                                            |            |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
| **0.3.4**  | * Performance improvements - render speeds ~2x faster               | 2016/11/15 |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
| **0.3.3**  | * Add PyPi badge                                                    | 2016/11/15 |
|            | * Use smbus2                                                        |            |
+------------+---------------------------------------------------------------------+------------+
| **0.3.2**  | * Fix bug in maze example (integer division on python 3)            | 2016/11/13 |
|            | * Use latest pip                                                    |            |
|            | * Add tox & travis config (+ badge)                                 |            |
|            | * Add RTFD config                                                   |            |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
| **0.3.1**  | * Adjust requirements (remove smbus)                                | 2016/11/13 |
|            | * Default RTFD theme                                                |            |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
| **0.3.0**  | * Allow SMBus implementation to be supplied                         | 2016/11/13 |
|            | * Add show, hide and clear methods                                  |            |
|            | * Catch & rethrow ``IOError`` exceptions                            |            |
|            | * Fix error in 'hello world' example                                |            |
|            | * Cleanup imports                                                   |            |
|            | * Allow setting width/height                                        |            |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
| **0.2.0**  | * Add Python 3 support                                              | 2016/09/06 |
|            | * Add options to demos                                              |            |
|            | * Micro-optimizations                                               |            |
|            | * Remove unused optional arg                                        |            |
|            | * Fix bug in rendering image data                                   |            |
|            | * Added more examples                                               |            |
|            | * Add setup file                                                    |            |
|            | * Support SH1106                                                    |            |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
