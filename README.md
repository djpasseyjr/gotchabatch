# gotchabatch: Generate slurm batches of python files
Automated file writing to distribute function calls with slurm

## Overview

Want to run the same code thousands of times with slightly different parameters and then compare the results? (i.e. Hyper parameter tuning.) This code will simplify the process by writing all the jobs and then generate a slurm script to run all of the jobs. To use this package, you need:

1. A function that you would like to call multiple times. This function must accept a keyword argument, `save_file`. Each time the function is called, a unique `.pkl` file name will be passed to the `save_file` keyword argument. (This is so the output of the function can be saved if desired.)
2. Path to the `.py` file containing the function described in (1).
3. All different function arguments as a list of n-tuples. Each tuple will be unpacked and passed to the function described in (1) so the function must accept n arguments. Alternatively, the user can supply an n-tuple of lists and the script will take the cartesian product of the lists to form a list of n-tuples.

## Example

Let's assume you have a file `path/to/file/statistical_experiment.py` and inside the file you
define a function `bayesian_experiment` that accepts 3 parameters and a `save_file` keyword argument.
If you want to run this function 1000 times and save the results of each run, you can do the following:

__Option 1__
The `main.py` file explains in detail each variable. Setting each constant in `main.py` correctly and running the file will generate job files and a bash script that submits them using slurm. Keeping with this example, the constants in `main.py` might be set to:

```
FUNCTION_NAME = "bayesian_experiment"

FUNCTION_FILE_PATH = "path/to/file/statistical_experiment.py"

ARGS = (
    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
)


FILE_PREFIX = "bayes"

CALLS_PER_JOB = 100

HOURS_PER_JOB = 10

GIGS_PER_CALL = 8
```

### Notes

* Setting `CALLS_PER_JOB = 100` and `HOURS_PER_JOB = 2` informs the script to allocate
10 hours for the job of executing `bayesian_experiment` 100 times. (Thus a single call to
`bayesian_experiment` should execute in under 6 minutes)

* The total number of calls to `bayesian_experiment` will be equal to number of combinations of arguments (or the length or `ARGS` if `ARGS` is a list of tuples instead of a tuple of lists)

* The number of jobs will be equal to the number of calls to `bayesian_experiment` divided by `CALLS_PER_JOB`. This number must be less than 1000 or the slurm batch won't work

## Installation

This repo is not a registered python package yet. For now, just clone the repo and add the directory containing the repo to your `PYTHONPATH` variable

Clone this repo using:
```
git clone https://github.com/djpasseyjr/gotchabatch.git
```
Add directory containing `gotchabatch` to your PYTHONPATH by adding
```
export PYTHONPATH="${PYTHONPATH}:/path/to/directory/containing/repo/"
```
to the .bash_profile file in your home directory. (Create one if it doesn't exist.) Restart your bash session.

