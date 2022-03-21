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
    import pickle
    import tempfile

    # Create a class that inherits from the original class
    # so we don't overwrite the original class's init
    # method. Classes are modified *in place*.
    class BoundClass(MyClass):
        pass
    
    BoundClass = argbind.bind(BoundClass, 'pattern')
    bound_fn = argbind.bind(my_func)

    argbind.parse_args() # add for help text, though it isn't used here.

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
        the_class = BoundClass() # prints "from binding in scoping pattern"
        bound_fn() # still prints 123

    with tempfile.NamedTemporaryFile() as f:
        # Make sure that one can pickle the class.
        pickle.dump(the_class, f)
