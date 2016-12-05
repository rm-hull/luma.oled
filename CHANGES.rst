ChangeLog
---------

+------------+---------------------------------------------------------------------+------------+
| Version    | Description                                                         | Date       |
+============+=====================================================================+============+
| *Upcoming* | *TBD*                                                               |            |
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
