# Expose arguments without prefix

This script:

- `examples/without_prefix/without_prefix.py`

shows how one can use `without_prefix=True` to expose a functions arguments
without the function name as the prefix, instead of exposing them with the
function name as the prefix. The interface to the script is now the same
as the one in `examples/hello_world/with_argparse.py`.

## ArgBind version

```
❯ python examples/without_prefix/without_prefix.py -h
usage: without_prefix.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--name NAME]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function hello:
  Say hello to someone. Additional scope patterns: scoped. Use
  these by prefacing any of the args below with one of these
  patterns. For example: --scoped/name VALUE.

  --name NAME           Who you're saying hello to, by default 'world'
```

Example:

```
❯ python examples/without_prefix/without_prefix.py
Hello world
❯ python examples/without_prefix/without_prefix.py --name test
Hello test
```
