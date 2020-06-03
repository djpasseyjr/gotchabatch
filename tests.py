from .generate_jobs import *
import os
import numpy as np
import pathlib
DIR = str(pathlib.Path(__file__).parent.absolute())

def empty_test_dir():
    test_dir = DIR + "/GeneratedJobs/test_job/"
    job_dir = test_dir + 'jobfiles/'
    save_dir = test_dir + 'savefiles/'
    for f in os.listdir(job_dir):
        os.remove(job_dir + f)
    os.rmdir(job_dir)
    os.rmdir(save_dir)
    os.rmdir(test_dir)

def rm_test_bash():
    test_bash = DIR + "/test_job.sh"
    if os.path.exists(test_bash):
        os.unlink(test_bash)

def test_job_gen():
    if os.path.exists(DIR + "/GeneratedJobs/test_job"):
        empty_test_dir()
    args = [(np.random.rand(5)) for i in range(95)]
    func_path = "/Users/djpassey/Code/gotchabatch/generate_jobs.py"
    func = "fake_func"
    fprefix = "test_job"
    generate_jobs(func, func_path, fprefix,  args, 10, 1, 2)
    assert len(os.listdir(DIR + "/GeneratedJobs/test_job/jobfiles")) == 10
    empty_test_dir()
    rm_test_bash()



test_job_gen()
