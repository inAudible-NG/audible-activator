#!/usr/bin/env python

import sys
import common

template = """REGEDIT4

[HKEY_LOCAL_MACHINE\Software\Audible\SWGIDMAP]
"0"=hex:%s
"1"=hex:%s
"2"=hex:%s
"3"=hex:%s
"4"=hex:%s
"5"=hex:%s
"6"=hex:%s
"7"=hex:%s
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <activation.blob / licenseForCustomerToken file>\n"
                         % sys.argv[0])
        sys.exit(-1)

    with open(sys.argv[1], "rb") as f:
        activation_bytes, output = common.extract_activation_bytes(f.read())
        print(activation_bytes)
        print((template % (output[0], output[1], output[2],
                          output[3], output[4], output[5],
                          output[6], output[7])))
