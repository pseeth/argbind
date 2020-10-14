# Example: MNIST

The following three scripts are considered here:

- `examples/mnist/with_argparse.py`
- `examples/mnist/with_argbind.py`
- `examples/mnist/with_argbind_and_refactor.py`

## ArgParse version

This is the original version of a script that trains a classifier on 
MNIST using a deep network. The script was taken from the PyTorch
documentation: https://github.com/pytorch/examples/tree/master/mnist. 
It's a simple script that uses `argparse.ArgumentParser` to configure
the various variables like batch size, learning rate, etc. The help
text looks like:

```
❯ python examples/mnist/with_argparse.py -h
usage: with_argparse.py [-h] [--batch-size N] [--test-batch-size N] [--epochs N] [--lr LR] [--gamma M] [--no-cuda] [--dry-run] [--seed S] [--log-interval N] [--save-model]

PyTorch MNIST Example

optional arguments:
  -h, --help           show this help message and exit
  --batch-size N       input batch size for training (default: 64)
  --test-batch-size N  input batch size for testing (default: 1000)
  --epochs N           number of epochs to train (default: 14)
  --lr LR              learning rate (default: 1.0)
  --gamma M            Learning rate step gamma (default: 0.7)
  --no-cuda            disables CUDA training
  --dry-run            quickly check a single pass
  --seed S             random seed (default: 1)
  --log-interval N     how many batches to wait before logging training status
  --save-model         For Saving the current Model
```

One thing to note here is that arguments like `dry_run` and `log_interval` are only used inside of the `train` function within the script. The `main` function has to specifically pass these arguments to
the `train` function. It actually passes the entire `args` variable into
the train script. This is a common pattern in argparse based scripts - 
the object containing the parsed arguments is passed every which way to every single function that might need something within it. ArgBind seeks
to fix this.

## ArgBind version

Let's now convert this to an ArgBind script. To do this, we remove
argparse, and instead rewrite our `main` function so that it takes 
all the arguments that we want, along with a numpydoc
docstring that describes each keyword argument:

```python
@argbind.bind_to_parser()
def main(
    batch_size : int = 64,
    test_batch_size : int = 1000,
    epochs : int = 14,
    lr : float = 1.0,
    gamma : float = 0.7,
    no_cuda : bool = False,
    dry_run : bool = False,
    seed : int = 1,
    log_interval : int = 10,
    save_model : bool = False,
):
    """Runs an MNIST classification experiment.

    Parameters
    ----------
    batch_size : int, optional
        input batch size for training, by default 64
    test_batch_size : int, optional
        input batch size for testing, by default 1000
    epochs : int, optional
        number of epochs to train, by default 14
    lr : float, optional
        learning rate, by default 1.0
    gamma : float, optional
        Learning rate step gamma, by default 0.7
    no_cuda : bool, optional
        disables CUDA training, by default False
    dry_run : bool, optional
        quickly check a single pass, by default False
    seed : int, optional
        random seed, by default 1
    log_interval : int, optional
        how many batches to wait before logging training status, by default 10
    save_model : bool, optional
        For Saving the current Model, by default False
    """
```

The defaults for each keyword argument are set at the function 
definition. The docstring describes each parameter in the 
same way as the help text of the argument parser. ArgBind
parses the function signature and docstring when 
`argbind.bind_to_parser()` is called on `main`, leading to a 
program with the following usage:

```
❯ python examples/mnist/with_argbind.py -h
usage: with_argbind.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--main.batch_size MAIN.BATCH_SIZE] [--main.test_batch_size MAIN.TEST_BATCH_SIZE] [--main.epochs MAIN.EPOCHS] [--main.lr MAIN.LR]
                       [--main.gamma MAIN.GAMMA] [--main.no_cuda] [--main.dry_run] [--main.seed MAIN.SEED] [--main.log_interval MAIN.LOG_INTERVAL] [--main.save_model]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function main:
  Runs an MNIST classification experiment.

  --main.batch_size MAIN.BATCH_SIZE
                        input batch size for training, by default 64
  --main.test_batch_size MAIN.TEST_BATCH_SIZE
                        input batch size for testing, by default 1000
  --main.epochs MAIN.EPOCHS
                        number of epochs to train, by default 14
  --main.lr MAIN.LR     learning rate, by default 1.0
  --main.gamma MAIN.GAMMA
                        Learning rate step gamma, by default 0.7
  --main.no_cuda        disables CUDA training, by default False
  --main.dry_run        quickly check a single pass, by default False
  --main.seed MAIN.SEED
                        random seed, by default 1
  --main.log_interval MAIN.LOG_INTERVAL
                        how many batches to wait before logging training status, by
                        default 10
  --main.save_model     For Saving the current Model, by default False
```

Because this is now an ArgBind script, we can save the default experiment
configuration to a `.yml` file:

```
python examples/mnist/with_argbind.py --args.save /tmp/saved_args.yml
```

will run the experiment, and also save the arguments that were used 
(here defaults). The saved `.yml` file looks like this:

```yaml
main.batch_size: 64
main.dry_run: false
main.epochs: 14
main.gamma: 0.7
main.log_interval: 10
main.lr: 1.0
main.no_cuda: false
main.save_model: false
main.seed: 1
main.test_batch_size: 1000
```

The same experiment can then be re-run via:

```
python examples/mnist/with_argbind.py --args.load /tmp/saved_args.yml
```

We can override some settings to get a different `.yml` file:

```
python examples/mnist/with_argbind.py --args.save /tmp/saved_args.yml --main.batch_size 1 --main.dry_run
```

which results in the following `.yml` file:

```yaml
main.batch_size: 1 # Overridden by command line and saved
main.dry_run: true # Overridden by command line and saved
main.epochs: 14
main.gamma: 0.7
main.log_interval: 10
main.lr: 1.0
main.no_cuda: false
main.save_model: false
main.seed: 1
main.test_batch_size: 1000
```

We can then load this experiment configuration the same way as before. 
Finally, we can run our script in `debug` mode to make sure what we 
think is happening is happening:

```
❯ python examples/mnist/with_argbind.py --args.debug 1
main <- batch_size=64, test_batch_size=1000, epochs=14, lr=1.0, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False
```

Additionally, note that in this version of the script, the experiment
can *also* be run without a command line interface, like in a notebook
or in another Python script. For example, we can sweep over a bunch
of batch sizes and learning rates, starting from an initial experiment 
configuration in a Python script using ArgBind like so:

```python
from with_argbind import main
import pathlib
import argbind
import itertools

here = pathlib.Path(__file__).parent.resolve()
args = argbind.load_args(here / 'conf/exp.yml')
args['args.debug'] = True

# Sweep over training batch size and learning rate
batch_sizes = [16, 32, 64]
learning_rates = [0.1, 0.5, 1.0]
N = 0

for bs in batch_sizes:
    for lr in learning_rates:
        print(f"Experiment {N}, batch size is {bs}, learning rate is {lr}.")
        args['main.batch_size'] = bs
        args['main.lr'] = lr
        with argbind.scope(args):
            main()
        N += 1
```

The initial experiment configuration is in `conf/exp.yml`. 
This script produces the following output (when `args.debug = True`) as above:

```
❯ python examples/mnist/sweep_argbind.py
Experiment 1, batch size is 16, learning rate is 0.1.
main <- batch_size=16, test_batch_size=1000, epochs=0, lr=0.1, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 2, batch size is 16, learning rate is 0.5.
main <- batch_size=16, test_batch_size=1000, epochs=0, lr=0.5, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 3, batch size is 16, learning rate is 1.0.
main <- batch_size=16, test_batch_size=1000, epochs=0, lr=1.0, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 4, batch size is 32, learning rate is 0.1.
main <- batch_size=32, test_batch_size=1000, epochs=0, lr=0.1, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 5, batch size is 32, learning rate is 0.5.
main <- batch_size=32, test_batch_size=1000, epochs=0, lr=0.5, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 6, batch size is 32, learning rate is 1.0.
main <- batch_size=32, test_batch_size=1000, epochs=0, lr=1.0, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 7, batch size is 64, learning rate is 0.1.
main <- batch_size=64, test_batch_size=1000, epochs=0, lr=0.1, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 8, batch size is 64, learning rate is 0.5.
main <- batch_size=64, test_batch_size=1000, epochs=0, lr=0.5, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False

Experiment 9, batch size is 64, learning rate is 1.0.
main <- batch_size=64, test_batch_size=1000, epochs=0, lr=1.0, gamma=0.7, no_cuda=False, dry_run=False, seed=1, log_interval=10, save_model=False
```

You can parallelize the for loop in the script to run experiments
easily in parallel.

## ArgBind version with refactoring

ArgBind lets you write scripts more naturally by specifying the arguments 
to the specific function or class that needs the argument, rather
than to a giant wrapper function, as you would do in an argparse
based script. This version of the MNIST script refactors it so that multiple
functions have bound arguments. The new usage looks like:

```
❯ python examples/mnist/with_argbind_and_refactor.py -h
usage: with_argbind_and_refactor.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--train.log_interval TRAIN.LOG_INTERVAL] [--train.dry_run] [--dataset.folder DATASET.FOLDER]
                                    [--dataset.split DATASET.SPLIT] [--dataset.batch_size DATASET.BATCH_SIZE] [--optimizer.lr OPTIMIZER.LR] [--scheduler.step_size SCHEDULER.STEP_SIZE] [--scheduler.gamma SCHEDULER.GAMMA]
                                    [--main.epochs MAIN.EPOCHS] [--main.no_cuda] [--main.seed MAIN.SEED] [--main.save_model]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function train:
  Trains a model.

  --train.log_interval TRAIN.LOG_INTERVAL
                        how many batches to wait before logging training status, by
                        default 10
  --train.dry_run       For Saving the current Model, by default False

Generated arguments for function dataset:
  Configuration for the dataset. Additional scope patterns:
  train, test. Use these by prefacing any of the args below
  with one of these patterns. For example:
  --train/dataset.batch_size VALUE.

  --dataset.folder DATASET.FOLDER
                        Where to download the data, by default '../data'
  --dataset.split DATASET.SPLIT
                        'train' or 'test' split of MNIST, by default 'train'
  --dataset.batch_size DATASET.BATCH_SIZE
                        Batch size for dataloader, by default 64

Generated arguments for function optimizer:
  Configuration for Adadelta optimizer.

  --optimizer.lr OPTIMIZER.LR
                        learning rate, by default 1.0

Generated arguments for function scheduler:
  Configuration for StepLR scheduler.

  --scheduler.step_size SCHEDULER.STEP_SIZE
                        Step size in StepLR, by default 1
  --scheduler.gamma SCHEDULER.GAMMA
                        Learning rate step gamma, by default 0.7

Generated arguments for function main:
  Runs an MNIST classification experiment.

  --main.epochs MAIN.EPOCHS
                        number of epochs to train, by default 14
  --main.no_cuda        disables CUDA training, by default False
  --main.seed MAIN.SEED
                        random seed, by default 1
  --main.save_model     For Saving the current Model, by default False
```

One notable change in the script is putting the dataset loading code inside of
two scope patterns: `train` and `test`. Inside the `main` function, the dataset
is built inside of the `train` scope for `train_dataloader` and inside of the
`test` scope for `test_dataloader`:

```
with argbind.scope(args, 'train'):        
    train_loader = dataset(device)
with argbind.scope(args, 'test'):
    test_loader = dataset(device)
```

`device` is a positional argument defined at runtime based on whether `cuda` is
available or not. The other keyword arguments to `dataset` are passed through
via the scoped `args` dictionary. To change the batch size and split of the test 
dataloader from the command line, we just do (along with args.debug=1):

```
❯ python examples/mnist/with_argbind_and_refactor.py --test/dataset.split=test --test/dataset.batch_size=1000 --args.debug=1
main <- epochs=14, no_cuda=False, seed=1, save_model=False
train/dataset <- folder=../data, split=train, batch_size=64
test/dataset <- folder=../data, split=test, batch_size=1000
optimizer <- lr=1.0
scheduler <- step_size=1, gamma=0.7
train <- log_interval=10, dry_run=False
```

You can see that `dataset` is called twice, with different arguments passed to it
depending on the scope that it's in. The first call is in the train scope, while
the second is in the test scope.

Like with other ArgBind scripts, we can save the configuration to a `.yml` file:

```yaml
dataset.batch_size: 64
dataset.folder: ../data
dataset.split: train

main.epochs: 14
main.no_cuda: false
main.save_model: false
main.seed: 1

optimizer.lr: 1.0

scheduler.gamma: 0.7
scheduler.step_size: 1

test/dataset.batch_size: 1000
test/dataset.folder: ../data
test/dataset.split: test

train.dry_run: false
train.log_interval: 10

train/dataset.batch_size: 64
train/dataset.folder: ../data
train/dataset.split: train
```

The experiment can now be rerun:

```
❯ python examples/mnist/with_argbind_and_refactor.py --args.load /path/to/exp.yml
```
