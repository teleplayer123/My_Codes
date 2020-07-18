#!/usr/bin/env python3

from time import time
import sys



def xdump(data, bs=16, en="utf8"):
    width = (bs * 2) + (bs // 2)
    lines = []
    cols = "BLOCK  BYTES{} {}".format(" " * (width + (width % bs) - 5), en.upper())
    dashes = "{0:-<6} {1:-<{2}}{3}{4}".format("", "", width + (width % bs), " ","-" * (len(en)+1))
    print(cols)
    print(dashes)
    for i in range(0, len(data), bs):
        block_data = data[i:i+bs]
        hexstr = " ".join(["%02x" %ord(x) for x in block_data])
        txtstr = "".join(["%s" %x if 32 <= ord(x) < 256  else "." for x in block_data])
        line = "{:06x} {:48}  {:16}\n".format(i, hexstr, txtstr)
        lines.append(line)
    return "".join([i for i in lines])
