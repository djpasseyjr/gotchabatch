import os
import pathlib
from itertools import product
DIR = str(pathlib.Path(__file__).parent.absolute())

def generate_jobs(func, func_path, fprefix, func_args, calls_per_job, hours_per_job, gigs_per_call):
    """ Generate jobs for super computing

        Parameters
        ----------
        func (string): The name of function to call during a job. This
            function must accept exactly one keyword argument: `save_file`
        func_path (string): Path of file containing `func` definition
        fprefix (string): Prefix for job files and their corresponding output files
        func_args (n-tuple of lists) or (list of n-tuples): Arguments to be passed
            to `func` during experiments. The function `func` must accept
            n non-keyword arguments.
        calls_per_job (int): How calls to func should happen in one job
        hours_per_job (int): Time to allocated to each job. Equal to
            `calls_per_job` * (time it takes to execute `func`). Minimum of one hour
        gigs_per_call (int): RAM needed to preform a single call to `func`
    """

    # Check arguments
    if isinstance(func_args, tuple) and isinstance(func_args[0], list):
        func_args = list(product(*func_args))
    else:
        if not (isinstance(func_args, list) or isinstance(func_args[0], tuple)):
            raise ValueError("Incorrect type for `func_args` parameter. Must be tuple of lists or list of tuples ")
    if  len(func_args) / calls_per_job > 1000:
        raise ValueError("Number of jobs exceeds 1000: increase `calls_per_job`")

    # Create directory for storing job files
    jobdir = DIR + "/GeneratedJobs/" + fprefix

    if os.path.exists(jobdir):
        raise ValueError(f"Supplied file prefix: {fprefix}, was already used to generate jobs")
    os.mkdir(jobdir)
    os.mkdir(jobdir + "/jobfiles")
    os.mkdir(jobdir + "/savefiles")

    # Make import statements
    imports = make_import_script(func, func_path, jobdir)

    # Initialize loop variables
    job_idx = 0
    output_idx = 0
    job_file = jobdir + '/jobfiles/' + fprefix + '_' + str(job_idx) + '.py'
    output_file = fprefix + '_' + str(output_idx) + '.pkl'
    fcontents = imports
    call_count = 0

    for fargs in func_args:
        if call_count == calls_per_job:
            # Save job file
            fstream = open(job_file, 'w')
            fstream.write(fcontents)
            fstream.close()
            job_idx += 1
            # Increment job file name
            job_file = jobdir + '/jobfiles/' + fprefix + '_' + str(job_idx) + '.py'
            # Start new job file contents
            fcontents = imports
            call_count = 0
        # Write a single call to `func` into the job file
        fcontents += "\nargs = " + str(fargs)
        fcontents += '\n' + func + "(*args, save_file=\"" + output_file + "\") \n"
        call_count += 1
        # Increment output file name
        output_idx += 1
        output_file = fprefix + '_' + str(output_idx) + '.pkl'

    # Save leftover calls into a file
    if call_count != 0:
        fstream = open(job_file, 'w')
        fstream.write(fcontents)
        fstream.close()
        
    write_bash_script(fprefix, job_idx, hours_per_job, gigs_per_call)


def write_bash_script(
    fprefix,
    number_of_jobs,
    hours_per_job,
    gigs_per_call
):
    """
    Write the bash script to run all the experiments and write a bash_script to cleanup the directory
    where all the files were created for that batch, write a post_batch completion script to compile output
    Parameters:
        fprefix                (str): the filename prefix that all the files have in common
        number_of_experiments   (int): the number of experiments is used to systematically
                                        compile all individual output files into one primary file
        hours_per_job               (int): this parameter is passed to write_bash_script
        minutes_per_job             (int): this parameter is passed to write_bash_script
        memory_per_job              (int): Gigabytes, input for --mem-per-cpu slurm command in bash_template
    """
    if not isinstance(gigs_per_call, int) and not isinstance(gigs_per_call, float):
        raise ValueError('memory should be an int or float')
    if not isinstance(hours_per_job, int) and not isinstance(hours_per_job, float):
        raise ValueError('hours_per_job should be an int or float')

    directory = DIR + "/GeneratedJobs/" + fprefix + "/jobfiles"
    save_dir = DIR + "/GeneratedJobs/" + fprefix + "/savefiles"

    tmpl_stream = open(DIR + '/bash_template.sh', 'r')
    tmpl_str = tmpl_stream.read()
    tmpl_str = tmpl_str.replace("#HOURS#", str(hours_per_job))
    tmpl_str = tmpl_str.replace("#MEMORY#", str(gigs_per_call))
    tmpl_str = tmpl_str.replace("#DIR#", directory)
    tmpl_str = tmpl_str.replace("#FNAME#", fprefix)
    tmpl_str = tmpl_str.replace("#OUTDIR#", save_dir)

    # Adjust number of experiments to match slurm job array endpoint inclusion
    tmpl_str = tmpl_str.replace("#NUMBER_JOBS#", str(number_of_jobs))
    new_f = open(fprefix + '.sh', 'w')
    new_f.write(tmpl_str)
    new_f.close()
    print('NEXT: sbatch', fprefix + '.sh')

def make_import_script(func, func_path, jobdir):
    if not os.path.exists(func_path):
        raise ValueError(f"Function file \"{func_path}\"  does not exist")

    fstart = func_path.rfind('/') + 1
    fstop = func_path.rfind(".")
    file = func_path[fstart:fstop]
    dir = str(pathlib.Path(func_path).parent.absolute())
    imports = "import sys\n" + "sys.path.insert(1, \"" + dir + "\")\n"
    imports += "from " + file + " import " + func + "\n"
    imports += "import os \n os.chdir(\"" + jobdir + "/savefiles\")"
    return imports
