if __name__ == "__main__":
    from tqdm import tqdm

    from dataset import get_mnist_dataloader
    from module import *
    from function import *
    from loss import *

    class Model(Module):
        def __init__(self):
            super().__init__()
            self.fc1 = Linear(28 * 28, 128)
            self.relu1 = ReLU()
            self.fc2 = Linear(128, 10)
        
        def forward(self, x: Tensor):
            return x.bind(self.fc1)\
                    .bind(self.relu1)\
                    .bind(self.fc2)

    model = Model()
    epochs = 10
    lr = 0.05
    bs = 64
    criterion = CrossEntropyLoss()

    for ep in range(1, epochs+1):
        total_loss = 0
        train_total = 0
        train_loader = get_mnist_dataloader("train", batch_size=bs, auto_download=True)
        pbar = tqdm(train_loader)

        for idx, (x, y) in enumerate(pbar):
            B, C, H, W = x.shape
            x = x.numpy().reshape(B, C*H*W)
            y = np.array([[1 if i == n else 0 for i in range(10)] for n in y])

            x = Tensor(x)

            out = model(x)
            loss = out.loss(criterion, y)
            total_loss += loss.item()
            train_total += B
            loss.backward(lr)

            pbar.set_postfix(
                {"Avg Loss": f"{total_loss / train_total:.4f}"}
            )

        total_correct = 0
        val_total = 0
        train_loader = get_mnist_dataloader("val", batch_size=bs, auto_download=True)
        pbar = tqdm(train_loader)

        for idx, (x, y) in enumerate(pbar):
            B, C, H, W = x.shape
            x = x.numpy().reshape(B, C*H*W)
            x = Tensor(x)

            out = model(x)
            total_correct += (1 * np.argmax(out.v, axis=1) == y).sum().item()
            val_total += B

            pbar.set_postfix(
                {"Accuracy": f"{total_correct / val_total * 100:.2f}%"}
            )
