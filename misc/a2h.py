import sys
import re

def a2h(s):
    h = []
    for i in s[:]:
        h.append("%02x" % ord(i))
    return "\\x".join(h)

def rev_a2h(s):
    if not re.match(r"^\\x", s):
        hs = a2h(s)
    else:
        hs = s
    rhs = ""
    odd = False
    obit = ""
    r = hs.split("\\x")
    if len(r) % 2 != 0:
        obit = r[0:1]
        r = r[1:]
        odd = True
    for i in range(len(r)-1, -1, -1):
        rhs += "\\x" + r[i]
    if odd:
        rhs += obit[0]
    return rhs

flags = {"-h", "-r"}
f, s = sys.argv[1], sys.argv[2]

if len(sys.argv) < 3 or f not in flags:
    print("""Usage: %prog [options] [string]

            options: -h  string to hex
                     -r  string to hex little endian""")
    sys.exit(0)

if f in {"-h"}:
    print(a2h(str(s)))
elif f in {"-r"}:
    print(rev_a2h(str(s)))
else:
    print("Invalid Input")
    sys.exit(0)

