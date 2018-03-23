ChangeLog
---------

+------------+---------------------------------------------------------------------+------------+
| Version    | Description                                                         | Date       |
+============+=====================================================================+============+
| **2.3.2**  | * Support for 96x96 color OLED (SSD1351)                            | 2018/03/03 |
+------------+---------------------------------------------------------------------+------------+
| **2.3.1**  | * Changed version number to inside ``luma/oled/__init__.py``        | 2017/11/23 |
+------------+---------------------------------------------------------------------+------------+
| **2.3.0**  | * Support for 128x128 color OLED (SSD1351)                          | 2017/10/30 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.12** | * Explicitly state 'UTF-8' encoding in setup when reading files     | 2017/10/18 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.11** | * Update dependencies                                               | 2017/09/19 |
|            | * Additional troubleshooting documentation                          |            |
+------------+---------------------------------------------------------------------+------------+
| **2.2.10** | * Add support for 128x32 mode for SH1106                            | 2017/05/01 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.9**  | * luma.core 0.9.0 or newer is required now                          | 2017/04/22 |
|            | * Documentation amends                                              |            |
+------------+---------------------------------------------------------------------+------------+
| **2.2.8**  | * SSD1331 & SSD1322 framebuffer & API docstrings                    | 2017/04/13 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.7**  | * Add support for 64x32 SSD1306 OLED                                | 2017/04/12 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.6**  | * Add support for 64x48 SSD1306 OLED                                | 2017/03/30 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.5**  | * Restrict exported Python symbols from ``luma.oled.device``        | 2017/03/02 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.4**  | * Tweaked SSD1325 init settings & replaced constants                | 2017/02/17 |
|            | * Update dependencies                                               |            |
+------------+---------------------------------------------------------------------+------------+
| **2.2.3**  | * Monochrome rendering on SSD1322 & SSD1325                         | 2017/02/14 |
+------------+---------------------------------------------------------------------+------------+
| **2.2.2**  | * SSD1325 performance improvements (perfloop: 25.50 --> 34.31 FPS)  | 2017/02/02 |
|            | * SSD1331 performance improvements (perfloop: 34.64 --> 51.89 FPS)  |            |
+------------+---------------------------------------------------------------------+------------+
| **2.2.1**  | * Support for 256x64 4-bit greyscale OLED (SSD1322)                 | 2017/01/29 |
|            | * Improved API documentation (shows inherited members)              |            |
+------------+---------------------------------------------------------------------+------------+
| **2.1.0**  | * Simplify/optimize SSD1306 display logic                           | 2017/01/22 |
+------------+---------------------------------------------------------------------+------------+
| **2.0.1**  | * Moved examples to separate git repo                               | 2017/01/15 |
|            | * Add notes about breaking changes                                  |            |
+------------+---------------------------------------------------------------------+------------+
| **2.0.0**  | * Package rename to ``luma.oled`` (**Note:** Breaking changes)      | 2017/01/11 |
+------------+---------------------------------------------------------------------+------------+
| **1.5.0**  | * Performance improvements for SH1106 driver (2x frame rate!)       | 2017/01/09 |
|            | * Support for 4-bit greyscale OLED (SSD1325)                        |            |
|            | * Landscape/portrait orientation with rotate=N parameter            |            |
+------------+---------------------------------------------------------------------+------------+
| **1.4.0**  | * Add savepoint/restore functionality                               | 2016/12/23 |
|            | * Add terminal functionality                                        |            |
|            | * Canvas image dithering                                            |            |
|            | * Additional & improved examples                                    |            |
|            | * Load config settings from file (for examples)                     |            |
|            | * Universal wheel distribution                                      |            |
|            | * Improved/simplified error reporting                               |            |
|            | * Documentation updates                                             |            |
+------------+---------------------------------------------------------------------+------------+
| **1.3.1**  | * Add ability to adjust brightness of screen                        | 2016/12/11 |
|            | * Fix for wrong value NORMALDISPLAY for SSD1331 device              |            |
+------------+---------------------------------------------------------------------+------------+
| **1.3.0**  | * Support for 16-bit color OLED (SSD1331)                           | 2016/12/11 |
|            | * Viewport/scrolling support                                        |            |
|            | * Remove pygame as an install dependency in setup                   |            |
|            | * Ensure SH1106 device collapses color images to monochrome         |            |
|            | * Fix for emulated devices: do not need cleanup                     |            |
|            | * Fix to allow gifanim emulator to process 1-bit images             |            |
|            | * Establish a single threadpool for all virtual viewports           |            |
|            | * Fix issue preventing multiple threads from running concurrently   |            |
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
