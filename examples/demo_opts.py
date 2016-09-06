import argparse

parser = argparse.ArgumentParser(description='oled arguments')
parser.add_argument(
    '--port', '-p',
    type=int,
    default=1,
    help='i2c bus number',
)
parser.add_argument(
    '--address', '-a',
    type=str,
    default='0x3c',
    help='i2c display address',
)
parser.add_argument(
    '--display', '-d',
    type=str,
    default='ssd1306',
    help='display type, one of ssd1306 or sh1106',
)

args = parser.parse_args()
if args.display not in ('ssd1306', 'sh1106'):
    parser.error('unknown display %s' % args.display)
try:
    args.address = int(args.address, 0)
except ValueError:
    parser.error('invalid address %s' % args.address)

import oled.device
Device = getattr(oled.device, args.display)
device = Device(port=args.port, address=args.address)
