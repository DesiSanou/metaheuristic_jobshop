import numpy as np


class GreedySolver():
    def __init__(self, machines, durations, number_of_jobs, number_of_tasks):
        self.machines = machines
        self.durations = durations
        self.number_of_jobs = number_of_jobs
        self.number_of_tasks = number_of_tasks
        self.resource = [[] for _ in range(self.number_of_tasks)]
        self.job_list = list()

    def greedy_stp(self):

        # Initialise schedulable tasks with the first tasks of all jobs
        first_task = 0
        schedulable_tasks = [(job, first_task) for job in range(self.number_of_jobs)]

        scheduled_tasks = []
        schedulable_task_exists = True

        while schedulable_task_exists:
            # Choose the task with the SPT among  schedulable tasks
            tasks_durations = [self.durations[job, task] for (job, task) in schedulable_tasks]

            index_of_task_to_schedule = np.argmin(np.array(tasks_durations)) # The one with the shortest processing time
            task_to_schedule = schedulable_tasks[index_of_task_to_schedule]

            # Assign the needed machine to the task
            machine_used_by_task = self.machines[task_to_schedule]
            self.resource[machine_used_by_task].append(task_to_schedule)

            # Update job list
            job, task = task_to_schedule
            self.job_list.append(job)

            # Update schedulable tasks
            scheduled_tasks.append(task_to_schedule)
            schedulable_tasks.remove(task_to_schedule)

            if task < self.number_of_tasks - 1:
                schedulable_tasks.append((job, task + 1))
            schedulable_task_exists = len(schedulable_tasks) != 0
        return self.job_list, self.resource
