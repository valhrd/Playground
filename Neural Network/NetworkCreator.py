from Neuron import Neuron
from Layer import Layer
import random

class Network:

    def __init__(self, inputLayerSize, hiddenLayerCount, hiddenLayerSize, outputLayerSize):
        self.inputLayer = Layer(inputLayerSize, True, False)
        self.inputLayerSize = inputLayerSize
        self.hiddenLayerCount = hiddenLayerCount
        self.hiddenLayerSize = hiddenLayerSize
        self.outputLayerSize = outputLayerSize

        self.hiddenGroup = None
        self.outputLayer = None

    def setInputLayer(self, trainingInput):
        self.inputLayer.setInput(trainingInput)

    def getOutput(self):
        return self.outputLayer.layer

    def createNetwork(self):
        outputLayer = Layer(self.outputLayerSize, False, True)
        self.outputLayer = outputLayer
        hiddenGroup = self.createHiddenGroup()
        self.attachInputToHidden(self.inputLayer, hiddenGroup)
        self.attachHiddenToOutput(hiddenGroup, outputLayer)

    def forwardPass(self):
        self.evaluateLayers()

    def createHiddenGroup(self):
        hiddenGroup = [Layer(self.hiddenLayerSize, False, False) for _ in range(self.hiddenLayerCount)]
        for i in range(self.hiddenLayerCount - 1):
            self.attachWeightToLayers(hiddenGroup[i], hiddenGroup[i + 1])
        self.hiddenGroup = hiddenGroup
        return hiddenGroup

    def attachWeightToLayers(self, start, next):
        weights = [[random.uniform(-10, 10) for _ in range(start.size)] for _ in range(next.size)]
        start.nextLayer = next
        next.prevLayer = start
        start.nextWeightMatrix = next.prevWeightMatrix = weights

    def attachInputToHidden(self, inputLayer, hiddenGroup):
        if not hiddenGroup:
            print("Empty hidden group")
            return
        self.attachWeightToLayers(inputLayer, hiddenGroup[0])

    def attachHiddenToOutput(self, hiddenGroup, outputLayer):
        if not hiddenGroup:
            print("Empty hidden group")
            return
        self.attachWeightToLayers(hiddenGroup[-1], outputLayer)
        
    def evaluateLayers(self):
        for hiddenLayer in self.hiddenGroup:
            hiddenLayer.evaluateLayer()
        self.outputLayer.evaluateLayer()

    def backPropagation(self, data, learningRate):
        if self.outputLayer.size != len(data):
            print(f"Invalid data: Output size of {self.outputLayer.size}, Data size of {len(data)}")
        self.outputBackPropagation(data, learningRate)

    def outputBackPropagation(self, data, learningRate):
        prevWeightMatrix = self.outputLayer.prevWeightMatrix
        nextData = [0 for i in range(self.outputLayer.prevLayer.size)]
        for neuron in self.outputLayer.layer:
            meanSquareDeriv = neuron.softmax - data[neuron.index]
            softmaxDeriv = neuron.softmax * (1 - neuron.softmax)
            actFuncDeriv = neuron.val * (1 - neuron.val)
            commonChange = (meanSquareDeriv * softmaxDeriv * actFuncDeriv) / self.outputLayer.size
            neuron.bias -= learningRate * commonChange
            for k in range(len(prevWeightMatrix[neuron.index])):
                currWeight = prevWeightMatrix[neuron.index][k]
                nextData[k] += commonChange * currWeight
                prevWeightMatrix[neuron.index][k] -= learningRate * commonChange * self.outputLayer.prevLayer.layer[k].val
        self.hiddenBackPropagation(nextData, len(self.hiddenGroup) - 1, learningRate)
            
    def hiddenBackPropagation(self, data, hiddenGroupIndex, learningRate):       
        if hiddenGroupIndex == -1:
            return
        currentLayer = self.hiddenGroup[hiddenGroupIndex]
        prevWeightMatrix = currentLayer.prevWeightMatrix
        nextData = [0 for i in range(currentLayer.prevLayer.size)]
        for neuron in self.hiddenGroup[hiddenGroupIndex].layer:
            meanSquareDeriv = -data[neuron.index]
            actFuncDeriv = neuron.val * (1 - neuron.val)
            commonChange = (meanSquareDeriv * actFuncDeriv) / currentLayer.size
            neuron.bias -= learningRate * commonChange
            for k in range(len(prevWeightMatrix[neuron.index])):
                currWeight = prevWeightMatrix[neuron.index][k]
                nextData[k] += commonChange * currWeight
                prevWeightMatrix[neuron.index][k] -= learningRate * commonChange * currentLayer.prevLayer.layer[k].val
        self.hiddenBackPropagation(nextData, hiddenGroupIndex - 1, learningRate)

    def costFunction(self, data):
        if len(self.outputLayer) != len(data):
            print("Invalid data")
            return []
        
        cost = 0
        for i in range(len(self.outputLayer)):
            cost += (self.outputLayer[i].val - data[i]) ** 2
        return cost / (2 * self.outputLayer.size)