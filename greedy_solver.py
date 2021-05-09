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

    def run_lrpt(self):
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

    def run_est_stp(self):
        resource = [[] for _ in range(self.number_of_tasks)]
        job_list = []

        # Initialise schedulable tasks with the first tasks of all jobs
        first_task = 0
        schedulable_tasks = [(job, first_task) for job in range(self.number_of_jobs)]

        scheduled_tasks = [[] for _ in range(self.number_of_jobs)]
        schedulable_task_exists = True

        while schedulable_task_exists:
            earliest_start_times = []
            for (job, task) in schedulable_tasks:
                used_machine = self.machines[job, task]
                if len(resource[used_machine]) > 0:
                    j, t = resource[used_machine][-1]
                    used_machine_ready = scheduled_tasks[j][t] + self.durations[j, t]
                if len(resource[used_machine]) == 0:
                    used_machine_ready = 0
                if task > 0:
                    prev_task_completed_time = scheduled_tasks[job][task - 1] + self.durations[job, task - 1]
                elif task == 0:
                    prev_task_completed_time = 0
                earliest_start_times.append(max(used_machine_ready, prev_task_completed_time))

            est_among_all = min(earliest_start_times)
            eligible_tasks = [task for index, task in enumerate(schedulable_tasks) if earliest_start_times[index] == est_among_all]

            if len(eligible_tasks) != 1:
                processing_times = []
                for (job, task) in eligible_tasks:
                    processing_time = self.durations[job, task]
                    processing_times.append(processing_time)
                task_to_schedule = eligible_tasks[np.argmin(np.array(processing_times))]

            elif len(eligible_tasks) == 1:
                task_to_schedule = eligible_tasks[0]
                index_of_task_to_schedule = self.machines[task_to_schedule]
            resource[index_of_task_to_schedule].append(task_to_schedule)

            job, task = task_to_schedule
            job_list.append(job)
            scheduled_tasks[job].append(est_among_all)  #
            schedulable_tasks.remove(task_to_schedule)
            if task < self.number_of_tasks - 1:
                schedulable_tasks.append((job, task + 1))
            schedulable_task_exists = len(schedulable_tasks) != 0
        return job_list, resource

    def run_est_lrpt(self):
        # Initialise schedulable tasks with the first tasks of all jobs
        first_task = 0
        schedulable_tasks = [(job, first_task) for job in range(self.number_of_jobs)]

        resource = [[] for _ in range(self.number_of_tasks)]
        job_list = list()

        scheduled_tasks = [[] for _ in range(self.number_of_jobs)]
        remaining_task_per_job = [[] for _ in range(self.number_of_jobs)]

        # initialisation
        for i in range(self.number_of_jobs):
            for job in range(self.number_of_tasks):
                remaining_task_per_job[i].append((i, job))
        schedulable_task_exists = True
        while schedulable_task_exists:

            earliest_start_times = []

            for (job, task) in schedulable_tasks:
                used_machine = self.machines[job, task]
                if len(resource[used_machine]) > 0:
                    j, t = resource[used_machine][-1]
                    used_machine_ready = scheduled_tasks[j][t] + self.durations[j, t]
                if len(resource[used_machine]) == 0:
                    used_machine_ready = 0

                if task > 0:
                    prev_task_completed_time = scheduled_tasks[job][task - 1] + self.durations[job, task - 1]
                if task == 0:
                    prev_task_completed_time = 0

                earliest_start_times.append(max(used_machine_ready, prev_task_completed_time))

            est_among_all = min(earliest_start_times)
            eligible_tasks = [task for index, task in enumerate(schedulable_tasks) if earliest_start_times[index] == est_among_all]

            if len(eligible_tasks) == 1:
                task_to_schedule = eligible_tasks[0]

            if len(eligible_tasks) > 1:
                eligible_jobs = [job for job, task in eligible_tasks]
                remaining_processing_times = [0] * self.number_of_jobs

                for i in eligible_jobs:
                    for job, task in remaining_task_per_job[i]:
                        remaining_processing_times[i] +=  self.durations[job, task]

                max_j = np.argmax(np.array(remaining_processing_times))

                for job, task in eligible_tasks:
                    if job == max_j:
                        task_to_schedule = job, task

            index_of_task_to_schedule = self.machines[task_to_schedule]
            resource[index_of_task_to_schedule].append(task_to_schedule)

            job, task = task_to_schedule
            job_list.append(job)

            scheduled_tasks[job].append(est_among_all)
            schedulable_tasks.remove(task_to_schedule)
            remaining_task_per_job[job].remove(task_to_schedule)
            if task < self.number_of_tasks - 1:
                schedulable_tasks.append((job, task + 1))
            schedulable_task_exists = len(schedulable_tasks) != 0
        return job_list, resource
