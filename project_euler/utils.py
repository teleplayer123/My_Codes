from functools import wraps

def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

@memo
def factorial(n):
    if n < 1:
        return 1
    return n * factorial(n-1)

def factors(n):
    f = []
    for i in range(2, n):
        if n % i == 0:
            f.append(i)
    return f

@memo
def gcd(a,b):
    if a == 0:
        return b
    return gcd(b % a, a)

def phi(n):
    result = 1
    for i in range(2, n):
        if(gcd(i, n) == 1):
            result += 1
    return result

def range_primes(n=20):
    p = []
    for i in range(2, n):
        if factors(i) == []:
            p.append(i)
    return p

def prime_factors(n):
    primes = range_primes(n)
    i = 2
    f = []
    while n % 2 == 0:
        f.append(i)
        n /= i
    for j in primes:
        while n % j == 0:
            f.append(j)
            n /= j
    return f

def prime_fact(n, primes):
    p = {}
    p[n] = []
    total = 1
    for i in primes:
        if n % i == 0:
            if i <= n: 
                p[n].append(i)
                total *= i
    return p 