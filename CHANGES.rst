ChangeLog
---------

+------------+---------------------------------------------------------------------+
| Version    | Description                                                         |
+============+=====================================================================+
| *Upcoming* | * Improve benchmarking examples                                     |
|            | * Fix resource leakage on emulated devices                          |
+------------+---------------------------------------------------------------------+
| **0.3.5**  | * Pygame-based device emulator & screen capture device emulator     |
|            | * Add bouncing balls demo, clock & Space Invaders examples          |
|            | * Auto cleanup on exit                                              |
|            | * Add bounding_box attribute to devices                             |
|            | * Demote buffer & pages attributes to "internal use" only           |
|            | * Replaced SH1106 data sheet with version that is not "preliminary" |
|            | * Add font attribution                                              |
|            | * Tests for SSD1306 & SSH1106 devices                               |
|            | * Add code coverage & upload to coveralls.io                        |
|            | * flake8 code compliance                                            |
|            | * Documentation updates                                             |
+------------+---------------------------------------------------------------------+
| **0.3.4**  | * Performance improvements - render speeds ~2x faster               |
|            | * Documentation updates                                             |
+------------+---------------------------------------------------------------------+
| **0.3.3**  | * Add PyPi badge                                                    |
|            | * Use smbus2                                                        |
+------------+---------------------------------------------------------------------+
| **0.3.2**  | * Fix bug in maze example (integer division on python 3)            |
|            | * Use latest pip                                                    |
|            | * Add tox & travis config (+ badge)                                 |
|            | * Add RTFD config                                                   |
|            | * Documentation updates                                             |
+------------+---------------------------------------------------------------------+
| **0.3.1**  | * Adjust requirements (remove smbus)                                |
|            | * Default RTFD theme                                                |
|            | * Documentation updates                                             |
+------------+---------------------------------------------------------------------+
| **0.3.0**  | * Allow SMBus implementation to be supplied                         |
|            | * Add show, hide and clear methods.                                 |
|            | * Catch & rethrow IOErrors                                          |
|            | * Fix error in 'hello world' example                                |
|            | * Cleanup imports                                                   |
|            | * Allow setting width/height                                        |
|            | * Documentation updates                                             |
+------------+---------------------------------------------------------------------+
| **0.2.0**  | * Add python3 support                                               |
|            | * Add options to demos                                              |
|            | * Micro-optimizations                                               |
|            | * Remove unused optional arg                                        |
|            | * Fix bug in rendering image data                                   |
|            | * Added more examples                                               |
|            | * Add setup file                                                    |
|            | * Support SH1106                                                    |
|            | * Documentation updates                                             |
+------------+---------------------------------------------------------------------+
