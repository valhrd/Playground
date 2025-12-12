from collections import deque, defaultdict

graph = {
    0: [1, 4],
    1: [2],
    2: [3],
    3: [4],
    4: [5,7,9,11],
    5: [6],
    7: [8],
    9: [10],
    11: [12],
    6: [13],
    8: [13],
    10: [13],
    12: [13],
    13: [14]
}

b_graph = {
    0: [1,3],
    1: [2],
    2: [3,5],
    3: [4],
    4: [5]
}

def bfs(graph):
    h = defaultdict(int)
    dq = deque([(0, 0)])
    seen = set()
    while dq:
        curr, count = dq.popleft()
        h[curr] = max(h[curr], count)
        if curr not in graph:
            continue
        for nb in graph[curr]:
            if count + 1 <= h[nb]:
                continue
            t = (nb, count + 1)
            if t in seen:
                continue
            dq.append(t)
            seen.add(t)
    
    return h

h = bfs(b_graph)
processed = defaultdict(lambda: [])
for k, v in h.items():
    processed[v].append(k)

for k, v in sorted(processed.items()):
    print('-' * 60)
    print(v)