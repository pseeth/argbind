import argparse

def dataset(
    some_positional_arg,
    folder : str = 'default',
):
    """Creates a dataset.

    Parameters
    ----------
    some_positional_arg 
        Some positional argument that gets passed in via the script.
    folder : str, optional
        Folder for the dataset, by default 'default'
    """
    print(folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_folder', type=str, default='default')
    parser.add_argument('--val_folder', type=str, default='default')
    parser.add_argument('--test_folder', type=str, default='default')

    some_positional_arg = None

    args = vars(parser.parse_args())
    dataset(some_positional_arg)

    dataset(some_positional_arg, args['train_folder'])
    dataset(some_positional_arg, args['val_folder'])
    dataset(some_positional_arg, args['test_folder'])
