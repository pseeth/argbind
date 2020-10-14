from with_argbind import main
import pathlib
import argbind
import itertools

here = pathlib.Path(__file__).parent.resolve()
args = argbind.load_args(here / 'conf/exp.yml')
args['args.debug'] = True

# Sweep over training batch size and learning rate
batch_sizes = [16, 32, 64]
learning_rates = [0.1, 0.5, 1.0]
N = 1

for bs in batch_sizes:
    for lr in learning_rates:
        print(f"Experiment {N}, batch size is {bs}, learning rate is {lr}.")
        args['main.batch_size'] = bs
        args['main.lr'] = lr
        with argbind.scope(args):
            main()
        print()
        N += 1
