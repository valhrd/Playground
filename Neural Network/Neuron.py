import numpy as np
import random

class Neuron:
    def __init__(self, index, val, bias, output=False):
        self.index = index
        self.val = val
        self.softmax = 0
        self.bias = bias

        self.output = output
    
    def __repr__(self):
        return f"<{self.softmax}>" if self.output else f"<{self.val}>"