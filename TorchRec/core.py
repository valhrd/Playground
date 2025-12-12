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
