def kaprekar(n, digits):
    seen = set()
    steps = -1
    while n not in seen:
        seen.add(n)
        integer = list(str(n))
        while len(integer) < digits:
            integer.append('0')
        integer.sort()
        smallest = "".join(integer)
        biggest = smallest[::-1]
        n = int(biggest) - int(smallest)
        steps += 1
    final.add(n)
    # return steps

final = set()
for k in range(1, 7):
    for i in range(10 ** (k - 1), 10 ** k):
        kaprekar(i, k)
    print(final)
    final = set()