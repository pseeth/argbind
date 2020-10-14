import argbind

@argbind.bind_to_parser()
def func(
    arg1 : str = 'default',
    arg2 : str = 'default',
    arg3 : str = 'default',
    arg4 : str = 'default'
):
    """Dummy function for binding.

    Parameters
    ----------
    arg1 : str, optional
        Argument 1, by default 'default'
    arg2 : str, optional
        Argument 2, by default 'default'
    arg3 : str, optional
        Argument 3, by default 'default'
    arg4 : str, optional
        Argument 4, by default 'default'
    """
    print(
        f"Argument 1: {arg1}\n"
        f"Argument 2: {arg2}\n"
        f"Argument 3: {arg3}\n"
        f"Argument 4: {arg4}"
    )

if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        func()
