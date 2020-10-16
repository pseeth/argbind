import argbind
from typing import List, Dict, Tuple

@argbind.bind()
def func(
    str_arg : str = 'string',
    int_arg : int = 1,
    dict_arg : Dict = None,
    list_int_arg : List[int] = None,
    list_str_arg : List[str] = None,
    bool_arg : bool = False,
    tuple_arg : Tuple[int, float, str] = None,
):
    def info(var, var_name):
        print(f"{var_name} - type: {type(var)}, val: {var}")

    info(str_arg, "String argument")
    info(int_arg, "Integer argument")
    info(dict_arg, "Dictionary argument")
    info(list_int_arg, "List of ints argument")
    info(list_str_arg, "List of strings argument")
    info(bool_arg, "Boolean argument")
    info(tuple_arg, "Tuple of (int, float, str)")

if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        func()
