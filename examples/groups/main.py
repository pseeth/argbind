# Sometimes you want to write a program that contains multiple
# subcommands, possibly with overlapping command names. To do this,
# use the "groups" feature of ArgBind.

import argbind
import sys

@argbind.bind(group="prepare")
def prepare(
    data_dir: str = "/data/"
):
    pass

@argbind.bind(group="train")
def train(
    data_dir: str = "/data/",
    num_epochs: int = 1000,
    save_path: str = "/runs/baseline"
):
    pass

@argbind.bind(group="evaluate")
def evaluate(
    data_dir: str = "/data/",
    save_path: str = "/runs/baseline"
):
    pass

if __name__ == "__main__":
    group = sys.argv.pop(1)
    args = argbind.parse_args(group=group)
    
    fn = locals().get(group)
    with argbind.scope(args):
        fn()
