import sys
import logging
import argparse

import oled.device
import oled.emulator
import oled.serial


parser = argparse.ArgumentParser(description='oled arguments',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--display', '-d', type=str, default='ssd1306', help='Display type, one of: ssd1306, ssd1331, sh1106, capture, pygame, qt, gifanim')
parser.add_argument('--width', type=int, default=128, help='Width of the device in pixels')
parser.add_argument('--height', type=int, default=64, help='Height of the device in pixels')
parser.add_argument('--interface', '-i', type=str, default='i2c', help='Serial interface type, one of: i2c, spi')
parser.add_argument('--i2c-port', type=int, default=1, help='I2C bus number')
parser.add_argument('--i2c-address', type=str, default='0x3C', help='I2C display address')
parser.add_argument('--spi-port', type=int, default=0, help='SPI port number')
parser.add_argument('--spi-device', type=int, default=0, help='SPI device')
parser.add_argument('--spi-bus-speed', type=int, default=8000000, help='SPI max bus speed (Hz)')
parser.add_argument('--bcm-data-command', type=int, default=24, help='BCM pin for D/C RESET (SPI devices only)')
parser.add_argument('--bcm-reset', type=int, default=25, help='BCM pin for RESET (SPI devices only)')
parser.add_argument('--transform', type=str, default='scale2x', help='Scaling transform to apply, one of: none, identity, scale2x, smoothscale (emulator only)')
parser.add_argument('--scale', type=int, default=2, help='Scaling factor to apply (emulator only)')
parser.add_argument('--mode', type=str, default='RGB', help='Colour mode, one of: 1, RGB, RGBA (emulator only)')
parser.add_argument('--duration', type=float, default=0.01, help='Animation frame duration (gifanim emulator only)')
parser.add_argument('--loop', type=int, default=0, help='Repeat loop, zero=forever (gifanim emulator only)')
parser.add_argument('--max-frames', type=int, help='Maximum frames to record (gifanim emulator only)')

# logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s - %(message)s'
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)

args = parser.parse_args()
if args.display in ('ssd1306', 'ssd1331', 'sh1106'):
    if args.interface not in ('i2c', 'spi'):
        parser.error('unknown interface %s' % args.interface)

    try:
        args.i2c_address = int(args.i2c_address, 0)
    except ValueError:
        parser.error('invalid address %s' % args.i2c_address)

    Device = getattr(oled.device, args.display)
    if (args.interface == 'i2c'):
        serial = oled.serial.i2c(port=args.i2c_port, address=args.i2c_address)
    elif (args.interface == 'spi'):
        serial = oled.serial.spi(port=args.spi_port,
                                 device=args.spi_device,
                                 bus_speed_hz=args.spi_bus_speed,
                                 bcm_DC=args.bcm_data_command,
                                 bcm_RST=args.bcm_reset)
    device = Device(serial, width=args.width, height=args.height)

elif args.display in ('capture', 'pygame', 'gifanim'):
    Emulator = getattr(oled.emulator, args.display)
    device = Emulator(**vars(args))

elif args.display in ('qt',):
    from oled.emulator.qt import QtEmulator
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    """
    window = QtWidgets.QMainWindow()

    button = QtWidgets.QPushButton("Hello SSD1306!")
    button.clicked.connect(on_click)

    window.setCentralWidget(button)
    window.show()

    app.exec_()
    """
    device = QtEmulator(**vars(args))

else:
    parser.error('unknown display %s' % args.display)
