import sys
import zlib

with open(sys.argv[1], 'r') as f:
    z = f.read()

print repr(zlib.decompress(z))


