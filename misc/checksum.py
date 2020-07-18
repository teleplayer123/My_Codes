import hashlib
import sys

class Checksum:
    def __init__(self, filename, compare_hash, hash_alg, hex_digest=True):
        self.filename = filename
        self.hash_alg = hash_alg
        self.compare_hash = compare_hash.lower()
        self.hex_digest = hex_digest

    def _checksum(self, filename):
        hsum = None
        if self.hash_alg == "sha256":
            hsum = hashlib.sha256()
        elif self.hash_alg == "sha1":
            hsum = hashlib.sha1()
        elif self.hash_alg == "sha512":
            hsum = hashlib.sha512()
        for byte in self._read_file(filename):
            hsum.update(byte)
        if self.hex_digest is True:
            return hsum.hexdigest()
        else:
            return hsum.digest()

    def _read_file(self, filename):
        bs = 65536
        with open(filename, "rb") as fh:
            block = fh.read(bs)
            while len(block) > 0:
                yield block
                block = fh.read(bs)

    def verify_sum(self, compare_h=None):
        return self._checksum(self.filename) == self.compare_hash

    def sum_value(self):
        return self._checksum(self.filename)


#c = Checksum("/home/csash/Downloads/virtualbox-6.1_6.1.4-136177_Ubuntu_bionic_amd64.deb",
#"929d2e974047be579f9a48a0a0c9130b70933f46bc28a1314bbc2ca68cecc224")
#print(c.verify_sum())
fn = sys.argv[1]
ch = sys.argv[2]
alg = sys.argv[3]
c = Checksum(fn, ch, alg)
print(c.verify_sum())
