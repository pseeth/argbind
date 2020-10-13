# Simple example: Hello World

These two scripts:

- `examples/hello_world/with_argbind.py`
- `examples/hello_world/with_argparse.py`

 compare building up a simple script
using `argparse` vs `argbind`. Each script has a single function 
`hello`, which prints `hello [name]`, where `name` can be controlled from
the command line. The help text looks a bit different:

## ArgParse version

```
❯ python examples/hello_world/with_argparse.py -h
usage: with_argparse.py [-h] [--name NAME]

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  Who you're saying hello to.
```

You can do:

```
❯ python examples/hello_world/with_argparse.py --name test
Hello test
```

## ArgBind version

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

You'll notice a few differences. The first is that the argument on the 
command line has changed from `name` to `hello.name`. ArgBind always 
generates command line arguments of the form 
`function_name.function_arg`. There are some other additional arguments:

- `args.save`: This allows us to save the arguments that were used to call the scripts.
- `args.load`: Arguments can be loaded from a `.yml` file rather than 
from command line.
- `args.debug`: When functions are called, the arguments that are passed
to them are printed.

Example usage:

```
❯ python examples/hello_world/with_argparse.py --name test
Hello test
❯ python examples/hello_world/with_argbind.py --hello.name test --args.save /tmp/saved_args.yml
Hello test
❯ python examples/hello_world/with_argbind.py --args.load /tmp/saved_args.yml
Hello test
❯ python examples/hello_world/with_argbind.py --args.load /tmp/saved_args.yml --args.debug=1
hello <- name=test
Hello test
```
