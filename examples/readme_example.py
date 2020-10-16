import argbind 

@argbind.bind()
def func(arg : str = 'default'):
    print(arg)

dict1 = {
    'func.arg': 1,
}
dict2 = {
    'func.arg': 2
}

with argbind.scope(dict1):
    func() # prints 1
with argbind.scope(dict2):
    func() # prints 2
func(arg=3) # prints 3.

if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        func()

    with argbind.scope(args):
        func(arg=3)
