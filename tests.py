from generate_jobs import *
import os
import numpy as np

def empty_test_dir():
    test_dir = "GeneratedJobs/test_job"
    for f in os.readdir(test_dir):
        os.remove(f)
    os.rmdir(test_dir)

def test_job_gen():
    if os.path.exists("GeneratedJobs/test_job"):
        empty_test_dir()
    args = [(np.random.rand(5)) for i in range(100)]
    imports = "import numpy as np"
    func = "fake_func"
    fprefix = "test_job"
    generate_jobs(fprefix, imports, func, args, 10, 1, 2)
    assert len(os.listdir("GeneratedJobs/test_job")) == 10
    empty_test_dir()


test_job_gen()
