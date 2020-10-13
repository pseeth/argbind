"""
ArgParse version of hello_world script. Help text:

❯ python examples/hello_world/with_argparse.py -h
usage: with_argparse.py [-h] [--name NAME]

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  Who you're saying hello to.

"""
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", type=str, help="Who you're saying hello to.", default="world"
    )

    args = vars(parser.parse_args())
    hello(args['name'])
