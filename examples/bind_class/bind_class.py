from ast import arg
import argbind

@argbind.bind()
class Example:
    def __init__(self, x: int = 4):
        pass

    @classmethod
    @argbind.bind()
    def some_class_method(cls, y: int = 2):
        print("I'm a class method")
        pass



if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        ex = Example()
        Example.some_class_method()
