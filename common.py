#!/usr/bin/env python2

from __future__ import print_function
import traceback
import binascii
import sys


def extract_activation_bytes(data):
    try:
        if (b"BAD_LOGIN" in data or b"Whoops" in data) or \
                b"group_id" not in data:
            print(data)
            print("\nActivation failed! ;(")
            sys.exit(-1)
        k = data.rfind(b"group_id")
        l = data[k:].find(b")")
        keys = data[k + l + 1 + 1:]
        output_keys = []
        # each key is of 70 bytes
        for i in range(0, 8):
            key = keys[i * 70 + i:(i + 1) * 70 + i]
            h = binascii.hexlify(bytes(key))
            h = [h[i:i+2] for i in range(0, len(h), 2)]
            h = b",".join(h)
            output_keys.append(h)
    except SystemExit as e:
        sys.exit(e)
    except:
        traceback.print_exc()

    # only 4 bytes of output_keys[0] are necessary for decryption! ;)
    activation_bytes = output_keys[0].replace(b",", b"")[0:8]
    # get the endianness right (reverse string in pairs of 2)
    activation_bytes = "".join(reversed([activation_bytes[i:i+2] for i in
                                         range(0, len(activation_bytes), 2)]))
    print(activation_bytes)
