import numpy as np

def pagerank(
    graph: list[list[int]],
    beta: float = 0.85,
    specific: list[int] = None,
    threshold: float = 1e-6,
) -> np.array:
    n = len(graph)
    assert 0 <= beta <= 1
    if specific is not None:
        assert all(0 <= v < n for v in specific)
    for nbs in graph:
        for nb in nbs:
            if not 0 <= nb < n:
                assert False

    mat = np.zeros((n, n))
    for i in range(n):
        if not graph[i]:
            mat[:, i] += beta / n
        else:
            mat[list(set(graph[i])), i] += beta / len(graph[i])
    
    if specific is None:
        overlay = np.ones((n, n))
        mat += overlay * (1 - beta) / n
    else:
        overlay = np.zeros((n, n))
        indices = np.array(specific)
        overlay[indices] = 1
        mat += overlay * (1 - beta) / len(set(specific))
    print(f'PageRank matrix formed:\n{mat}')

    # Pagerank iteration
    iterations = 0
    prev = None
    curr = np.ones(n) / n
    def mae(curr: np.array, prev: np.array) -> float:
        if prev is None:
            return float('inf')
        return np.mean(np.abs(curr - prev))

    while mae(curr, prev) > threshold:
        iterations += 1
        prev = curr
        curr = mat @ curr
    print(f'Solution: {curr} | Iterations {iterations}')
    return curr

if __name__ == '__main__':
    # graph = [[1,2], [2], [0]]
    # graph = [[1,2], [2], [2]]
    # graph = [[1,2], [0], [3], [2]]
    # graph = [[1,2], [2], []]
    graph = [[1,2],[0],[3],[2]]
    pagerank(graph, beta=0.8, specific=[0])