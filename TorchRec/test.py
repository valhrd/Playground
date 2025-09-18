from abc import ABC, abstractmethod
import numpy as np

class Module(ABC):
    def __init__(self):
        self.back = None

    @abstractmethod
    def forward(self, *args):
        pass

    @abstractmethod
    def backward(self, *args):
        pass

    def __call__(self, *args):
        return self.forward(*args)        

class FC(Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.weights = np.random.normal(size=(in_channels, out_channels))
        self.bias = np.random.normal(size=(out_channels,))
    
    def forward(self, x):
        self.back = x
        return x @ self.weights + self.bias
    
    def backward(self, lr, dz):
        self.weights -= lr * np.outer(self.back, dz)
        self.bias -= lr * dz
        return dz @ self.weights.T
    
class ReLU(Module):
    def forward(self, x):
        out = x * (x > 0)
        self.back = out > 0
        return out
    
    def backward(self, dz):
        return self.back * dz

class Sigmoid(Module):
    def forward(self, x):
        out = 1 / (1 + np.exp(-x))
        self.back = out * (1 - out)
        return out
    
    def backward(self, dz):
        return self.back * dz
    
class Softmax(Module):
    def forward(self, x):
        temp = np.exp(x)
        out = temp / np.sum(temp)

        self.back = np.diag(out) - np.outer(out, out)
        return out
    
    def backward(self, dz):
        return self.back @ dz
    
class MSELoss(Module):
    def forward(self, y_pred, y_targets):
        diff = y_targets - y_pred
        self.back = diff / diff.shape[0]
        return diff @ diff / diff.shape[0]

    def backward(self):
        return self.back
    
class BCELoss(Module):
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

class CrossEntropyLoss(Module):
    def __init__(self, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.softmax = Softmax()

    def forward(self, y_pred, y_targets):
        y_softmax = self.softmax(y_pred)
        y_targets = np.clip(y_targets, self.eps, 1 - self.eps)

        self.back = y_softmax - y_targets
        return -(np.sum(y_targets * np.log(y_softmax)))

    def backward(self):
        return self.back

if __name__ == "__main__":
    from dataset import get_mnist_dataloader
    from tqdm import tqdm

    class Model(Module):
        def __init__(self):
            super().__init__()
            self.fc1 = FC(28 * 28, 128)
            self.relu = ReLU()
            self.fc2 = FC(128, 10)
            self.softmax = Softmax()
        
        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x
        
        def backward(self, dz):
            dz = self.fc2.backward(lr, dz)
            dz = self.relu.backward(dz)
            dz = self.fc1.backward(lr, dz)

    model = Model()
    epochs = 1
    lr = 0.0005
    bs = 1
    criterion = CrossEntropyLoss()

    for ep in range(1, epochs+1):
        total_loss = 0
        train_total = 0
        train_loader = get_mnist_dataloader("train", batch_size=bs, auto_download=True)
        pbar = tqdm(train_loader)

        for idx, (x, y) in enumerate(pbar):
            # import ipdb; ipdb.set_trace()
            # B, C, H, W = x.shape
            # x = x.numpy().reshape(B, C*H*W)
            x = x.numpy().flatten()
            y = np.array([1 if i == y else 0 for i in range(10)])
            out = model(x)

            loss = criterion(out, y)
            total_loss += loss
            train_total += 1

            dz = criterion.backward()
            model.backward(dz)

            pbar.set_postfix(
                {"Avg Loss": total_loss / train_total}
            )

        total_correct = 0
        val_total = 0
        train_loader = get_mnist_dataloader("val", batch_size=bs, auto_download=True)
        pbar = tqdm(train_loader)

        for idx, (x, y) in enumerate(pbar):
            x = x.numpy().flatten()
            out = model(x)
            total_correct += np.argmax(out) == y
            val_total += 1

            pbar.set_postfix(
                {"Accuracy": total_correct / val_total}
            )

        
   
