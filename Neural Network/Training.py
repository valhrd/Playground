from NetworkCreator import *
from Layer import Layer
import random

trainingData = [[1 if i == j else 0 for i in range(10)] for j in range(10)]
trainingOutput = [1 / 10 for _ in range(10)]

nn = Network(10, 3, 25, 2)
nn.createNetwork()
nn.forwardPass()

for _ in range(100):
    for td in trainingData:
        nn.forwardPass()
    nn.backPropagation(trainingData, 0.5)
    nn.forwardPass()

nn.forwardPass()
print(nn.getOutput().layer)