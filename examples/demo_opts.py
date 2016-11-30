import argparse
import oled.device
import oled.serial

parser = argparse.ArgumentParser(description='oled arguments')

parser.add_argument(
    '--port', '-p',
    type=int,
    default=1,
    help='i2c bus number')

parser.add_argument(
    '--address', '-a',
    type=str,
    default='0x3C',
    help='i2c display address')

parser.add_argument(
    '--display', '-d',
    type=str,
    default='ssd1306',
    help='display type, one of: ssd1306, sh1106, capture, pygame')

parser.add_argument(
    '--interface', '-i',
    type=str,
    default='i2c',
    help='serial interface type, one of i2c or spi')

# TODO: Add arguments req'd for SPI

args = parser.parse_args()
if args.display not in ('ssd1306', 'sh1106', 'capture', 'pygame'):
    parser.error('unknown display %s' % args.display)
if args.interface not in ('i2c', 'spi'):
    parser.error('unknown interface %s' % args.interface)
try:
    args.address = int(args.address, 0)
except ValueError:
    parser.error('invalid address %s' % args.address)

Device = getattr(oled.device, args.display)
if args.display in ('ssd1306', 'sh1106'):
    if (args.interface == 'i2c'):
        serial = oled.serial.i2c(port=args.port, address=args.address)
    elif (args.interface == 'spi'):
        serial = oled.serial.spi()
    device = Device(serial)
else:
    device = Device()
