# ArgBind

**Build CLIs via docstrings and type annotations, with YAML support.**

![Build](https://github.com/pseeth/argbind/workflows/Build/badge.svg) 
[![PyPI version](https://badge.fury.io/py/argbind.svg)](https://badge.fury.io/py/argbind)
[![codecov](https://codecov.io/gh/pseeth/argbind/branch/main/graph/badge.svg?token=BWI0FHZI5H)](undefined)
![Lines of code](https://img.shields.io/tokei/lines/github/pseeth/argbind)
[![Downloads](https://pepy.tech/badge/argbind)](https://pepy.tech/project/argbind)

*ArgBind is a simple way to bind function or class arguments to the command line or to .yml files!* 
It supports scoping of arguments, similar to other frameworks like 
[Hydra](https://github.com/facebookresearch/hydra) and
[gin-config](https://github.com/google/gin-config).
ArgBind is *very* small (only ~400 lines of code, in one file), can be used to make complex and well-documented command line programs, and allows 
you to configure program execution from .yml files.

If you're migrating from an ArgParse script to an ArgBind script, check out the
[migration guide](./examples/migration). Scroll down to see some [examples](#examples). Please also look at the 
current known [limitations](#limitations-and-known-issues) of ArgBind.

## Why ArgBind?

I built ArgBind mostly to help me configure my machine learning experiments. ML experiment
configuration is often highly nested, and can get out of hand quick. I didn't want to switch
my workflow around too much to accommodate a new framework. Instead, I wanted the scripts
that I've written to be easily adapted so that I could achieve a few goals:

1. Configure scripts using `.yml` files. Be able to save `.yml` files that can be used to rerun scripts the exact same way twice.
2. Spend time writing actual functions needed to run experiments, not argument parsers.
3. Be able to run my experiment code from other Python scripts, notebooks, or the command line.
4. Be able to specify arguments from the command line directly to various functions.
5. Be able to use scoping patterns, so I can run a function inside of a `train` scope and `test` scope, with different results (e.g. for getting a train dataset and a test dataset).

Nothing out there really fit the bill, so I wrote ArgBind. If you have 
an `argparse` based script, converting it to ArgBind should be very quick! ArgBind is simple, 
small, and easy to use. To get a feel for how it works, check out [usage](#usage), [design](#design), and [examples](#examples)!

## Installation

Install via `pip`:

```
python -m pip install argbind
```

Or from source:

```
git clone https://github.com/pseeth/argbind.git
cd argbind
python -m pip install -e .
```

## Examples

- [Example 1: Hello World](./examples/hello_world/)
- [Example 2: Scope patterns](./examples/scoping/)
- [Example 3: Typing](./examples/typing/)
- [Example 4: MNIST Script](./examples/mnist/)
- [Example 5: Loading, saving, and using .yml files](./examples/yaml)
- [Example 6: Multi-stage programs](./examples/multistage)
- [Example 7: Mimic more traditional CLI, without `func.arg` notation](./examples/without_prefix)
- [Example 8: Debug mode](./examples/debug)
- [Example 9: Migrating from ArgParse](./examples/migration)
- [Example 10: Binding existing functions and classes](./examples/bind_existing)

## Usage

There are six main functions.

- `bind`: Binds keyword arguments (and positional arguments if `positional=True`) of a function or class to ArgBind.
- `parse_args`: Actually parses command line arguments into a dictionary.
- `scope`: Context manager that scopes a dictionary containing function arguments to be used by the functions.
- `dump_args`: Dumps the args dictionary to a `.yml` file. Used internally when program is called with `--args.save path/to/save.yml`.
- `load_args`: Loads args from a `.yml` file. Used internally when program is called with `--args.load path/to/load.yml`.
- `get_used_args`: Gets arguments that have actually been used by call functions up to this point.

Your code with ArgBind generally follows this pattern:

1. Write a function with a good docstring, and typed arguments. If arguments are not typed, their type will be inferred from the type of the default.
2. Bind it via `bind`.
3. When program is called, parse the arguments via `parse_args`.
4. Scope the arguments, and call the bound function within the context block.
5. Optionally call program with `--args.save` to save the current execution configuration to a `.yml` file or `--args.load` to load arguments from a prior saved execution configuration to run it the same way twice.
6. Optionally, run your script with `--args.debug=1` to see exactly how every bound function is called.

In your program, you can call `get_used_args` to inspect the state of the argument dictionary. Here's a minimal example:

```python
import argbind

@argbind.bind()
def hello(
    name : str = 'world'
):
    """Say hello to someone.

    Parameters
    ----------
    name : str, optional
        Who you're saying hello to, by default 'world'
    """
    print("Hello " + name)

if __name__ == "__main__":
    # Arguments for CLI automatically generated from bound functions under the pattern
    # function_name.function_arg.
    args = argbind.parse_args()
    # When called within a scope, the keyword arguments map to those from CLI or 
    # from defaults.
    with argbind.scope(args):
        hello()
```

Help text is automatically generated from the docstring:

```
❯ python examples/hello_world/with_argbind.py -h
usage: with_argbind.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--hello.name HELLO.NAME]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function hello:
  Say hello to someone.

  --hello.name HELLO.NAME
                        Who you're saying hello to, by default 'world'
```

Execution of this could look like:

```
# Default arguments
❯ python examples/hello_world/with_argbind.py
Hello world
# Binding name from the command line and saving the args.
❯ python examples/hello_world/with_argbind.py --hello.name=you --args.save=/tmp/args.yml
Hello you
# Loading saved arguments.
❯ python examples/hello_world/with_argbind.py --args.load=/tmp/args.yml
Hello you
# Loading saved arguments, and overriding via command line.
❯ python examples/hello_world/with_argbind.py --args.load=/tmp/args.yml --hello.name=me
Hello me
# See how each function is called with args.debug=1.
❯ python examples/hello_world/with_argbind.py --args.load=/tmp/args.yml --args.debug=1
hello(
  name : str = you
)
Hello you
```

You can also run the `hello` function from another Python script or a Jupyter notebook:

```python
import argbind
# Import the bound function
from .hello_world import hello 
# Load the args
args = argbind.load_args('/tmp/args.yml')
# Scope the args
with argbind.scope(args):
    # Run the bound function
    hello() # Prints 'Hello you'.
hello() # Prints 'Hello world', as it's outside scope.
# Can edit the args before scoping again.
args['hello.name'] = 'me'
with argbind.scope(args):
    hello() # Prints 'Hello me'.
```

You'll notice that ArgBind forces you to document and type your 
function arguments, which is always a good idea! 
Please check out the [examples](#examples) for more details!


## Design

ArgBind is designed around a decorator that can be used on
functions the user wants to expose to command line or to a .yml file.
The arguments to that function are 
then bound to a dictionary. When the function is called, 
each argument is looked up in the dictionary and its
value is replaced with the corresponding value in the dictionary. The
dictionary that the function looks for values in is controlled by
`scope`:

```python
import argbind 

@argbind.bind()
def func(arg : str = 'default'):
    print(arg)

dict1 = {
    'func.arg': 1,
}
dict2 = {
    'func.arg': 2
}

with argbind.scope(dict1):
    func() # prints 1
with argbind.scope(dict2):
    func() # prints 2
func(arg=3) # prints 3.
```

The function arguments are bound to the command line. Continuing the 
simple program from above:

```python
if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        func()
    with argbind.scope(args):
        func(arg=3)
```

You can call this function like so:

```bash
❯ python examples/readme_example.py --func.arg 5
1 # Looks up `arg` in dict1
2 # Looks up `arg` in dict2
3 # arg is passed in on python call `func(arg=3)`
5 # Looks up `arg` from command line call `--func.arg 5`
3 # arg is passed in from two places: `func(arg=3)` and `--func.arg 5`. Former overrides the latter.
```

The logic here is that arguments that are bound that are closer to the actual function call get priority. From highest priority, to lowest, it goes:

1. Bound explicitly in Python code
2. Bound via command line
3. Bound via .yml file
4. Bound via default for kwarg

You can also use `bind` directly on classes - see [here](./examples/bind_existing).

# Limitations and known issues

There are some limitations to ArgBind, some due to how Python function decorator works,
and others out of a desire to keep ArgBind's code simple and straightforward.

## Boolean keyword arguments

If a boolean is flipped to True in a `.yml` file, there's no
way to override it from the command line. If you want a flag to
be flippable, make the argument an int instead of a bool and use
0 and 1 for True and False. Then you can override from command
line like `--func.arg 0` or `--func.arg 1`.

## Bound function names should be unique

Functions that are bound must be unique, even if they are in different files. The 
function name is resolved in the argument parser only using the immediate name, not
a path to the function etc. 

## Supported docstring formats

ArgBind uses [docstring-parser](https://github.com/rr-/docstring_parser), and so
the only supported styles are: ReST, Google, and Numpydoc-style docstrings.

## Not all types are supported

ArgBind supports most types that might pop up in your script, but not all. The supported types can be seen in the [typing example](./examples/typing/).

## Positional arguments should not be saved into .yml files

If the a positional argument is saved into a .yml file, and loaded
via `--args.load`, then any positional argument passed in the
command line will be overridden. Take care not to pass in 
positional arguments via `.yml` files.

# Releasing

Do the following steps:

```
python setup.py sdist
```

Upload it to test PyPI:

```
pip install twine
twine upload --repository testpypi dist/*
pip install -U --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -U argbind
```

Make sure you can install it and it works (e.g. run the examples). Now upload
to actual PyPI:

```
twine upload dist/*
```

# Issues? Questions?

If you've run into some issues with ArgBind, or have some questions, please ask 
via Github Issues. Projects like ArgBind are pretty tricky to get right, so there
may be some edge cases that have been missed.
