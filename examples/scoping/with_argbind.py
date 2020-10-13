import argbind

@argbind.bind_to_parser('train', 'val', 'test')
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
    args = argbind.parse_args()
    some_positional_arg = None
    with argbind.scope(args):
        dataset(some_positional_arg)
    for scope in ['train', 'val', 'test']:
        with argbind.scope(args, scope):
            dataset(some_positional_arg)
