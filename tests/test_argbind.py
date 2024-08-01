import argbind
import contextlib
import os


@contextlib.contextmanager
def temporary_working_directory(path):
    original_working_directory = os.getcwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(original_working_directory)


def test_load_args():
    arg1 = argbind.load_args("examples/yaml/conf/base.yml")
    with open("examples/yaml/conf/base.yml") as f:
        arg2 = argbind.load_args(f)
    assert arg1 == arg2


def test_config_directory():
    with temporary_working_directory("tests"):
        arg1 = argbind.load_args("examples/yaml/conf/exp2.yml", config_directory="..")
    with open("examples/yaml/conf/exp2.yml") as f:
        arg2 = argbind.load_args(f)

    assert arg1 == arg2
