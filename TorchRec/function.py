import numpy as np

from module import Module, Tensor

# Fixed
class ReLU(Module):
    def forward(self, x):
        out = x * (x > 0)
        self.back = out > 0
        return out

    def backward(self, dz):
        return self.back * dz

# Fixed
class Sigmoid(Module):
    def forward(self, x):
        out = 1 / (1 + np.exp(-x))
        self.back = out * (1 - out)
        return out

    def backward(self, dz):
        return self.back * dz

class Tanh(Module):
    def forward(self, x):
        out = np.tanh(x)
        self.back = np.cosh(x) ** (-2)
        return out

    def backward(self, dz):
        return self.back * dz

# Fixed
class Softmax(Module):
    def forward(self, x):
        x_shifted = x - np.max(x, axis=-1, keepdims=True)
        temp = np.exp(x_shifted)
        out = temp / np.sum(temp, axis=-1, keepdims=True)
        return out

    def backward(self, dz):
        return self.back @ dz

class LeakyReLU(Module):
    def __init__(self, alpha=0.01):
        super().__init__()
        self.alpha = alpha

    def forward(self, x):
        out = x * (x > 0) + self.alpha * x * (x <= 0)
        self.back = (x > 0) + self.alpha * (x <= 0)
        return out

    def backward(self, dz):
        return self.back * dz
