from utils import factors

def primes(n=100):
    p = []
    for i in range(2, n):
        if factors(i) == []:
            p.append(i)
    return p

def find_max(primes, n):
    x = 1
    for i in primes:
        if x * i > n:
            return x
        x *= i
print(find_max(primes(55), 1000000))