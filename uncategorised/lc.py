def generate(ls, fP, sP):
    n = len(ls)
    opps = [(ls[i], ls[n - 1 - i]) for i in range(n // 2)]
    poss = []

    i, j = ls.index(fP), ls.index(sP)
    if i + j == n - 1:
        return poss

    def make(temp, opps, index):
        if index == len(opps):
            poss.append(sorted(temp.copy()))
            return
        
        if fP in opps[index]:
            temp.append(fP)
        elif sP in opps[index]:
            temp.append(sP)
        else:
            temp.append(opps[index][0])
            make(temp, opps, index + 1)
            temp.pop()
            temp.append(opps[index][1])
        make(temp, opps, index + 1)
        temp.pop()
    
    temp = []
    if len(ls) % 2:
        temp.append(ls[n // 2])
    make(temp, opps, 0)
    return poss


def dfs(ls, fP, sP, f):
    ls = list(filter(lambda x: x is not None, ls))
    n = len(ls)
    i, j = ls.index(fP) + 1, ls.index(sP) + 1

    if (i, j) in h[n]:
        return h[n][(i, j)] + 1

    b = True

    poss = generate(ls, fP, sP)
    if not poss:
        b = False
        m = 1

    if b:
        m = f([dfs(p, fP, sP, f) for p in poss])

    h[n][(ls.index(fP) + 1, ls.index(sP) + 1)] = m
    return m + 1


upper = 28
h = {j:{} for j in range(2, upper + 1)}
for n in range(2, upper + 1):
    ls = [i + 1 for i in range(n)]
    for a in range(1, n // 2 + 1):
        for b in range(a + 1, n + 1):
            dfs(ls, a, b, max)
    print(f"Done: n = {n}")
for n in h:
    print(f"{n}: {h[n]},")