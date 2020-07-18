def palindromic(n):
    k = str(n)
    s = sum(int(i)**2 for i in k)
    if k[0] != k[-1]:
        if s < 10 and n % 10 != 0:
            return n
    else:
        return

def is_palindrome(n):
    s = str(n)
    r = ""
    for i in range(len(s)-1, -1, -1):
        r += s[i]
    if s == r:
        return True
    else:
        return False

m = 0
for i in range(999, 99, -1):
    for j in range(i, (i//10)-1, -1):
        n = i * j
        if is_palindrome(n):
            if n > m:
                m = n
print(m)