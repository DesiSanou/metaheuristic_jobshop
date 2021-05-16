import logging
from Encoding import Encoding
from Instance import Instance
from Schedule import Schedule
from Task import Task


class JobNumbers(Encoding):
    def __init__(self, instance: Instance, job_list=None):
        self.nextToSet = 0
        self.instance = instance
        super(Instance)
        if job_list is None:
            self.jobs = [-1] * (self.instance.numJobs * self.instance.numMachines)
        else:
            self.jobs = job_list

    def toSchedule(self):
        nextFreeTimeResource = [0]* self.instance.numMachines
        nextTask = [0] * self.instance.numJobs
        taskList = [0] * self.instance.numTasks
        startTimes = [taskList for _ in range(self.instance.numJobs)]
        for job in self.jobs:
            task = nextTask[job]
            machine = int(self.instance.machine(job, task))

            est = 0 if task == 0 else startTimes[job][task-1] + self.instance.duration(job, task-1)
            est = max(est, nextFreeTimeResource[machine])

            startTimes[job][task] = est
            nextFreeTimeResource[machine] = est + self.instance.duration(job, task)
            nextTask[job] = task + 1
        return Schedule(self.instance, startTimes)

    def __str__(self):
        return str(self.jobs[0:self.nextToSet])

