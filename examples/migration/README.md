# Migrating from ArgParse to ArgBind

This document provides a quick overview of how to migrate an
ArgParse script into an ArgBind script. There are four steps:

1. Make sure the main logic of your script happens within a function, not within the script itself.
2. Make the function's arguments match the ones you exposed in ArgParse, with types to match. If there's help text, write it in the docstring of the function.
3. Bind the function to the parser using `argbind.bind`, optionally using `without_prefix` and `positional` arguments to match your ArgParse program's API.
4. In the `__name__ == "__main__"` block, use `argbind.parse_args`, then scope the arguments and call the function.

## Example

Here's an example of a script written in ArgParse:

```python
import argparse

def main(
    arg1, arg2='arg2', arg3=1.0
):
    print(arg1, arg2, arg3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "arg1", type=int, help="The first argument (positional)",
    )
    parser.add_argument(
        "--arg2", type=str, help="The second argument (keyword)",
        default='arg2'
    )
    parser.add_argument(
        "--arg3", type=float, help="The third argument (keyword)",
        default='arg3'
    )

    args = vars(parser.parse_args())
    main(args['arg1'], arg2=args['arg2'], arg3=['arg3'])
```

It's a simple script with three arguments, each with a different 
type (`int`, `str`, `float`). The types are enforced in each
`parser.add_argument`'s `type` kwarg. The defaults are in two
places, once in the function and once in the parser.
`arg1` is positional and the other two are keyword arguments. The help
text for this program looks like this:

```
❯ python examples/migration/argparse_script.py -h
usage: argparse_script.py [-h] [--arg2 ARG2] [--arg3 ARG3] arg1

positional arguments:
  arg1         The first argument (positional)

optional arguments:
  -h, --help   show this help message and exit
  --arg2 ARG2  The second argument (keyword)
  --arg3 ARG3  The third argument (keyword)
```

Let's migrate it to ArgBind:

```python
import argbind

@argbind.bind(without_prefix=True, positional=True)
def main(
    arg1 : int, 
    arg2 : str = 'arg2', 
    arg3 : float = 1.0
):
    """Same script, ArgBind style.

    Parameters
    ----------
    arg1 : int
        The first argument (positional).
    arg2 : str, optional
        The second argument (keyword), by default 'arg2'.
    arg3 : float, optional
        The third argument (keyword), by default 1.0
    """    
    print(arg1, arg2, arg3)

if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        main()
```

A few things shifted around:

1. The help text for each argument was turned into numpy-style docstrings.
2. The defaults for each argument are kept in the function declaration.
3. The arguments are now *typed* explicitly in the function declaration. ArgBind looks at these types when building the parser.
4. The function is *bound* via `@argbind.bind`, and `without_prefix=True` and `positional=True` are set.
5. In the block at the bottom, the `args` are parsed via `argbind`, then `scoped`, and then `main` is called *without any arguments*. The arguments to `main` are looked up in scoped arguments and passed in at runtime - a form of *dependency injection*.

The help text looks like this:

```
❯ python examples/migration/argbind_script.py -h
usage: argbind_script.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--arg2 ARG2] [--arg3 ARG3] arg1

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function main:
  Same script, ArgBind style.

  arg1                  The first argument (positional).
  --arg2 ARG2           The second argument (keyword), by default 'arg2'.
  --arg3 ARG3           The third argument (keyword), by default 1.0
```

You'll notice that there are three more arguments `args.save`, `args.load`, and `args.debug`. The first two of these allow you to save and load arguments from `.yml` files. For more, see the [YAML example](../yaml). `args.debug` lets you see exactly the arguments that bound functions are called with as they are being called:

```
❯ python examples/migration/argbind_script.py --args.debug=1 1
main(
  arg1 : int = 1
  arg2 : str = arg2
  arg3 : float = 1.0
)
1 arg2 1.0
```

And that's it! ArgBind has more features, such as the ability to keep configuration files that can nest or reference environment variables, 
easily do hyperparameter sweeps, using scopes to call functions with
different arguments based on which scope you're calling them within, 
and more. 
Hope it helps tame the wild world of argument parsing for you in your 
daily work. To get it, just do `pip install argbind`. Thanks for 
reading!
