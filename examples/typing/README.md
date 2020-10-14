# Supported types

ArgBind figures out how to parse things from the command line using
Python Type Hinting. This means that the functions that you bind
from your function *must* be strongly typed in the function
signature. The following types are supported:

- Strings
- Integers
- Dictionaries 
    - Passed in on command line like "x=y a=1", which maps to `{'x': 'y', 'a': 1}`. The types of each value are inferred by evaluating the
    string.
- Lists
    - Lists should also be typed and all be of one type, like `List[int]` or `List[str]`. They're passed in like on command line as space-delimited strings: "a b c", or "1 2 3".
- Booleans
    - Passed in as flags from command line, like `--func.bool_arg`, which will set it to True. Make the default False.
- Tuples
    -Tuples must be strongly typed, with each entry in the expected tuple typed, like this `Tuple[int, float, str]`.

## Example

See `examples/typing/with_argbind.py` for an example.

```
❯ python examples/typing/with_argbind.py -h
usage: with_argbind.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--func.str_arg FUNC.STR_ARG] [--func.int_arg FUNC.INT_ARG] [--func.dict_arg FUNC.DICT_ARG] [--func.list_int_arg FUNC.LIST_INT_ARG]
                       [--func.list_str_arg FUNC.LIST_STR_ARG] [--func.bool_arg] [--func.tuple_arg FUNC.TUPLE_ARG]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function func:

  --func.str_arg FUNC.STR_ARG
  --func.int_arg FUNC.INT_ARG
  --func.dict_arg FUNC.DICT_ARG
  --func.list_int_arg FUNC.LIST_INT_ARG
  --func.list_str_arg FUNC.LIST_STR_ARG
  --func.bool_arg
  --func.tuple_arg FUNC.TUPLE_ARG
```

Usage:

```
❯ python examples/typing/with_argbind.py --func.str_arg "test" --func.int_arg 10 --func.dict_arg "x=5 y=a" --func.list_int_arg "1 2 3" --func.list_str_arg "a b c" --func.bool_arg --func.tuple_arg "1 1.0 number1" --args.save /tmp/saved_args.yml
String argument - type: <class 'str'>, val: test
Integer argument - type: <class 'int'>, val: 10
Dictionary argument - type: <class 'dict'>, val: {'x': 5, 'y': 'a'}
List of ints argument - type: <class 'list'>, val: [1, 2, 3]
List of strings argument - type: <class 'list'>, val: ['a', 'b', 'c']
Boolean argument - type: <class 'bool'>, val: True
Tuple of (int, float, str) - type: <class 'list'>, val: [1, 1.0, 'number1']
❯
❯ python examples/typing/with_argbind.py --args.load /tmp/saved_args.yml
String argument - type: <class 'str'>, val: test
Integer argument - type: <class 'int'>, val: 10
Dictionary argument - type: <class 'dict'>, val: {'x': 5, 'y': 'a'}
List of ints argument - type: <class 'list'>, val: [1, 2, 3]
List of strings argument - type: <class 'list'>, val: ['a', 'b', 'c']
Boolean argument - type: <class 'bool'>, val: True
Tuple of (int, float, str) - type: <class 'list'>, val: [1, 1.0, 'number1']
```

`saved_args.yml` looks like this:

```yaml
func.bool_arg: true
func.dict_arg:
  x: 5
  y: a

func.int_arg: 10
func.list_int_arg:
- 1
- 2
- 3
func.list_str_arg:
- a
- b
- c
func.str_arg: test
func.tuple_arg:
- 1
- 1.0
- number1
```
