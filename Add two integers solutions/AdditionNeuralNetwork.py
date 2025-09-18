import os

import torch
import torch.nn as nn
import torch.functional as f

class Adder(nn.Module):
    def __init__(self, bound=100):
        super(Adder, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 20),    # from 128 → 32
            nn.Tanh(),           # smaller, faster than ReLU here
            nn.Linear(20, 4 * bound + 1)
        )

    def forward(self, x):
        return self.net(x)


class ModelManager:
    def __init__(self, model, inputs, targets, lr=0.001, momentum=0.9, epochs=100):
        self.model = model

        self.inputs = inputs
        self.targets = targets

        self.lr = lr
        self.momentum = momentum
        self.epochs = epochs
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(model.parameters(), lr=self.lr)


    def training_loop(self):
        for i in range(1, self.epochs + 1):
            train_loss = self.train_model()
            if i % 10 == 0:
                print(f"Training loss after {i} epochs: {train_loss}")

    def train_model(self):
        model = self.model
        model.train()

        train_loss = 0

        self.optimizer.zero_grad()

        outputs = model(self.inputs)
        loss = self.criterion(outputs, self.targets)
        loss.backward()

        self.optimizer.step()
        train_loss += loss.item()

        return train_loss
    

    def validate_model(self):
        model = self.model
        model.eval()

        val_loss = 0

        outputs = model(self.inputs)
        loss = self.criterion(outputs, self.targets)

        val_loss += loss.item()

        return val_loss
    

    def export_model(self):
        os.makedirs("model", exist_ok=True)
        save_path = "model/addition_state.pth"
        torch.save(self.model.state_dict(), save_path)
        return save_path


    def get_model(self):
        return self.model

    
if __name__ == '__main__':
    bound = 100

    dataset = [[i, j, i + j] for i in range(-bound, bound + 1) for j in range(-bound, bound + 1)]
    dataset = torch.Tensor(dataset)

    inputs = dataset[:,:2]
    inputs = inputs / bound
    
    predictions = dataset[:,2]
    targets = (predictions + 2 * bound).long()

    print(inputs.shape)
    print(targets.shape)

    model = Adder(bound=bound)
    model_manager = ModelManager(model, inputs, targets, lr=0.1, epochs=5000)

    model_manager.training_loop()

    print(model_manager.export_model())

    model = model_manager.get_model()
    model.eval()

    total = 0
    correct = 0
    for i in range(-bound, bound + 1):
        for j in range(-bound, bound + 1):
            predicted = model(torch.Tensor([[i / bound, j / bound]])).argmax().item() - 2 * bound
            total += 1
            correct += (predicted == i + j)
    print(f"Accuracy: {correct / total * 100:.2f}%")