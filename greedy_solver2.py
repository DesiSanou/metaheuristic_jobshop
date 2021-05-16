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



    def run_est_stp(self):
        ressource = [[] for _ in range(m)]  # matrice m*n
        list_job = []  # pour representation par job

        realisable = []

        # Initialisation : Déterminer l’ensemble des tâches réalisables (initialement, les premières tâches de tous les jobs)
        for i in range(n):
            realisable.append((i, 0))

        realisees = [[] for i in range(n)]  # par job, on stocke date de debut de chaque tache

        while (len(realisable) != 0):  # realisable peut redescendre à 0 et il reste des taches à realisées ??

            start_possible = []  # liste des dates de début possible ppour chaque tache realisable

            # On limites aux taches commencant au plus tot.
            # Trouver à quelle date peuvent commencer au plus tot chaque tache realisable
            for (j, o) in realisable:
                # index libre
                mac = machines[j, o]
                if len(ressource[mac]) > 0:
                    jm, om = ressource[mac][-1]
                    mac_ready = realisees[jm][om] + durations[jm, om]
                if len(ressource[mac]) == 0:
                    mac_ready = 0

                if o > 0:
                    # tache precedente finie
                    fin_prec = realisees[j][o - 1] + durations[j, o - 1]
                if o == 0:
                    fin_prec = 0

                start_possible.append(max(mac_ready, fin_prec))

            start = min(start_possible)
            # indices = start_possible.index(start) #ne fonctionne pas, renvoie uniquement la première valeure
            choisies = [value for index, value in enumerate(realisable) if start_possible[index] == start]

            if len(choisies) != 1:
                # Choisir une tâche dans cet ensemble, STP, la plus courte
                durees = []
                for (j, o) in choisies:
                    duree = durations[j, o]
                    durees.append(duree)
                next_t = choisies[np.argmin(np.array(durees))]

            if len(choisies) == 1:
                next_t = choisies[0]

            # Placer cette tâche sur la ressource qu’elle demande
            # (à la première place libre dans la représentation par ordre de passage)
            k = machines[next_t]
            ressource[k].append(next_t)

            j, o = next_t
            list_job.append(j)

            # Mettre à jour l’ensemble des tâches réalisables
            # On dit qu’une tâche est réalisable si tous ses prédécesseurs ont été traités
            realisees[j].append(start)  #

            realisable.remove(next_t)
            if o < m - 1:  # un job contient m taches
                # print((j,o+1)) #debug
                realisable.append((j, o + 1))

        # print(realisees) #debug
        # print(len(realisees)) #debug
        return list_job, ressource
