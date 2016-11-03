#!/usr/bin/env python2

# Parser for AudibleActivation.sys files

import sys
import binascii
import struct

# AudibleActivation.sys file format
#
# Each "line" is of 70 bytes

# First 4 bytes are the "activation_bytes"
#  "FFFFFFFF" pattern implies that the slot is not in use

# Next two bytes are the activation slot number (0 to 7)
#
# These observations also apply to the "SWGIDMAP" registry key, and the binary
# blob that is transferred during the online activation process!


def extract_activation_bytes(filename):

    with open(filename, "rb") as f:
        odata = f.read(4)
        mdata = struct.pack(">i", struct.unpack("<i", odata)[0])
        sys.stdout.write(binascii.hexlify(mdata) + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <path of AudibleActivation.sys>\n" %
                         sys.argv[0])
        sys.exit(-1)

    extract_activation_bytes(sys.argv[1])
