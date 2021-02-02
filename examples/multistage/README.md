# Writing multi-stage programs

You may have an experiment workflow that works in multiple stages. 
For example, you might have the following:

1. Download necessary data
2. Preprocess the data
3. Train a model
4. Evaluate the model
5. Produce plots/figures analyzing the model performance

This example provides a reasonable style to follow that works
for this use-case. The key idea is to encapsulate each of those
stages in their own functions, which is bound via ArgBind. 

Let's see how to build a script that works for this.
The script is `examples/multistage/multistage.py`. The script's 
stages are each encapsulated into a function, which executes
it:

- `download()`: Downloads the data to a target folder.
- `preprocess()`: Preprocesses data from a source folder to a target folder.
- `train()`: Trains a model given data in a training folder, and saves the model to disk.
- `evaluate()`: Evaluates a model, give a path to it, and a path to a test folder. 
                Saves the results to another folder.
- `analyze()`: Analyzes the data in a results folder and produces a plot.

There are two additional bound functions:

- `run_stages()`: Runs the requested stages in the script. Takes a list of strings, each of which corresponds to the stages above. If a specified stage is not known to the script, this throws an error. The run stages function looks like this:

```
@argbind.bind()
def run(stages : List[str] = STAGES):
    """Run stages.

    Parameters
    ----------
    stages : List[str], optional
        List of stages to run, by default 
        ['download', 'preprocess', 'train', 
         'evaluate', 'analyze']
    """
    with output():
        for stage in stages:
            if stage not in STAGES:
                raise ValueError(
                    f"Requested stage {stage} not in known stages {STAGES}"
                )
            stage_fn = globals()[stage]
            stage_fn()
```

- `output()`: The script switches working directories to the specified folder. The rest of the script can then use relative paths with respect to the specified output folder. This is a context manager that is bound via ArgBind! While not the focus of this example, it's a nifty function to use in experiment code.

Let's look at the help for this script:

```
usage: multistage.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD]
                     [--args.debug ARGS.DEBUG] [--output.folder OUTPUT.FOLDER]
                     [--download.folder DOWNLOAD.FOLDER]
                     [--preprocess.src_folder PREPROCESS.SRC_FOLDER]
                     [--preprocess.dst_folder PREPROCESS.DST_FOLDER]
                     [--train.folder TRAIN.FOLDER]
                     [--train.epochs TRAIN.EPOCHS] [--train.lr TRAIN.LR]
                     [--train.model_type TRAIN.MODEL_TYPE]
                     [--train.model_path TRAIN.MODEL_PATH]
                     [--evaluate.model_path EVALUATE.MODEL_PATH]
                     [--evaluate.folder EVALUATE.FOLDER]
                     [--evaluate.results_folder EVALUATE.RESULTS_FOLDER]
                     [--analyze.results_folder ANALYZE.RESULTS_FOLDER]
                     [--run.stages RUN.STAGES]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function output:
  Controls the output folder where everything gets saved.

  --output.folder OUTPUT.FOLDER
                        Output folder, everything is saved relative to this folder,
                        by default '.'

Generated arguments for function download:
  Download data to folder.

  --download.folder DOWNLOAD.FOLDER
                        Absolute path to folder to download data to, by default
                        '/data/raw'

Generated arguments for function preprocess:
  Preprocess data.

  --preprocess.src_folder PREPROCESS.SRC_FOLDER
                        Absolute path to raw data, by default '/data/raw'
  --preprocess.dst_folder PREPROCESS.DST_FOLDER
                        Absolute path where preprocessed data is placed, by default
                        '/data/processed'

Generated arguments for function train:
  Train the model.

  --train.folder TRAIN.FOLDER
                        Folder to train from, by default '/data/processed/train/'
  --train.epochs TRAIN.EPOCHS
                        Number of epochs, by default 50
  --train.lr TRAIN.LR   Learning rate, by default 1e-3
  --train.model_type TRAIN.MODEL_TYPE
                        Type of model, by default 'conv'
  --train.model_path TRAIN.MODEL_PATH
                        Where to save model to, by default 'checkpoints/model.pth'

Generated arguments for function evaluate:
  Evaluate the model.

  --evaluate.model_path EVALUATE.MODEL_PATH
                        Path to model to evaluate, by default
                        'checkpoints/model.pth'
  --evaluate.folder EVALUATE.FOLDER
                        Folder containing data to evaluate model on, by default
                        '/data/processed/test/'
  --evaluate.results_folder EVALUATE.RESULTS_FOLDER
                        Folder to save results into, by default './results'

Generated arguments for function analyze:
  Analyze model performance, make plots.

  --analyze.results_folder ANALYZE.RESULTS_FOLDER
                        Folder where results are, by default './results'

Generated arguments for function run:
  Run stages.

  --run.stages RUN.STAGES
                        List of stages to run, by default  ['download',
                        'preprocess', 'train',   'evaluate', 'analyze']
```

Right off the bat, you can see we have control over every facet of this 
scripts execution. Let's execute it:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: DOWNLOAD
Downloading data to /data/raw

STAGE: PREPROCESS
Preprocessing /data/raw into /data/processed

STAGE: TRAIN
Training model conv on data in /data/processed/train/ for 50 epochs, with learning rate of 0.001

STAGE: EVALUATE
Evaluating model checkpoints/model.pth on /data/processed/test/, saving results to ./results

STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```

The script executed each stage in the default order. Let's take a look at what's inside
`/tmp/output/`:

```
❯ tree /tmp/output
/tmp/output
├── checkpoints
│   └── model.pth
└── results
    ├── example.npy
    └── example.png
```

Let's specify the stages we want to run. We've downloaded and preprocessed t
he data already, so let's skip those:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output --run.stages "train evaluate analyze"
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: TRAIN
Training model conv on data in /data/processed/train/ for 50 epochs, with learning rate of 0.001

STAGE: EVALUATE
Evaluating model checkpoints/model.pth on /data/processed/test/, saving results to ./results

STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```

Maybe we found a bug in our evaluation code, so let's fix it and try again, skipping
train this time:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output --run.stages "evaluate analyze"
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: EVALUATE
Evaluating model checkpoints/model.pth on /data/processed/test/, saving results to ./results

STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```


Maybe we want to tweak the resultant plots, and run it again:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output --run.stages "analyze"
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```

Maybe we want to redo the entire experiment, but this time train the model for 100 epochs instead of 50:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output --run.stages "train evaluate analyze" --train.epochs 100
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: TRAIN
Training model conv on data in /data/processed/train/ for 100 epochs, with learning rate of 0.001

STAGE: EVALUATE
Evaluating model checkpoints/model.pth on /data/processed/test/, saving results to ./results

STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```

Finally, save that last command to a .yml so we can run it again if we want:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output --run.stages "train evaluate analyze" --train.epochs 100 --args.save /tmp/saved_args.yml
```

```yaml
analyze.results_folder: ./results

download.folder: /data/raw

evaluate.folder: /data/processed/test/
evaluate.model_path: checkpoints/model.pth
evaluate.results_folder: ./results

output.folder: /tmp/output

preprocess.dst_folder: /data/processed
preprocess.src_folder: /data/raw

run.stages:
- train
- evaluate
- analyze

train.epochs: 100
train.folder: /data/processed/train/
train.lr: 0.001
train.model_path: checkpoints/model.pth
train.model_type: conv
```

And we can run it again if we want, without specifying everything:

```
python examples/multistage/multistage.py --args.load /tmp/saved_args.yml
```

Or re-run the same experiment, but tweak the learning rate and save everything to a different folder:

```
❯ python examples/multistage/multistage.py --args.load /tmp/saved_args.yml --train.lr .1 --output.folder /tmp/output2
Making output folder /tmp/output2.
Switched working directory to /tmp/output2
STAGE: TRAIN
Training model conv on data in /data/processed/train/ for 100 epochs, with learning rate of 0.1

STAGE: EVALUATE
Evaluating model checkpoints/model.pth on /data/processed/test/, saving results to ./results

STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```

What if we specify a stage that doesn't exist? The `run_stages` function is written 
in the script to throw a helpful error:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output --run.stages "non_existent_stage"
Making output folder /tmp/output.
Switched working directory to /tmp/output
Returning to original folder
Traceback (most recent call last):
  File "examples/multistage/multistage.py", line 162, in <module>
    run()
  File "/Users/prem/research/argbind/argbind/argbind.py", line 84, in cmd_func
    return func(*args, **kwargs)
  File "examples/multistage/multistage.py", line 153, in run
    raise ValueError(
ValueError: Requested stage non_existent_stage not in known stages ['download', 'preprocess', 'train', 'evaluate', 'analyze']
```

For our final trick, let's look at the script with `--args.debug 1`:

```
❯ python examples/multistage/multistage.py --output.folder /tmp/output --args.debug 1
run(
  stages : list = ['download', 'preprocess', 'train', 'evaluate', 'analyze']
)
output(
  folder : str = /tmp/output
)
Making output folder /tmp/output.
Switched working directory to /tmp/output
download(
  folder : str = /data/raw
)
STAGE: DOWNLOAD
Downloading data to /data/raw

preprocess(
  src_folder : str = /data/raw
  dst_folder : str = /data/processed
)
STAGE: PREPROCESS
Preprocessing /data/raw into /data/processed

train(
  folder : str = /data/processed/train/
  epochs : int = 50
  lr : float = 0.001
  model_type : str = conv
  model_path : str = checkpoints/model.pth
)
STAGE: TRAIN
Training model conv on data in /data/processed/train/ for 50 epochs, with learning rate of 0.001

evaluate(
  model_path : str = checkpoints/model.pth
  folder : str = /data/processed/test/
  results_folder : str = ./results
)
STAGE: EVALUATE
Evaluating model checkpoints/model.pth on /data/processed/test/, saving results to ./results

analyze(
  results_folder : str = ./results
)
STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```

This is one way to structure a multi-stage program with ArgBind. 
Check out the full script for more details!

## Making each function a subcommand

You may want to structure your programs as one with subprograms, which can be specified like this:

```
python program.py subprogram --sub_program.arg1=...
```

You can do this in ArgBind by using `positional=True` in the `run` function:

```python
@argbind.bind(without_prefix=True, positional=True)
def run(stage : str):
    """Run stages.

    Parameters
    ----------
    stages : str
        Stage to run
    """
    with output():
        if stage not in STAGES:
            raise ValueError(
                f"Requested stage {stage} not in known stages {STAGES}"
            )
        stage_fn = globals()[stage]
        stage_fn()
```

Then, you can run each stage independently as its own program like so:

```
❯ python examples/multistage/multistage_with_subcommands.py download
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: DOWNLOAD
Downloading data to /data/raw

Returning to original folder
❯ python examples/multistage/multistage_with_subcommands.py preprocess
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: PREPROCESS
Preprocessing /data/raw into /data/processed

Returning to original folder
❯ python examples/multistage/multistage_with_subcommands.py train
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: TRAIN
Training model conv on data in /data/processed/train/ for 50 epochs, with learning rate of 0.001

Returning to original folder
❯ python examples/multistage/multistage_with_subcommands.py evaluate
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: EVALUATE
Evaluating model checkpoints/model.pth on /data/processed/test/, saving results to ./results

Returning to original folder
❯ python examples/multistage/multistage_with_subcommands.py analyze
Making output folder /tmp/output.
Switched working directory to /tmp/output
STAGE: ANALYZE
Generating plots for ./results

Returning to original folder
```