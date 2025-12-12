from collections import Counter

def create_palindromes(counter):
    odds = sum([1 for k in counter if k % 2])
    if odds > 1:
        return []

    odd = [k for k in counter if k % 2][0] if odds else None
    for k in counter:
        counter[k] //= 2

    res = []
    def dfs(temp, c):
        if all(v == 0 for v in c.values()):
            s = "".join(temp)
            if odd:
                res.append(s + str(odd) + s[::-1])
                return
            res.append(s + s[::-1])
            return

        for k in c:
            if c[k] == 0:
                continue
            c[k] -= 1
            temp.append(str(k))
            dfs(temp, c)
            c[k] += 1
            temp.pop()
    
    dfs([], counter)
    return res


res = []
def outer_dfs(curr, h):
    if curr == 10:
        if sum(h.values()) > 17:
            return
        temp = Counter()
        temp += h
        res.extend(create_palindromes(temp))
        return
    h[curr] = curr
    outer_dfs(curr + 1, h)
    h.pop(curr)
    outer_dfs(curr + 1, h)


outer_dfs(1, Counter())
print(sorted([int(v) for v in res if v]))