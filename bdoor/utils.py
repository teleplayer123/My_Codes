import os
import zipfile

def save_from(dir_path, new_dir_path):
    filename = dir_path.split("/")[-1]
    new_path = os.path.join(new_dir_path, filename)
    file = open(dir_path, "r")
    with open(new_path, "w") as fh:
        for line in file:
            fh.write(line)
    odir = new_dir_path.replace(filename, "")
    file.close()
    if filename in os.listdir(odir):
        return True
    else:
        return False

def save(fname, path):
    new_path = os.path.join(path, fname.filename)
    file = open(fname)
    with open(new_path, "w") as fh:
        for line in file:
            fh.write(line)
    if fname.filename in os.listdir(path):
        return True
    else:
        return False

def create_zip(dir_path: str, zname: str) -> zipfile.ZipFile:
    with zipfile.ZipFile(zname, "w") as zipf:
        for root, _, files in os.walk(dir_path):
            for file in files:
                zipf.write(os.path.join(root, file))
    return zname