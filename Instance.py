import numpy as np
import logging
from Task import Task


class Instance:
    def __init__(self, numJobs=0, numTasks=0):
        super(Instance, self).__init__()
        self.numJobs = numJobs
        self.numTasks = numTasks
        self.numMachines = numTasks
        self.durations = np.zeros((numJobs, numTasks))
        self.machines = np.zeros((numJobs, numTasks), dtype=int)

    def machine(self, *kwargs):
        if isinstance(kwargs[0], Task):
            return self.machine(kwargs[0].job, kwargs[0].task)
        else:
            job = kwargs[0]
            task = kwargs[1]
            return self.machines[job, task]

    def duration(self, *kwargs):
        if isinstance(kwargs[0], Task):
            return self.durations[kwargs[0].job, kwargs[0].task]
        else:
            job = kwargs[0]
            task = kwargs[1]
            return self.durations[job, task]

    def task_with_machine(self, job, wanted_machine):

        for task in range(self.numTasks):
            if self.machines[job,task] == wanted_machine:
                return task
        print("No task targeting machine "+ str(wanted_machine)+" on job "+str(job))
        return None

    @staticmethod
    def fromFile(path):
        with open(path, "r") as file:
            lines = file.readlines()
            init = 0
            for i in range(len(lines)):
                line = lines[i]
                line_params = line.strip().split()
                if line_params[0] != "#" and len(line_params) == 2:
                    num_jobs = int(line_params[0])
                    num_task = int(line_params[1])
                    logging.debug("num_jobs:"+str(num_jobs))
                    logging.debug("num_task:" + str(num_task))
                    init = i

            pb = Instance(num_jobs, num_task)
            for job in range(num_jobs):
                line_par = lines[init+1].strip().split()
                for task, step in zip(range(num_task), range(0, len(line_par), 2)):
                    pb.machines[job, task] = int(line_par[step])
                    pb.durations[job, task] = int(line_par[step+1])

                init += 1
            return pb

    def __str__(self):
        return "Instance numJobs:"+ str(self.numJobs)+"; numTasks:"+ str(self.numTasks)+"; numMachines:"+str(self.numMachines)