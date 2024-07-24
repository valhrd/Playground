import numpy as np
import random

class Neuron:
    def __init__(self, index, val, bias):
        self.val = val
        self.index = index
        self.bias = bias

        self.prevLayer = []
        self.prevWeightMatrix = [[]]

        self.nextLayer = []
        self.nextWeightMatrix = [[]]
    
    def __repr__(self):
        return f"<{self.val}>"

    def attachPrevLayer(self, nodeList, weightMatrix):
        self.prevLayer = nodeList
        self.prevWeightMatrix = weightMatrix
    
    def attachNextLayer(self, nodeList, weightMatrix):
        self.nextLayer = nodeList
        self.nextWeightMatrix = weightMatrix

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def evaluate(self):
        self.val = self.sigmoid(sum([self.prevLayer[i].val * self.prevWeightMatrix[i][self.index] for i in range(len(self.prevLayer))]) - self.bias)