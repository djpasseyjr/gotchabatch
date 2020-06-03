import os
from itertools import product

def generate_jobs(fprefix, imports, func, func_args, calls_per_job, hours_per_job, gigs_per_call):
    """ Generate jobs for super computing

        Parameters
        ----------
        fprefix (string): Prefix for job files and their corresponding output files
        imports (string): A string containing the import statements to use at the
            beginning of an experiment file
        func (string): The name of experiment function to call during a job. This
            function must accept exactly on keyword argument: `save_file`
        func_args (n-tuple of lists) or (list of n-tuples): Arguments to be passed
            to `func` during experiments. The function `func` must accept exactly
            n non-keyword arguments.
        calls_per_job (int): How calls to func should happen in one job
        hours_per_job (int): Time to allocated to each job. Equal to
            `calls_per_job` * (time it takes to execute `func`). Minimum of one hour
        gigs_per_call (int): RAM needed to preform a call to `func`
    """
    # Create directory for storing job files
    jobdir = "GeneratedJobs/" + fprefix
    if os.path.exists(jobdir):
        raise ValueError(f"Supplied file prefix: {fprefix}, was already used to generate jobs")
    os.mkdir(jobdir)

    if isinstance(func_args, tuple) and isinstance(func_args[0], list):
        func_args = product(*func_args)
    else:
        if not isinstance(func_args, list) and isinstance(func_args[0], tuple):
            raise ValueError("Incorrect type for `func_args` parameter. Must be tuple of lists or list of tuples ")

    # Initialize loop variables
    job_idx = 1
    output_idx = 1
    job_file = jobdir + '/' + fprefix + '_' + str(job_idx) + '.py'
    output_file = jobdir + '/' + fprefix + '_' + str(output_idx) + '.pkl'
    fcontents = imports + '\n'
    call_count = 0

    for fargs in func_args:
        if call_count == calls_per_job:
            fstream = open(job_file, 'w')
            fstream.write(fcontents)
            fstream.close()
            job_idx += 1
            # New job file name
            job_file = jobdir + '/' + fprefix + '_' + str(job_idx) + '.py'
            fcontents = imports + '\n'
            call_count = 0
        # Write a single call to `func` into the job file
        fcontents += "\nargs = " + str(fargs)
        fcontents += '\n' + func + "(*args, save_file=\"" + output_file + "\") \n"
        call_count += 1
        # Increment output file name
        output_idx += 1
        output_file = jobdir + '/' + fprefix + '_' + str(output_idx) + '.pkl'

    # Save leftover calls into a file
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

    directory = "GeneratedJobs/" + fprefix
    tmpl_stream = open('bash_template.sh', 'r')
    tmpl_str = tmpl_stream.read()
    tmpl_str = tmpl_str.replace("#HOURS#", str(hours_per_job))
    tmpl_str = tmpl_str.replace("#MEMORY#", str(gigs_per_call))
    tmpl_str = tmpl_str.replace("#DIR#", directory)
    tmpl_str = tmpl_str.replace("#FNAME#", fprefix)
    # Adjust number of experiments to match slurm job array endpoint inclusion
    tmpl_str = tmpl_str.replace("#NUMBER_JOBS#", str(number_of_jobs - 1))
    new_f = open(fprefix + '.sh', 'w')
    new_f.write(tmpl_str)
    new_f.close()
    print('NEXT: sbatch', fprefix + '.sh')
