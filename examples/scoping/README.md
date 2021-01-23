# Scoping arguments

- `examples/scoping/with_argbind.py`
- `examples/scoping/with_argparse.py`

Functions can be called in scopes, that are defined when the 
function is bound. The two scripts here show how this is 
achieved using argparse vs argbind.

## ArgParse version

```
❯ python examples/scoping/with_argparse.py -h
usage: with_argparse.py [-h] [--train_folder TRAIN_FOLDER] [--val_folder VAL_FOLDER] [--test_folder TEST_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  --train_folder TRAIN_FOLDER
  --val_folder VAL_FOLDER
  --test_folder TEST_FOLDER
```

The arguments must be defined explicitly (here as train_folder, 
val_folder, test_folder), and the code must be written to accommodate
the different calls.

Usage:

```
❯ python examples/scoping/with_argparse.py --train_folder train --val_folder val --test_folder test
default
train
val
test
```

## ArgBind version

```
❯ python examples/scoping/with_argbind.py -h
usage: with_argbind.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--dataset.folder DATASET.FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function dataset:
  Creates a dataset. Additional scope patterns: train, val,
  test. Use these by prefacing any of the args below with one
  of these patterns. For example: --train/dataset.folder
  VALUE.

  --dataset.folder DATASET.FOLDER
                        Folder for the dataset, by default 'default'
```

We see our usual arguments that can be used for loading from and saving 
arguments to YAML files. We also see only a single argument: `dataset.folder`, that can be called with different scoping patterns `train`, 
`val`, and `test`.

Example usage:

```
❯ python examples/scoping/with_argbind.py --train/dataset.folder train --val/dataset.folder val --test/dataset.folder test
default
train
val
test
❯ python examples/scoping/with_argbind.py --train/dataset.folder train --val/dataset.folder val --test/dataset.folder test --args.save /tmp/saved_args.yml
default
train
val
test
❯ python examples/scoping/with_argbind.py --args.load /tmp/saved_args.yml
default
train
val
test
❯ python examples/scoping/with_argbind.py --args.load /tmp/saved_args.yml --args.debug 1
dataset(
  folder : str = default
)
default
dataset(
  # scope = train
  folder : str = train
)
train
dataset(
  # scope = val
  folder : str = val
)
val
dataset(
  # scope = test
  folder : str = test
)
test
```
