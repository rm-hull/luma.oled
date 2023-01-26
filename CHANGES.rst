ChangeLog
---------

+------------+---------------------------------------------------------------------+------------+
| Version    | Description                                                         | Date       |
+============+=====================================================================+============+
| **3.11.0** | * Add support for SH1107 greyscale OLED                             | 2023/01/26 |
+------------+---------------------------------------------------------------------+------------+
| **3.10.0** | * Fix SSD1322 NHD initialization and encode each pixel as 4bit+4bit | 2022/11/14 |
|            |   identical nibbles                                                 |            |
+------------+---------------------------------------------------------------------+------------+
| **3.9.0**  | * Use native namespace package configuration                        | 2022/10/19 |
|            | * Drop support for Python 3.6                                       |            |
+------------+---------------------------------------------------------------------+------------+
| **3.8.1**  | * Fix mutable default parameter bug when using multiple displays    | 2020/11/15 |
+------------+---------------------------------------------------------------------+------------+
| **3.8.0**  | * Improved diff_to_previous framebuffer performance                 | 2020/11/06 |
+------------+---------------------------------------------------------------------+------------+
| **3.7.0**  | * Drop support for Python 3.5, only 3.6 or newer is supported now   | 2020/10/25 |
|            | * Add support for SSD1351 128x96 display                            |            |
|            | * Pin luma.core to 1.x.y line only, in anticipation of performance  |            |
|            |   improvements in upcoming major release                            |            |
+------------+---------------------------------------------------------------------+------------+
| **3.6.0**  | * Add support for Winstar OLED displays                             | 2020/09/24 |
+------------+---------------------------------------------------------------------+------------+
| **3.5.0**  | * Drop support for Python 2.7, only 3.5 or newer is supported now   | 2020/07/04 |
+------------+---------------------------------------------------------------------+------------+
| **3.4.0**  | * Add support for SSD1362 256x64 Greyscale OLED                     | 2020/01/19 |
+------------+---------------------------------------------------------------------+------------+
| **3.3.0**  | * Namespace fix                                                     | 2019/06/19 |
+------------+---------------------------------------------------------------------+------------+
| **3.2.1**  | * Fix bug where SSD1325 ``framebuffer=diff_to_prev`` didn't set     | 2019/04/30 |
|            |   column address properly, resulting in garbled output              |            |
+------------+---------------------------------------------------------------------+------------+
| **3.2.0**  | * Add support for 128x64 OLED (Newhaven SSD1322_NHD))               | 2019/04/17 |
+------------+---------------------------------------------------------------------+------------+
| **3.1.1**  | * Fix bug where SSD1327 ``framebuffer=diff_to_prev`` didn't set     | 2019/03/30 |
|            |   column address properly, resulting in garbled output              |            |
|            | * Minor API documentation improvements                              |            |
+------------+---------------------------------------------------------------------+------------+
| **3.1.0**  | * Add support for 128x64 monochrome OLED (SSD1309)                  | 2018/12/21 |
+------------+---------------------------------------------------------------------+------------+
| **3.0.1**  | * Fix bug where SSD1325/1327 didn't handle ``framebuffer`` properly | 2018/12/21 |
+------------+---------------------------------------------------------------------+------------+
| **3.0.0**  | * **BREAKING** Fix SSD1351 init sequence didn't set RGB/BGR color   | 2018/12/02 |
|            |   order properly. Users of this device should verify proper color   |            |
|            |   rendering and add ``bgr=True`` if blue/red color components       |            |
|            |   appear to be reversed                                             |            |
|            | * Device consolidation - greyscale and colour SSD13xx devices now   |            |
|            |   share common base classes.                                        |            |
+------------+---------------------------------------------------------------------+------------+
| **2.5.1**  | * Fix bug where SSD1331/1351 didn't render green accurately         | 2018/09/14 |
+------------+---------------------------------------------------------------------+------------+
| **2.5.0**  | * Add support form 128x128 Monochrome OLED (SH1106) (by @Gadgetoid) | 2018/09/07 |
|            | * Dependency and documentation updates                              |            |
|            | * Minor packaging changes                                           |            |
+------------+---------------------------------------------------------------------+------------+
| **2.4.1**  | * Fix bug where SSD1327 init sequence exceeds serial command size   | 2018/05/28 |
+------------+---------------------------------------------------------------------+------------+
| **2.4.0**  | * Support for 128x128 4-bit OLED (SSD1327)                          | 2018/04/18 |
+------------+---------------------------------------------------------------------+------------+
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
