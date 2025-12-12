import numpy as np

from core import Module

# Fixed
class Linear(Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.weights = np.random.normal(size=(in_channels, out_channels))
        self.bias = np.random.normal(size=(out_channels,))

        self.grad_w = None
        self.grad_b = None

    def forward(self, x):
        self.back = x
        return x @ self.weights + self.bias

    def backward(self, dz):
        self.grad_w = self.back.T @ dz
        self.grad_b = dz.mean(axis=0)
        return dz @ self.weights.T

    def step(self, lr):
        self.weights -= lr * self.grad_w
        self.bias -= lr * self.grad_b

class PReLU(Module):
    def __init__(self, alpha=0.25):
        super().__init__()
        self.alpha = alpha
        self.grad_alpha = None
        self.x = None
    
    def forward(self, x):
        out = x * (x > 0) + self.alpha * x * (x <= 0)
        self.x = x
        self.back = (x > 0) + self.alpha * (x <= 0)
        return out

    def backward(self, dz):
        self.grad_alpha = np.sum(dz * self.x * (self.x <= 0))
        return self.back * dz
