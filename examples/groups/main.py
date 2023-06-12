# Sometimes you want to write a program that contains multiple
# subcommands, possibly with overlapping command names. To do this,
# use the "groups" feature of ArgBind.

import argbind
import sys

# This function is always bound.
@argbind.bind(without_prefix=True)
def common(
    some_arg: str = "test"
):
    pass

# This function is bound only when "prepare" is the group.
@argbind.bind(group="prepare", without_prefix=True)
def prepare(
    data_dir: str = "/data/"
):
    pass

# This function is bound only when "train" is the group.
@argbind.bind(group="train", without_prefix=True)
def train(
    data_dir: str = "/data/",
    num_epochs: int = 1000,
    save_path: str = "/runs/baseline"
):
    pass

# This function is bound only when "evaluate" is the group.
@argbind.bind(group="evaluate", without_prefix=True)
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
