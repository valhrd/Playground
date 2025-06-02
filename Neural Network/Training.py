from NetworkCreator import *
from Layer import Layer
import random

trainingData = [1, 0]

nn = Network(10, 3, 25, 2)
nn.createNetwork()
nn.setInputLayer([0,0,0,0,0,0,0,0,0,1])
nn.forwardPass()

for inverse_rate in range(1, 1001):
    nn.backPropagation(trainingData, 1 / inverse_rate)
    nn.forwardPass()

nn.forwardPass()
print(nn.getOutput())