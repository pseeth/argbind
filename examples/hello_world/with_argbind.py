"""
ArgBind version of hello_world script. Help text:

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

"""
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
