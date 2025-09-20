import numpy as np

from module import Module, Tensor
from function import Softmax

class Loss(Module):
    pass

# NOT Fixed 
class MSELoss(Loss):
    def forward(self, y_pred, y_targets):
        diff = y_targets - y_pred
        self.back = diff / diff.shape[0]
        return diff @ diff / diff.shape[0]

    def backward(self):
        return self.back

# NOT Fixed
class BCELoss(Loss):
    def __init__(self, eps=1e-5):
        super().__init__()
        self.eps = eps

    def forward(self, y_pred, y_targets):
        y_pred = np.clip(y_pred, self.eps, 1 - self.eps)
        y_targets = np.clip(y_targets, self.eps, 1 - self.eps)

        # self.back = (1 - y_targets) / (1 - y_pred) - (y_targets / y_pred)
        return -(np.sum(y_targets * np.log(y_pred) + (1 - y_targets) * np.log(1 - y_pred)))

    def backward(self):
        return self.back

# Fixed
class CrossEntropyLoss(Loss):
    def __init__(self, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.softmax = Softmax()

    def forward(self, y_pred, y_targets):
        B = y_pred.shape[0]
        y_softmax = self.softmax(y_pred)
        y_softmax = np.clip(y_softmax, self.eps, 1 - self.eps)
        y_targets = np.clip(y_targets, self.eps, 1 - self.eps)

        self.back = (y_softmax - y_targets) / B
        return -(np.sum(y_targets * np.log(y_softmax))) / B

    def backward(self):
        return self.back