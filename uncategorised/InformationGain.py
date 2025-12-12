from math import log2

def shannon_entropy(args):
    assert sum(args) == 1
    entropy = 0
    for probability in args:
        if probability == 0:
            continue
        entropy += -probability * log2(probability)
    return entropy

def information_gain(node_probs, children_sizes, children_probs):
    assert sum(node_probs) == 1
    assert len(children_sizes) == len(children_probs)

    info_gain = shannon_entropy(node_probs)
    total = sum(children_sizes)
    for i in range(len(children_sizes)):
        info_gain -= (children_sizes[i] / total) * shannon_entropy(children_probs[i])
    return info_gain

# print("Cond2Left", information_gain([27/34, 7/34], [25, 9], [[1, 0],[2/9, 7/9]]))
# print("Cond3Right", information_gain([10/13, 3/13], [9, 4], [[1, 0],[1/4, 3/4]]))
# print("A1", information_gain([3/5, 2/5], [1, 4], [[1, 0], [2/4, 2/4]]))
# print("A2", information_gain([3/5, 2/5], [2, 3], [[1, 0], [1/3, 2/3]]))
# print("A3", information_gain([3/5, 2/5], [3, 2], [[2/3, 1/3], [1/2, 1/2]]))

# print(information_gain([70/160, 60/160, 30/160],[40, 70, 50],[[20/40, 20/40, 0/40],[30/70, 10/70, 30/70],[20/50, 30/50, 0/50]]))
print(shannon_entropy([2/9, 7/9]))
print(shannon_entropy([1/4, 3/4]))