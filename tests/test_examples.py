import glob
import pytest 
import pathlib
import subprocess
import os
from subprocess import PIPE
import tempfile
import yaml
import argbind

OVERWRITE = False

here = pathlib.Path(__file__).parent.resolve()
examples_path = here.parent / 'examples'
regression_path = (here / 'regression').resolve()
paths = glob.glob(str(examples_path) + '/*/*.py')

os.makedirs(regression_path, exist_ok=True)

def check(output, output_path):
    if not os.path.exists(output_path) or OVERWRITE:
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output)
    else:
        with open(output_path, 'r') as f:
            reg_output = f.read()
        assert output == reg_output

@pytest.mark.parametrize("path", paths)
def test_example(path):
    # Get help text
    output = subprocess.run(["python", path, "-h"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = output.stdout.decode('utf-8')
    
    _path = path.split('examples/')[-1] + '.help'
    output_path = regression_path / _path
    # Ignore the bind_module ones for help text, as the PyTorch docstrings
    # might change on us, causing tests to fail.
    if "bind_module" not in path:
        check(output, output_path)

    # Execute it
    add_args = []
    if 'argparse' not in path:
        add_args.append("--args.debug=1")
        if 'mnist' in path:
            add_args.append("--main.epochs=0")
    elif 'mnist' in path:
        add_args.append("--epochs=0")
    
    if 'positional' in path:
        add_args.extend(["Bob", "bob@abc.com", "--hello.notes='Some notes about Bob'"])
    if 'subcommands' in path:
        add_args.append("download")
    if 'migration' in path:
        add_args.append("1")

    output = subprocess.run(["python", path] + add_args, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = output.stdout.decode('utf-8')

    _path = path.split('examples/')[-1] + '.run'
    output_path = regression_path / _path
    check(output, output_path)

    # Test argbind with saving/loading args
    with tempfile.TemporaryDirectory() as tmpdir:
        if 'argparse' not in path:
            # Save args
            save_path = str(pathlib.Path(tmpdir) / 'args.yml')
            add_args = [f'--args.save={save_path}']
            if 'mnist' in path:
                add_args.append("--main.epochs=0")
            output = subprocess.run(["python", path] + add_args, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output1 = output.stdout.decode('utf-8')

            # Load args
            add_args[0] = f'--args.load={save_path}'
            output = subprocess.run(["python", path] + add_args, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output2 = output.stdout.decode('utf-8')

            assert output1 == output2        

def test_yaml_example():
    added_args = [
        '--args.load=examples/yaml/conf/base.yml',
        '--args.load=examples/yaml/conf/exp1.yml',
        '--args.load=examples/yaml/conf/exp2.yml',
        '--args.load=examples/yaml/conf/exp3.yml',
        '--args.load=examples/yaml/conf/exp4.yml',
    ]
    added_args = [
        {'env': {}, 'flags': ['--args.load=examples/yaml/conf/base.yml']},
        {'env': {}, 'flags': ['--args.load=examples/yaml/conf/exp1.yml']},
        {'env': {}, 'flags': ['--args.load=examples/yaml/conf/exp2.yml']},
        {'env': {}, 'flags': ['--args.load=examples/yaml/conf/exp3.yml']},
        {'env': {'ARGBIND_ENV_VAR': 'test'}, 'flags': ['--args.load=examples/yaml/conf/exp4.yml']},
        {'env': {}, 'flags': ['--args.load=examples/yaml/conf/exp4.yml']},
    ]

    path = str(examples_path / 'yaml' / 'main.py')
    for i, add_arg in enumerate(added_args):      
        cmd = [f"python", path] + add_arg['flags'] 

        environ = os.environ.copy()        
        environ.update(add_arg['env'])

        output = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            env=environ
        )
        output = output.stdout.decode('utf-8')

        _path = path.split('examples/')[-1] + f'.run{i}'
        output_path = regression_path / _path
        check(output, output_path)

def test_typing_example():
    added_args = [
        [
            "--func.str_arg=test",
            "--func.int_arg=10",
            "--func.dict_arg=x=5 y=a",
            "--func.list_int_arg=1 2 3",
            "--func.list_str_arg=a b c",
            "--func.bool_arg",
            "--func.tuple_arg=1 1.0 number1"
        ]
    ]
    path = str(examples_path / 'typing' / 'with_argbind.py')
    for i, add_arg in enumerate(added_args):
        output = subprocess.run(["python", path] + add_arg, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = output.stdout.decode('utf-8')

        _path = path.split('examples/')[-1] + f'.run{i}'
        output_path = regression_path / _path
        check(output, output_path)

def test_scoping_example():
    added_args = [
        [
            "--dataset.folder=newdefault",
        ],
        [
            "--dataset.folder=newdefault", 
            "--train/dataset.folder=train"
        ]
    ]

    path = str(examples_path / 'scoping' / 'with_argbind.py')
    for i, add_arg in enumerate(added_args):
        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = str(pathlib.Path(tmpdir) / 'args.yml')
            add_args = [f'--args.save={save_path}'] + add_arg
            print(' '.join(["python", path] + add_args))
            output = subprocess.run(["python", path] + add_args, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            data = argbind.load_args(save_path)
            data = {key: val for key, val in data.items() if '/' not in key}
            argbind.dump_args(data, save_path)

            add_arg = [x for x in add_arg if '/' not in x]
            add_args = [f'--args.load={save_path}'] + add_arg
            
            output = subprocess.run(["python", path] + add_args, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = output.stdout.decode('utf-8')

            _path = path.split('examples/')[-1] + f'.run{i}'
            output_path = regression_path / _path
            check(output, output_path)

