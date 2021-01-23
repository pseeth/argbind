# Debug mode

One of the cool features of ArgBind is its debug mode. Debug mode can be 
enabled on all ArgBind scripts via `--args.debug=1` passed in on the
command line, or `args.debug: 1` if using a config file. When a function
is called, the function name, arguments and scope are printed just
before the function call, so you can be sure of what keyword arguments
the function was called with, like so:

```
[function_name](
    # scope = [scope]
    kwarg1 : type = val1,
    kwarg2 : type = val2,
    kwarg3 : type = val3,
    ...
)
```

Let's take a look at some examples, generated from running the other examples with
debug mode on.

## Hello world

```
❯ python examples/hello_world/with_argbind.py --args.debug=1
hello(
  name : str = world
)
Hello world
```

```
❯ python examples/hello_world/with_argbind.py --args.debug=1 --hello.name=test
hello(
  name : str = test
)
Hello test
```

## MNIST

```
❯ python examples/mnist/with_argbind_and_refactor.py --args.debug=1 --main.epochs=1 --train.dry_run
main(
  epochs : int = 1
  no_cuda : bool = False
  seed : int = 1
  save_model : bool = False
)
dataset(
  # scope = train
  folder : str = ../data
  split : str = train
  batch_size : int = 64
)
dataset(
  # scope = test
  folder : str = ../data
  split : str = train
  batch_size : int = 64
)
optimizer(
  lr : float = 1.0
)
scheduler(
  step_size : int = 1
  gamma : float = 0.7
)
train(
  log_interval : int = 10
  dry_run : bool = True
)
```

## Shows types

```
❯ python examples/typing/with_argbind.py --func.str_arg "test" --func.int_arg 10 --func.dict_arg "x=5 y=a" --func.list_int_arg "1 2 3" --func.list_str_arg "a b c" --func.bool_arg --func.tuple_arg "1 1.0 number1" --args.save /tmp/saved_args.yml --args.debug=1
func(
  str_arg : str = test
  int_arg : int = 10
  dict_arg : dict = {'x': 5, 'y': 'a'}
  list_int_arg : list = [1, 2, 3]
  list_str_arg : list = ['a', 'b', 'c']
  bool_arg : bool = True
  tuple_arg : tuple = (1, 1.0, 'number1')
)
String argument - type: <class 'str'>, val: test
Integer argument - type: <class 'int'>, val: 10
Dictionary argument - type: <class 'dict'>, val: {'x': 5, 'y': 'a'}
List of ints argument - type: <class 'list'>, val: [1, 2, 3]
List of strings argument - type: <class 'list'>, val: ['a', 'b', 'c']
Boolean argument - type: <class 'bool'>, val: True
Tuple of (int, float, str) - type: <class 'tuple'>, val: (1, 1.0, 'number1')
```

## Scope of functions

```
❯ python examples/scoping/with_argbind.py --args.load /tmp/saved_args.yml --args.debug 1
dataset(
  folder : str = default
)
default
dataset(
  # scope = train
  folder : str = train
)
train
dataset(
  # scope = val
  folder : str = val
)
val
dataset(
  # scope = test
  folder : str = test
)
test
```
