from abc import ABC, abstractmethod
import numpy as np

class Module(ABC):
    def __init__(self):
        self.back = None

    @abstractmethod
    def forward(self, *args):
        pass

    def backward(self, dz):
        pass

    def step(self, lr):
        pass

    def __call__(self, tensor, *args):
        return self.forward(tensor, *args)

class Tensor:
    def __init__(self, v, graph=[]):
        self.v = v
        self.graph = graph

    def bind(self, module):
        out = module(self.v)
        return Tensor(out, self.graph + [module])
    
    def loss(self, loss_fn, targets):
        loss = loss_fn(self.v, targets)
        return LossTensor(loss, self.graph, loss_fn)

    def item(self):
        return self.v.item()

class LossTensor(Tensor):
    def __init__(self, v, graph, loss_fn):
        super().__init__(v, graph)
        self.loss_fn = loss_fn

    def backward(self, lr):
        dz = self.loss_fn.backward()
        graph = self.graph[::-1]
        for module in graph:
            dz = module.backward(dz)
        for module in graph:
            module.step(lr)
        self.graph = []

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
