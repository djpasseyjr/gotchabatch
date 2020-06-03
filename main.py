from generate_jobs import generate_jobs

# Job files will be named `FILE_PREFIX + job_number + ".py"` and corresponding
# job output files will be named `FILE_PREFIX + job_number + ".pkl"` (where
# `job_number` is generated during the file generation process)
FILE_PREFIX = "job"

# User defined import statements
IMPORT_STATEMENTS = "\nimport numpy as np\nimport sys"

# User defined experiment function name. It should be imported with the import
# statements above. The function must accept the keyword argument `save_file`
# which will indicate the name given to the output file of the experiment.
EXPERIMENT_FUNCTION_NAME = "experiment"
EXPERIMENT_FUNCTION_FILE_LOCATION = ""

# Args must be either
#     1. A list of n-tuples where each ntuple will be passed unpacked to the experiment function
#     2. A n-tuple of lists. The cartesian product of all lists will be generated and
#        the corresponding n-tuples will be passed to the experiment function
ARGS = (
    list(range(10)),
    ["uniform", "normal", "lognormal"],
    [1e-7, 1e-8, 1e-9, 1e-10]
)

# (int): How calls to `EXPERIMENT_FUNCTION_NAME` should happen in one job
CALLS_PER_JOB = 1

# (int): Time to allocated to each call to `EXPERIMENT_FUNCTION_NAME` (Must be
# at least one hour)
HOURS_PER_CALL = 12

# RAM needed to preform a call to `EXPERIMENT_FUNCTION_NAME`
GIGS_PER_CALL = 8

generate_jobs(
    FILE_PREFIX,
    IMPORT_STATEMENTS,
    EXPERIMENT_FUNCTION_NAME,
    ARGS,
    CALLS_PER_JOB,
    HOURS_PER_CALL,
    GIGS_PER_CALL
)
