# Binding classes

## Binding only the init

You can keep a class entirely intact by binding only the init of the class, like so:

```python
class Example:
    @argbind.bind()
    def __init__(self, x: int = 4):
        pass
```

`__init__` is special cased inside of ArgBind so that the prefix is the class name, instead of `__init__`. The usage for the above looks like this:

```
❯ python examples/bind_init_of_class/bind_init_only.py -h
usage: bind_init_only.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG]
                         [--Example.x EXAMPLE.X]
```

You can also bind methods within a class, and their prefixes will include the class name, like so:

```python
class Example:
    @argbind.bind()
    def __init__(self, x: int = 4):
        pass

    @classmethod
    @argbind.bind()
    def some_class_method(cls, y: int = 2):
        pass
```

The usage for the above looks like:

```
❯ python examples/bind_init_of_class/bind_init_only.py -h
usage: bind_init_only.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG]
                         [--Example.x EXAMPLE.X]
                         [--Example.some_class_method.y EXAMPLE.SOME_CLASS_METHOD.Y]
```

## Modifying the class `__init__` function

If you bind a class like so:

```python
@argbind.bind()
class Example:
    def __init__(self, x: int = 4):
        pass

    @classmethod
    def some_class_method(cls):
        pass
```

The following operations take place:

1. An argbound version of the class's init function is created:

```python
class_init = getattr(obj, "__init__")
new_init = argbind.bind(class_init)
```

2. The class's init function is set to this new argbound init:

```python
setattr(obj, "__init__", new_init)
```

3. The modified class is returned:

```python
return obj
```

This object now behaves just like the original class, but its arguments are bound! You can do all of this after the fact as well, like so:

```python
Example = argbind.bind(Example)
# The class method still exists!
Example.some_class_method()
```