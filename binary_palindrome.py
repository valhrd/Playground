def generate(n):

    res = []
    def dfs(s, index):
        if index >= n:
            return
        res.append(s + s[::-1])
        res.append(s + '0' + s[::-1])
        res.append(s + '1' + s[::-1])
        dfs(s + '0', index + 1)
        dfs(s + '1', index + 1)
    
    dfs("1", 0)
    return res

t = generate(20)
print(sorted(set([int(b, 2) for b in t if b])))