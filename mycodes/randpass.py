from hashlib import sha256
from random import randint, choice, seed, randrange
import re
import os

chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
"q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 1, 2, 3, 4, 5, 6, 7, 8, 9]

def random_pass(base_str: str="", use_seed: bool=False, p_len: int=10, 
                sym_mix: bool=False, num_sym: int=3) -> str:
    if use_seed is True:
        seed(os.urandom(2048))
    if base_str == "":
        for _ in range(16):
            base_str += str(choice(chars))
    b = int.from_bytes(bytes(base_str.encode()), "little")
    change1 = b >> randint(50, 127) 
    change2 = b << randint(1, 49)
    changed = change1 << 2 & change2
    changed = changed % 357
    p = sha256(changed.to_bytes(8, "little")).hexdigest()
    size = len(p)
    sym = ["!", "@", "#", "$", "%", "^", "&", "*", "~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "~", "`"]
    if size < p_len:
        p += p
    while size > p_len - num_sym:
        s = size // 2
        p1 = p[:-s]
        p2 = p[s:]
        if (size - num_sym) % 5 and s > p_len:
            p = p2 + choice(chars[6:26]) + p1
        else:
            p = p2 + p1
        p = p[:-num_sym]
        size = len(p)
    for _ in range(num_sym):
        if not sym_mix:
            p += choice(sym)
        else:
            i = randrange(2, len(p))
            p = list(p)
            p.insert(i, choice(sym))
            p = "".join(p)
    if not re.match(r"^[A-Za-z]+?", p):
        return random_pass(base_str, use_seed, 
                            p_len, sym_mix, num_sym)
    else:
        return p

r = random_pass(use_seed=True, sym_mix=True)
print(r)