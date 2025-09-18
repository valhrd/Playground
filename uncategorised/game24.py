def compute(lsts, expr, index):
    if index == len(lsts):
        try:
            return [round(eval("".join(expr[:-1])), ndigits=5)]
        except:
            return []
    res = []
    for n in lsts[index]:
        expr.append(str(n))
        for op in "+-*/":
            expr.append(op)
            res.extend(compute(lsts, expr, index + 1))
            expr.pop()
        expr.pop()
    return res

def f(lst):
    n = len(lst)
    if n == 1:
        return list(set([lst[0]]))
    
    values = set()
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            for k in range(j + 1, n + 2):
                temp = [lst[:i], lst[i:j], lst[j:k], lst[k:]]
                temp = [f(l) for l in temp if len(l) > 0]
                for v in set(compute(temp, [], 0)):
                    values.add(v)
    return list(values)

h = {}
for i in range(1,10):
    for j in range(1, 10):
        for k in range(1, 10):
            for l in range(1, 10):
                lst = [i,j,k,l]
                t = tuple(sorted(lst))
                # print(t)
                if t in h and h[t]:
                    continue
                h[t] = (24 in f(lst))
print(h)