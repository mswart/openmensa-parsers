#!python3
from config import providers, parse
import sys

if len(sys.argv) < 3:
    print('usage: {} <provider> <canteen>'.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)
provider = sys.argv[1]
canteen = sys.argv[2]
if provider not in providers:
    print('unknown provider "{}"'.format(provider), file=sys.stderr)
    print('registered provider:\n  {}'.format('\n  '.join(sorted(providers.keys()))), file=sys.stderr)
    sys.exit(2)
if canteen not in providers[provider]['canteens']:
    print('unknown canteen "{}"'.format(canteen), file=sys.stderr)
    print('registered canteen:\n  {}'.format('\n  '.join(sorted(providers[provider]['canteens'].keys()))), file=sys.stderr)
    sys.exit(3)

print(parse(provider, canteen, len(sys.argv) > 3))
