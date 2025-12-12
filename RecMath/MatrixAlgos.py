from typing import List

def determinant(matrix: List[List[int]]) -> int:
    assert len(matrix) == len(matrix[0])
    
    n = len(matrix)
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
    
    det = 0
    flip = 1
    for i in range(n):
        submatrix = []
        for j in range(n):
            if i != j:
                submatrix.append(matrix[j][1:])
        det += matrix[i][0] * flip * determinant(submatrix)
        flip = -flip
    return det

mat = [
    [1,10,2,0],
    [0,1,0,0],
    [0,5,1,0],
    [0,0,0,1]
]

def inverse(matrix: List[List[int]]) -> List[List[int]]:
    assert len(matrix) == len(matrix[0])
    
    det = determinant(matrix)
    if det == 0:
        return None

    n = len(matrix)
    if n == 2:
        return [[1 / det * matrix[1][1], -1 / det * matrix[0][1]],[-1 / det * matrix[1][0], 1 / det * matrix[0][0]]]

mat = [
    [1,2],
    [3,4]
]
print(inverse(mat))