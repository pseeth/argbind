# Binding existing functions or classes

ArgBind can be used to bind functions that already exist in other packages,
provided that the function's arguments are *typed*. Function arguments must be typed
so that ArgBind knows how to parse the command line before passing arguments
to the function. Other limitations as laid out in the ArgBind README also apply.

## How to use it

Let's say I have some module where the following objects are defined:

```python
# contents of my_module.py
class MyClass:
    def __init__(self, x: str = "from default"):
        self.x = x

def my_func(x: int = 100):
    print(x)
    return x
```

Obviously, the creator of this package isn't using ArgBind anywhere, but
since the objects are already defined, we can't decorate them with the
`@` syntax. So, we should do this instead:

```python
import argbind

BoundClass = argbind.bind(MyClass)
bound_fn = argbind.bind(my_func)
```

Now when you call either `BoundClass` or `bound_fn`, you get the "ArgBind'ed" version
of those functions. If you call `MyClass` or `my_func` instead, you'll get the original
functions - undecorated, which won't have any ArgBindiness associated with them. 
They are just the original functions, as defined in the module.

If you want to bind it within some scoping patterns, then you just do this:

```python
BoundClass = argbind.bind(MyClass, 'train')
bound_fn = argbind.bind(my_func, 'train')
```

Let's look at a complete example:

```python
# Functions/classes that should be bound
class MyClass:
    def __init__(self, x: str = "from default"):
        self.x = x
        print(self.x)

def my_func(x: int = 100):
    print(x)
    return x

if __name__ == "__main__":
    import argbind
    
    BoundClass = argbind.bind(MyClass, 'pattern')
    bound_fn = argbind.bind(my_func)

    args = {
      'MyClass.x': 'from binding',
      'pattern/MyClass.x': 'from binding in scoping pattern',
      'my_func.x': 123,
      'args.debug': True # for printing arguments passed to each function
    }

    # Original objects are not affected by ArgBind
    print("Original object output")
    with argbind.scope(args):
        MyClass() # prints "from default"
        my_func() # prints 100
    print()
    
    # Bound objects ARE affected by ArgBind
    print("Bound objects output")
    with argbind.scope(args):
        BoundClass() # prints "from binding"
        bound_fn() # prints 123
    print()
    
    # Scoping patterns can be used
    print("Bound objects inside scoping pattern output")
    with argbind.scope(args, 'pattern'):
        BoundClass() # prints "from binding in scoping pattern"
        bound_fn() # still prints 123
```

This has the following output:

```bash
❯ python examples/bind_existing/with_argbind.py
Original object output
from default
100

Bound objects output
MyClass(
  x : str = from binding
)
from binding
my_func(
  x : int = 123
)
123

Bound objects inside scoping pattern output
MyClass(
  # scope = pattern
  x : str = from binding in scoping pattern
)
from binding in scoping pattern
my_func(
  # scope = pattern
  x : int = 123
)
123
```
