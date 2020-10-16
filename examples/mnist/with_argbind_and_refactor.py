from __future__ import print_function
import argbind
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

@argbind.bind()
def train(
    model, 
    device, 
    train_loader, 
    optimizer, 
    epoch,
    log_interval : int = 10,
    dry_run : bool = False,
):
    """Trains a model.

    Parameters
    ----------
    log_interval : int, optional
        how many batches to wait before logging training status, by default 10
    dry_run : bool, optional
        For Saving the current Model, by default False
    """
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            if dry_run:
                break


def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

@argbind.bind('train', 'test')
def dataset(
    device,
    folder : str = '../data',
    split : str = 'train',
    batch_size : int = 64,
):
    """Configuration for the dataset.

    Parameters
    ----------
    folder : str, optional
        Where to download the data, by default '../data'
    split : str, optional
        'train' or 'test' split of MNIST, by default 'train'
    batch_size : int, optional
        Batch size for dataloader, by default 64
    """
    train = (split == 'train')
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    kwargs = {'batch_size': batch_size}
    if device == 'cuda':
        cuda_kwargs = {'num_workers': 1,
                       'pin_memory': True,
                       'shuffle': True}
        kwargs.update(cuda_kwargs)
    dataset = datasets.MNIST('../data', train=train, download=True,
                       transform=transform)

    dataloader = torch.utils.data.DataLoader(dataset, **kwargs)
    return dataloader

@argbind.bind()
def optimizer(
    model,
    lr : float = 1.0
):
    """Configuration for Adadelta optimizer.

    Parameters
    ----------
    lr : float, optional
        learning rate, by default 1.0
    """
    return optim.Adadelta(model.parameters(), lr=lr)

@argbind.bind()
def scheduler(
    optimizer,
    step_size : int = 1,
    gamma : float = 0.7
):
    """Configuration for StepLR scheduler.

    Parameters
    ----------
    step_size : int, optional
        Step size in StepLR, by default 1
    gamma : float, optional
        Learning rate step gamma, by default 0.7
    """
    return StepLR(optimizer, step_size=1, gamma=gamma)

@argbind.bind()
def main(
    args,
    epochs : int = 14,
    no_cuda : bool = False,
    seed : int = 1,
    save_model : bool = False,
):
    """Runs an MNIST classification experiment.

    Parameters
    ----------
    epochs : int, optional
        number of epochs to train, by default 14
    no_cuda : bool, optional
        disables CUDA training, by default False
    seed : int, optional
        random seed, by default 1
    save_model : bool, optional
        For Saving the current Model, by default False
    """
    use_cuda = not no_cuda and torch.cuda.is_available()
    torch.manual_seed(seed)
    device = torch.device("cuda" if use_cuda else "cpu")

    with argbind.scope(args, 'train'):        
        train_loader = dataset(device)
    with argbind.scope(args, 'test'):
        test_loader = dataset(device)

    model = Net().to(device)
    _optimizer = optimizer(model)
    _scheduler = scheduler(_optimizer)
    
    for epoch in range(1, epochs + 1):
        train(model, device, train_loader, _optimizer, epoch)
        test(model, device, test_loader)
        _scheduler.step()

    if save_model:
        torch.save(model.state_dict(), "mnist_cnn.pt")


if __name__ == '__main__':
    args = argbind.parse_args()
    with argbind.scope(args):
        main(args)
