import argbind

def test_load_args():
    arg1 = argbind.load_args("examples/yaml/conf/base.yml")
    with open("examples/yaml/conf/base.yml") as f:
        arg2 = argbind.load_args(f)
    assert arg1 == arg2
