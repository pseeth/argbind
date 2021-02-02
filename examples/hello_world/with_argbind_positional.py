"""
❯ python examples/hello_world/with_argbind_positional.py -h
usage: with_argbind_positional.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--hello.notes HELLO.NOTES] hello.name hello.email

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

  hello.name            Who you're saying hello to.
  hello.email           The email of the person.
  --hello.notes HELLO.NOTES
                        Some optional notes about the person.
"""
import argbind

@argbind.bind(positional=True)
def hello(
    name : str,
    email : str,
    notes : str = "notes"
):
    """Say hello to someone.

    Parameters
    ----------
    name : str
        Who you're saying hello to.
    email : str
        The email of the person.
    notes : str, optional
        Some optional notes about the person.
    """
    print("Hello " + name + ' at ' + email)
    print(f"About {name}: {notes}")

if __name__ == "__main__":
    # Arguments for CLI automatically generated from bound functions under the pattern
    # function_name.function_arg.
    args = argbind.parse_args()
    # When called within a scope, the keyword arguments map to those from CLI or 
    # from defaults.
    with argbind.scope(args):
        hello()
