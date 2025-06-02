def collatz(n: int):
    if n < 1:
        return
    steps = 0
    while n > 1:
        if n % 2:
            n = 3 *n + 1
        else:
            n //= 2
        steps += 1
    return steps

for i in range(1000):
    print(collatz(i))