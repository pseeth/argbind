# ArgBind

*ArgBind is a simple way to bind arguments to functions to the command line or to .yml files!* It supports scoping of arguments, similar to other frameworks like 
[Hydra](https://github.com/facebookresearch/hydra) and
[gin-config](https://github.com/google/gin-config).
ArgBind is *very* small, can be used to make super simple command
line programs with help text loaded directly from docstrings, and allows you
to configure program execution from .yml files. Best of all, it's only ~300 lines!

Scroll down to see some [examples](#examples).

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

## Examples

- [Example 1: Hello World](./examples/hello_world/README.md)
- [Example 2: Scope patterns](./examples/scoping/README.md)
- [Example 3: Typing](./examples/typing/README.md)

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

NOTE: If a boolean is flipped to True in the .yml file, there's no
way to override it from the command line. If you want a flag to
be flippable, make the argument an int instead of a bool and use
0 and 1 for True and False. Then you can override from command
line like `--func.arg 0` or `--func.arg 1`.
