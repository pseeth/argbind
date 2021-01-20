"""
Help text:

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

"""
import argbind

# By using without_prefix=True, the arguments to this function are 
# available globally, without the function name as the prefix.
@argbind.bind('scoped', without_prefix=True)
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
