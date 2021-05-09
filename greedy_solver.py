import numpy as np


class GreedySolver(object):
    def __init__(self, machines, durations, number_of_jobs, number_of_tasks):
        self.machines = machines
        self.durations = durations
        self.number_of_jobs = number_of_jobs
        self.number_of_tasks = number_of_tasks

    def run_stp(self):

        # Initialise schedulable tasks with the first tasks of all jobs
        first_task = 0
        schedulable_tasks = [(job, first_task) for job in range(self.number_of_jobs)]

        resource = [[] for _ in range(self.number_of_tasks)]
        job_list = list()

        scheduled_tasks = []
        schedulable_task_exists = True

        while schedulable_task_exists:
            # Choose the task with the SPT among  schedulable tasks
            tasks_durations = [self.durations[job, task] for (job, task) in schedulable_tasks]

            index_of_task_to_schedule = np.argmin(np.array(tasks_durations)) # The one with the shortest processing time
            task_to_schedule = schedulable_tasks[index_of_task_to_schedule]

            # Assign the needed machine to the task
            machine_used_by_task = self.machines[task_to_schedule]
            resource[machine_used_by_task].append(task_to_schedule)

            # Update job list
            job, task = task_to_schedule
            job_list.append(job)

            # Update schedulable tasks
            scheduled_tasks.append(task_to_schedule)
            schedulable_tasks.remove(task_to_schedule)

            if task < self.number_of_tasks - 1:
                schedulable_tasks.append((job, task + 1))
            schedulable_task_exists = len(schedulable_tasks) != 0
        return job_list, resource

    def run_lrtp(self):
        # Initialise schedulable tasks with the first tasks of all jobs
        first_task = 0
        schedulable_tasks = [(job, first_task) for job in range(self.number_of_jobs)]

        resource = [[] for _ in range(self.number_of_tasks)]
        job_list = list()

        scheduled_tasks = []
        remaining_task_per_job = [[] for _ in range(self.number_of_tasks)]

        for job in range(self.number_of_jobs):
            for task in range(self.number_of_tasks):
                remaining_task_per_job[job].append((job, task))

        schedulable_task_exists = True

        while schedulable_task_exists:
            remaining_processing_times = [0] * self.number_of_jobs

            # compute the remaining processing time of each job
            for a_job in range(self.number_of_jobs):
                for job, task in remaining_task_per_job[a_job]:
                    remaining_processing_times[a_job] += self.durations[job, task]

            job_with_lrpt = np.argmax(np.array(remaining_processing_times))  # The job with the LRPT

            for job, task in schedulable_tasks:
                if job == job_with_lrpt:
                    task_to_schedule = job, task
                    index_of_task_to_schedule = self.machines[task_to_schedule]
                    resource[index_of_task_to_schedule].append(task_to_schedule)
                    job, task = task_to_schedule
                    job_list.append(job)

                    scheduled_tasks.append(task_to_schedule)
                    schedulable_tasks.remove(task_to_schedule)
                    remaining_task_per_job[job].remove(task_to_schedule)
                    if task < self.number_of_tasks - 1:
                        schedulable_tasks.append((job, task + 1))
                    break

            schedulable_task_exists = len(schedulable_tasks) != 0

        return job_list, resource
