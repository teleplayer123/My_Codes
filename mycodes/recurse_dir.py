import sys
import os
import datetime

def main():
    counts = [0, 0]
    paths = sys.argv[2:]
    filenames = []
    dirnames = []
    for path in paths:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.startswith("."):
                    continue
                fullname = os.path.join(root, name)
                if fullname.startswith("./"):
                    fullname = fullname[2:]
                filenames.append(fullname)
            dirnames.append(dirs)
        counts[0] += len(filenames)
        counts[1] += len(dirnames)
        process_lists(filenames, dirnames)
    print("{0} file{1}, {2} director{3}".format(
          "{0:n}".format(counts[0]) if counts[0] else "no",
          "s" if counts[0] != 1 else "",
          "{0:n}".format(counts[1]) if counts[1] else "no",
          "ies" if counts[1] != 1 else "y"))


def process_lists(filenames, dirnames):
    key_list = []
    opts = sys.argv[1]
    for name in filenames:
        modified = ""
        if opts in {"-m", "-modified"}:
            try:
                modified += (datetime.datetime.fromtimestamp(
                              os.path.getmtime(name))
                                .isoformat(" ") [:19] + " ")
            except EnvironmentError:
                modified += "{0:19}".format("unknown")
        size = ""
        if opts in {"-s", "-size"}:
            try:
                size += "{0:n}".format(os.path.getsize(name))
            except EnvironmentError:
                size += "{0:n}".format("unkown")
        if opts in {"-m", "-modified"}:
            orderkey = modified
        elif opts in {"-s", "-size"}:
            orderkey = size
        else:
            orderkey = name
        key_list.append((orderkey, "{0}".format(name)))
        for line in sorted(key_list):
            print(line)


main()