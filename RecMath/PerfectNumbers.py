def is_prime(n):
    if n <= 1:
        return False
    f = 2
    while f * f <= n:
        if n % f == 0:
            return False
        f += 1
    return True

for i in range(1, 101):
    mersenne = (1 << i) - 1
    if is_prime(mersenne):
        print(mersenne * 1 << (i - 1))

'''[6,
    28,
    496,
    8128,
    33550336,
    8589869056,
    137438691328,
    2305843008139952128,
    2658455991569831744654692615953842176]'''