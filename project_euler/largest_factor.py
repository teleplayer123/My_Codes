from utils import factors
import math

n = 600851475143
p = []
for i in range(3, int(math.sqrt(n))):
    if n % i == 0:
        p.append(i)
f = []
for j in p:
    if factors(j) == []:
        f.append(j)
print(max(f))