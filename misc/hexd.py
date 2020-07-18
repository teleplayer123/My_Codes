#!/usr/bin/env python3

import os
from time import time
import sys

def xdump(filename, bs=16, en="utf8", outfile="hexdump{}.txt"):
    logdir = "/home/csash/dumplogs"
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logf = os.path.join(logdir, outfile.format(str(time()).split(".")[0][:5]))
    width = (bs * 2) + (bs // 2)
    lines = []
    i = 0
    cols = "BLOCK  BYTES{} {}".format(" " * (width + (width % bs) - 5), en.upper())
    dashes = "{0:-<6} {1:-<{2}}{3}{4}".format("", "", width + (width % bs), " ","-" * (len(en)+1))
    with open(logf, "w", encoding=en) as fh:
        fh.write(cols+"\n")
        fh.write(dashes+"\n")
        for block_data in reader(filename, bs):
            hexstr = " ".join(["%02x" %ord(chr(x)) for x in block_data])
            txtstr = "".join(["%s" %chr(x) if 32 <= ord(chr(x)) <= 127  else "." for x in block_data])
            line = "{:06x} {:48}  {}\n".format(i, hexstr, txtstr)
            lines.append(line)
            i += 1
        fh.write("".join([x for x in lines]))
    return "".join([i for i in lines])

def reader(filename, bs):
    with open(filename, "rb") as fh:
        block = fh.read(bs)
        while len(block) > 0:
            yield block
            block = fh.read(bs)

infile = sys.argv[1]
xd = xdump(infile)
print("logged in folder /home/csash/dumplogs")
print(xd)
