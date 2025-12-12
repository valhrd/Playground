import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

def get_mnist_dataloader(mode, datapath="datasets/", batch_size=64, auto_download=False):
    transform = transforms.Compose(
        [
            transforms.ToTensor()
        ]
    )

    dataset = torchvision.datasets.MNIST(
        root=datapath,
        train=(mode == "train"),
        transform=transform,
        download=auto_download
    )
    data_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=(mode == "train")
    )
    return data_loader