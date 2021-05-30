import copy
import logging

from Encoding import *
from Schedule import *
from Instance import Instance


class ResourceOrder(Encoding):
    def __init__(self, instance: Instance, task_by_machines):
        super(Encoding, self).__init__()
        self.instance = instance
        super(Instance)
        self.tasksByMachine = [None]*instance.numMachines
        for machine in range(instance.numMachines):
            tasks_on_machine = [Task(job=item[0], task= item[1]) for item in task_by_machines[machine]]
            self.tasksByMachine[machine] = tasks_on_machine

        self.nextFreeSlot = [0]*instance.numMachines

    def toschedule(self):
        # indicate for each task that have been scheduled, its start time
        startTimes = [[0]*self.instance.numTasks for _ in range(self.instance.numJobs)]

        # for each job, how many tasks have been scheduled (0 initially)
        nextToScheduleByJob = [0]*self.instance.numJobs

        # for each machine, how many tasks have been scheduled (0 initially)
        nextToScheduleByMachine = [0]*self.instance.numMachines

        # for each machine, earliest time at which the machine can be used
        releaseTimeOfMachine = [0]*self.instance.numMachines
        number_of_scheduled_task = 0
        any_match = True
        while any_match:
            schedulable = None
            tasks_that_are_next_to_schedule = [self.tasksByMachine[m][nextToScheduleByMachine[m]]
                                               for m in range(self.instance.numMachines)
                                               if nextToScheduleByMachine[m] < self.instance.numJobs]
            for mtask in tasks_that_are_next_to_schedule:
                if mtask.task == nextToScheduleByJob[mtask.job]:
                    schedulable = mtask
                    number_of_scheduled_task += 1
                    break
            if schedulable is not None:
                # we found a schedulable task, lets call it t
                t = schedulable
                machine = int( self.instance.machine(t.job, t.task) )
                if t.task == 0:
                    est = 0
                else:
                    est = startTimes[t.job][t.task-1] + self.instance.duration(t.job, t.task-1)
                index_release = int(self.instance.machine(t))
                est = max(est, releaseTimeOfMachine[index_release])
                startTimes[t.job][t.task] = est

                # mark the task as scheduled
                nextToScheduleByJob[t.job] += 1
                nextToScheduleByMachine[machine] += 1
                # increase the release time of the machine
                releaseTimeOfMachine[machine] = est + self.instance.duration(t.job, t.task)
            else:
                logging.warning("Number of tasks scheduled:" + str(number_of_scheduled_task))
                return None
            any_match_list = [nextToScheduleByJob[j] < self.instance.numTasks for j in range(self.instance.numJobs) ]
            any_match = True in any_match_list

        # we exited the loop : all tasks have been scheduled successfully
        logging.warning("Number of tasks scheduled:" + str(number_of_scheduled_task))
        return Schedule(self.instance, startTimes)

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        s = ""
        for m in range(self.instance.numMachines):
            s += "\nMachine " + str(m) + ":"
            tasks_str = ";".join([str(self.tasksByMachine[m][job]) for job in range(self.instance.numJobs)] ) #join tasks or machine m
            s += tasks_str + "\n"
        return s