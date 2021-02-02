import argbind

@argbind.bind(without_prefix=True, positional=True)
def main(
    arg1 : int, 
    arg2 : str = 'arg2', 
    arg3 : float = 1.0
):
    """Same script, ArgBind style.

    Parameters
    ----------
    arg1 : int
        The first argument (positional).
    arg2 : str, optional
        The second argument (keyword), by default 'arg2'.
    arg3 : float, optional
        The third argument (keyword), by default 1.0
    """    
    print(arg1, arg2, arg3)

if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        main()
