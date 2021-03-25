from hashlib import sha256
from random import randint, choice, seed, randrange
import re
import os
import sys


def random_pass(base_str: str="", rand_seed: bool=True, p_len: int=14, 
                sym_mix: bool=True, num_sym: int=3, iterations: int=4) -> str:
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sym = ["!", "@", "#", "$", "%", "^", "&", "*", "~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "~", "`"]
    if rand_seed is True:
        seed(os.urandom(4048))
    else:
        seed(len(base_str))
    if base_str == "":
        for _ in range(16):
            base_str += str(choice(chars))
    b = int.from_bytes(bytes(base_str.encode()), "little")
    n = randint(1,31)
    changed = b << n | b >> (32 - n)
    changed = changed % 357
    p = sha256(changed.to_bytes(8, "big")).hexdigest()
    size = len(p)
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
        p = choice(chars[1:24]) + "".join(p[1:])
    if iterations > 0:
        iterations -= 1
        return random_pass(base_str=base_str, rand_seed=rand_seed,
                        p_len=p_len, sym_mix=sym_mix, num_sym=num_sym, iterations=iterations)
    else:
        return p

r = random_pass(p_len=16, num_sym=3, iterations=4)
print(r)
