from utils import gcd, range_primes

#smallest multiple
def lcm(n):
    m = 1
    for i in range(1, n+1):
        m *= (i / gcd(m, i))
    return m

#10001 prime
def seive(n):
    p = [True for _ in range(n+1)]
    i = 2
    while i**2 <= n:
        if p[i] == True:
            for j in range(i**2, n+1, i):
                p[j] = False
        i += 1
    primes = []
    for i in range(2, n+1):
        if p[i] is True:
            primes.append(i)
    return primes

#print(seive(104750)[-1])
primes = seive(2000000)

#pythagorean triplet a**2 + b**2 = c**2