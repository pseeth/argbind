import glob
import pytest 
import pathlib
import subprocess
import os

here = pathlib.Path(__file__).parent.resolve()
examples_path = here.parent / 'examples'
regression_path = (here / 'regression').resolve()
paths = glob.glob(str(examples_path) + '/*/*.py')

os.makedirs(regression_path, exist_ok=True)

def check(output, output_path):
    if not os.path.exists(output_path):
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
    output = subprocess.run(["python", path, "-h"], capture_output=True)
    output = output.stdout.decode('utf-8')
    
    _path = path.split('examples/')[-1] + '.help'
    output_path = regression_path / _path
    check(output, output_path)

    # Execute it
    add_args = ["--args.debug=1"]
    if 'mnist' in path:
        add_args.append("--main.epochs=0")
    output = subprocess.run(["python", path] + add_args, capture_output=True)
    output = output.stdout.decode('utf-8')

    _path = path.split('examples/')[-1] + '.log'
    output_path = regression_path / _path
    check(output, output_path)
