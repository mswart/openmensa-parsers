#!python3
from config import providers, parse
import sys

if len(sys.argv) < 3:
    print('usage: {} <provider> <canteen>'.format(sys.argv[0]), file=sys.stderr)
provider = sys.argv[1]
canteen = sys.argv[2]
if provider not in providers:
    print('unknown provider', file=sys.stderr)
    print('registered provider:\n{}'.format('\n'.join(sorted(providers.keys()))), file=sys.stderr)
if canteen not in providers[provider]['canteens']:
    print('unknown canteen', file=sys.stderr)
    print('registered canteen:\n{}'.format('\n'.join(sorted(providers[provider]['canteens'].keys()))), file=sys.stderr)

print(parse(provider, canteen))
