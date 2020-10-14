# ArgBind


![Build](https://github.com/pseeth/argbind/workflows/Build/badge.svg) 
[![PyPI version](https://badge.fury.io/py/argbind.svg)](https://badge.fury.io/py/argbind)
[![codecov](https://codecov.io/gh/pseeth/argbind/branch/main/graph/badge.svg?token=BWI0FHZI5H)](undefined)

*ArgBind is a simple way to bind arguments to functions to the command line or to .yml files!* It supports scoping of arguments, similar to other frameworks like 
[Hydra](https://github.com/facebookresearch/hydra) and
[gin-config](https://github.com/google/gin-config).
ArgBind is *very* small, can be used to make super simple command
line programs with help text loaded directly from docstrings, and allows you
to configure program execution from .yml files. Best of all, it's <300 lines of code!

Scroll down to see some [examples](#examples). Please also look at the 
current known [limitations](#limitations) of ArgBind.

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

Nothing out there really fit the bill, so I wrote ArgBind. It's simple, 
small, and easy to use. To get a feel for how it works, please look at some examples!

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
- [Example 5: Extended syntax for .yml files](./examples/yaml)

## Design

ArgBind is designed around a decorator that can be used on
functions the user wants to expose to command line or to a .yml file.
The typed keyword arguments to that function are 
then bound to a dictionary. When the function is called, 
each keyword argument is looked up in the dictionary and its
value is replaced with the corresponding value in the dictionary. The
dictionary that the function looks for values in is controlled by
`scope`:

```python
import argbind 

@argbind.bind_to_parser()
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

The catch is that the function's keyword argument MUST be typed.
This is required so that ArgBind knows how to parse it from the
command line.

## Usage

### How to bind a function

Decorate the function with `bind_to_parser`,
adding it to `PARSE_FUNCS`. The argument
parser inspects each function in PARSE_FUNCS
and adds it to the argument flags. For example:

```python
@bind_to_parser('train', 'val')
def autoclip(percentile : float = 10.0):
    print(f'Called autoclip with percentile={percentile}')
```

This functions arguments are available at:

```bash
python example.py --autoclip.percentile=N
```

The function arguments must be annotated with
their type. Only keyword arguments are included
in the ArgumentParser.

You can optionally define additional patterns to match
for different scopes. This will use the arguments
given on that pattern when the scope is set to that
pattern. The argument is available on command line at
`--pattern/func.kwarg`. The patterns used were `train`
and `val` so the additional arguments are also
available for binding:

```bash
python example.py \ 
    --autoclip.percentile=100 
    --train/autoclip.percentile=1
    --val/autoclip.percentile=5
```

Use with the corresponding code:

```python
# above this, parse the args
args = argbind.parse_args()
with scope(args):
    autoclip() # prints 100
with scope(args, 'train'):
    autoclip() # prints 1
with scope(args, 'val'):
    autoclip() # prints 5
```

### Saving and loading arguments in .yml files

Instead of memorizing complex command line arguments for 
different experiments or configurations, one can save 
and load args via .yml files. To use this, use the 
`--args.save` and `--args.load` arguments to your script.
The first will save the arguments that were used in
the run (including all default values for all functions) 
to a .yml file, for example:

```yml
stages.run:
- TRAIN
- EVALUATE
- ANALYZE
```

Then, when you use --args.load with the path to the saved
file, when the stages function is called, it will run 
TRAIN, then EVALUATE, then ANALYZE. If you edit it to 
look like this:

```yml
stages.run:
- TRAIN
- EVALUATE
```

then only the first two stages will be run. The .yml files are
saved with a flat structure (no nesting). If you provide command line
arguments, then only the parameters that are on the command line
override those in the .yml file. For example:

```bash
python program.py --args.load args.yml --stages.run TRAIN
```
will only run the TRAIN stage, even if args.yml file looks like
above. 

# Limitations

There are some limitations to ArgBind, some due to how Python function decorator works,
and others out of a desire to keep ArgBind's code simple and straightforward.

## Boolean keyword arguments

If a boolean is flipped to True in a `.yml` file, there's no
way to override it from the command line. If you want a flag to
be flippable, make the argument an int instead of a bool and use
0 and 1 for True and False. Then you can override from command
line like `--func.arg 0` or `--func.arg 1`.

## Functions get wrapped

Functions get wrapped and returned as a different function. This other function
is called `cmd_func`, and it's where the magic happens. `cmd_func` does a lookup in
the currently scoped argument dictionary to find matching keyword arguments to
the function it wrapped. Then it calls the function using the matched keyword arguments.
So, if you bind a function, and then inspect it, you won't see the original function.
Instead, you'll see `cmd_func`. This can have adverse effects if you bind a class with
ArgBind, as the actual class will become a function! For now (and possibly forever), 
don't bind classes, bind only functions.

## Bound function names should be unique

Functions that are bound must be unique, even if they are in different files. The 
function name is resolved in the argument parser only using the immediate name, not
a path to the function etc. 

## Supported docstring formats

ArgBind uses [docstring-parser](https://github.com/rr-/docstring_parser), and so
the only supported styles are: ReST, Google, and Numpydoc-style docstrings.

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
are surely some edge cases that have been missed.
