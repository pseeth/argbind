import argbind
from typing import List
from pathlib import Path
import os
from contextlib import contextmanager

STAGES = ['download', 'preprocess', 'train', 'evaluate', 'analyze']

@argbind.bind()
@contextmanager
def output(folder : str = '/tmp/output'):
    """Controls the output folder where everything gets saved.
    Switches the scripts working directory to this folder.

    Parameters
    ----------
    folder : str, optional
        Output folder, everything is saved relative to this folder, by default '.'
    """
    print(f"Making output folder {folder}.")
    newdir = Path(folder)
    newdir.mkdir(parents=True, exist_ok=True)

    curdir = os.getcwd()
    try:
        os.chdir(newdir)
        print(f"Switched working directory to {newdir}")
        yield
    finally:
        os.chdir(curdir)
        print(f"Returning to original folder")

@argbind.bind()
def download(
    folder : str = '/data/raw'
):
    """Download data to folder.

    Parameters
    ----------
    folder : str, optional
        Absolute path to folder to download data to, by default '/data/raw'
    """
    folder = Path(folder)
    print("STAGE: DOWNLOAD")
    print(f"Downloading data to {folder}")
    print()

@argbind.bind()
def preprocess(
    src_folder : str = '/data/raw',
    dst_folder : str = '/data/processed'
):
    """Preprocess data.

    Parameters
    ----------
    src_folder : str, optional
        Absolute path to raw data, by default '/data/raw'
    dst_folder : str, optional
        Absolute path where preprocessed data is placed, by default '/data/processed'
    """
    src_folder = Path(src_folder)
    dst_folder = Path(dst_folder)
    print(f"STAGE: PREPROCESS")
    print(f"Preprocessing {src_folder} into {dst_folder}")
    print()

@argbind.bind()
def train(
    folder : str = '/data/processed/train/',
    epochs : int = 50,
    lr : float = 1e-3,
    model_type : str = 'conv',
    model_path : str = 'checkpoints/model.pth'
):
    """Train the model.

    Parameters
    ----------
    folder : str, optional
        Folder to train from, by default '/data/processed/train/'
    epochs : int, optional
        Number of epochs, by default 50
    lr : float, optional
        Learning rate, by default 1e-3
    model_type : str, optional
        Type of model, by default 'conv'
    model_path : str, optional
        Where to save model to, by default 'checkpoints/model.pth'
    """
    print("STAGE: TRAIN")
    print(f"Training model {model_type} on data in {folder} "
          f"for {epochs} epochs, with learning rate of {lr}")
    Path(model_path).parent.mkdir(exist_ok=True, parents=True)
    Path(model_path).touch()
    print()

@argbind.bind()
def evaluate(
    model_path : str = 'checkpoints/model.pth',
    folder : str = '/data/processed/test/',
    results_folder : str = './results'
):
    """Evaluate the model.

    Parameters
    ----------
    model_path : str, optional
        Path to model to evaluate, by default 'checkpoints/model.pth'
    folder : str, optional
        Folder containing data to evaluate model on, by default '/data/processed/test/'
    results_folder : str, optional
        Folder to save results into, by default './results'
    """
    print("STAGE: EVALUATE")
    print(f"Evaluating model {model_path} on {folder}, "
          f"saving results to {results_folder}")
    Path(results_folder).mkdir(parents=True, exist_ok=True)
    (Path(results_folder) / 'example.npy').touch()
    print()

@argbind.bind()
def analyze(
    results_folder : str = './results'
):
    """Analyze model performance, make plots.

    Parameters
    ----------
    results_folder : str, optional
        Folder where results are, by default './results'
    """
    print("STAGE: ANALYZE")
    print(f"Generating plots for {results_folder}")
    (Path(results_folder) / 'example.png').touch()
    print()

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

if __name__ == "__main__":
    args = argbind.parse_args()
    with argbind.scope(args):
        run()
