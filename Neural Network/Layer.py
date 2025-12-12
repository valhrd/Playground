from Neuron import Neuron
import numpy as np
import random

class Layer:
    def __init__(self, neuronCount, input, output):
        self.layer = [Neuron(index, 0, 0 if input else random.randrange(-10, 11), output=True if output else False) for index in range(neuronCount)]
        self.size = neuronCount
        self.output = output

        self.prevLayer = []
        self.prevWeightMatrix = [[]]

        self.nextLayer = []
        self.nextWeightMatrix = [[]]
    
    def setInput(self, layerRepresentation):
        if len(layerRepresentation) != self.size:
            print("Layer sizes do not match!")
            return
        temp = []
        for index in range(len(layerRepresentation)):
            temp.append(Neuron(index, layerRepresentation[index], 0, False))
        self.layer = temp
    
    def attachPrevLayer(self, layer, weights):
        self.prevLayer = layer
        self.prevWeightMatrix = weights

    def attachNextLayer(self, layer, weights):
        self.nextLayer = layer
        self.nextWeightMatrix = weights
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def softmax(self):
        total = 0
        for neuron in self.layer:
            total += np.exp(neuron.val)
        for neuron in self.layer:
            neuron.softmax = np.exp(neuron.val) / total

    def evaluateLayer(self):
        for neuron in self.layer:
            neuron.val = self.sigmoid(sum([self.prevLayer.layer[k].val * self.prevWeightMatrix[neuron.index][k] for k in range(self.prevLayer.size)]) + neuron.bias)
        if self.output:
            self.softmax()