from Neuron import Neuron
import random

def createHiddenGroup(layerCount, layerSize):
    hiddenGroup = [[Neuron(index, 0, random.randint(0, 11)) for index in range(layerSize)] for _ in range(layerCount)]
    for i in range(layerCount - 1):
        attachWeightToLayers(hiddenGroup[i], hiddenGroup[i + 1])
    return hiddenGroup

def attachWeightToLayers(start, next):
    weights = [[random.uniform(0, 1) for _ in range(len(next))] for _ in range(len(start))]
    for neuron in start:
        neuron.attachNextLayer(next, weights)
    for neuron in next:
        neuron.attachPrevLayer(start, weights)

def attachLayers(inputLayer, hiddenGroup, outputLayer):
    if not hiddenGroup:
        print("Empty hidden group")
        return
    
    attachWeightToLayers(inputLayer, hiddenGroup[0])
    attachWeightToLayers(hiddenGroup[-1], outputLayer)
    
def evaluateNeurons(hiddenGroup, outputLayer):
    for hiddenLayer in hiddenGroup:
        for neuron in hiddenLayer:
            neuron.evaluate()

    for neuron in outputLayer:
        neuron.evaluate()

def createNetwork(inputLayer, hiddenLayerCount, hiddenLayerSize, outputLayerSize):
    outputLayer = [Neuron(index, 0, random.randint(0, 11)) for index in range(outputLayerSize)]
    hiddenGroup = createHiddenGroup(hiddenLayerCount, hiddenLayerSize)
    attachLayers(inputLayer, hiddenGroup, outputLayer)
    evaluateNeurons(hiddenGroup, outputLayer)
    return [hiddenGroup, outputLayer]

inputLayer = [Neuron(index, 0, random.randint(0, 11)) for index in range(25)]
hidden, output = createNetwork(inputLayer, 2, 5, 10)
print(output[0])
