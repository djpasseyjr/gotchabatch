# gotchabatch: Generate slurm batches of python files
Automated file writing to distribute function calls with slurm

## Overview

Sometimes you want to run the same code thousands of times with slightly different parameters and compare results. (i.e. Hyper parameter tuning) This code makes it easy to do that on a super computer that uses slurm. To use this package, you need:

1. A function that you would like to call multiple times. This function must accept a single keyword argument, `save_file`. Each time the function is called, a unique `.pkl` file name will be passed to the `save_file` keyword argument. (This is so the output of the function can be saved if desired.)
2. Path to the `.py` file containing the function described in (1).
3. All different function arguments as a list of n-tuples. Each tuple will be unpacked and passed to the function described in (1) so the function must accept n arguments. Alternatively, the user can supply an n-tuple of lists and the script will take the cartesian product of the lists to form a list of n-tuples.

## Example

## Installation
