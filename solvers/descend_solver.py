import numpy as np
import time
import math

import Schedule as sch
from Instance import Instance
import Schedule as sc
import solvers.greedy_solver as gs




class DescendSolver(object):
    def __init__(self, instance: Instance):
        self.machines = instance.machines
        self.durations = instance.durations
        self.number_of_jobs = instance.numJobs
        self.number_of_tasks = instance.numTasks


    def solve_descend(self, method_list,timeout):
        results = []
        instance = Instance()
        instance.durations = self.durations
        instance.machines = self.machines
        instance.numJobs = self.number_of_jobs
        instance.numTasks = self.number_of_tasks
        gs_solver = gs.GreedySolver(instance)

        for gredy_method in method_list:
            if gredy_method == 'spt':
                job_list, resource = gs_solver.run_spt()
            if gredy_method == 'lpt':
                job_list, resource = gs_solver.run_lpt()
            if gredy_method == 'lrpt':
                job_list, resource = gs_solver.run_lrpt()
            if gredy_method == 'est_spt':
                job_list, resource = gs_solver.run_est_spt()
            if gredy_method == 'est_lrpt':
                job_list, resource = gs_solver.run_est_lrpt()

            start = time.time()
            makespan, _ = self.descent_solver(resource, timeout)
            end = time.time()
            results.append([end - start, makespan])


        return results



    def descent_solver(self, solution, timeout=1200):

        instance = Instance()
        instance.durations = self.durations
        instance.machines = self.machines
        instance.numJobs = self.number_of_jobs
        instance.numTasks = self.number_of_tasks

        best_solution = solution
        best_detailed_ressource = sch.detailed_representation(best_solution,instance)
        makespan = sch.evaluate_detailed_represenation(best_detailed_ressource,instance)
        critical_path = sch.critical_path(instance, best_detailed_ressource, makespan, best_solution)

        list_makespan = [makespan]

        start = time.time()
        while time.time() < start + timeout:
            # blocks of critical path
            blocks = self.blocks_from_critical_path(critical_path, self.machines)

            # list of neighboring solutions
            all_neighbors = self.return_all_neighbors(blocks, best_solution, self.machines)

            # best neighbor
            best_voisin, best_voisin_sol, best_voisin_detail = self.choose_best_neighbor(all_neighbors, instance)

            # update solution if better than previous one
            if best_voisin < makespan:
                makespan = best_voisin
                list_makespan.append(makespan)
                best_solution = best_voisin_sol
                best_detail = best_voisin_detail
                path = sch.critical_path(instance, best_detail, makespan,  best_solution)

            else:
                break

        return makespan, best_solution

    def return_all_neighbors(self,blocks, solution, machines):
        all_neighbors = []
        for i in range(len(blocks)):
            b = blocks[i]
            new_solution = self.solution_generated_by_neighborhood(b, solution, machines)
            all_neighbors.extend(new_solution)
        return all_neighbors

    def solution_generated_by_neighborhood(self,bloc, ressource, machines):

        machine = machines[bloc[0][0], bloc[0][1]]


        list_solutions = []

        list_neighbors = []

        # permute
        neighbor_1 = []
        neighbor_1.extend(bloc)
        neighbor_1[1], neighbor_1[0] = neighbor_1[0], neighbor_1[1]
        list_neighbors.append(neighbor_1)

        new_solution = sch.duplicate_ressource(ressource)
        index = new_solution[machine].index((bloc[0]))


        new_solution[machine][index-1], new_solution[machine][index ] = new_solution[machine][index ], new_solution[machine][index-1]
        list_solutions.append(new_solution)

        if len(bloc) > 2:
            # permute the last one
            neighbor_2 = []
            neighbor_2.extend(bloc)
            neighbor_2[-1], neighbor_2[-2] = neighbor_2[-2], neighbor_2[-1]
            list_neighbors.append(neighbor_2)

            new_solution = sch.duplicate_ressource(ressource)
            index = new_solution[machine].index((bloc[-1]))
            new_solution[machine][index - 1], new_solution[machine][index] = new_solution[machine][index], \
                                                                             new_solution[machine][index - 1]
            list_solutions.append(new_solution)

        return list_solutions

    def blocks_from_critical_path(self,critical_path, machines):

        blocks = []
        bloc = []

        precedent_machine = machines[critical_path[0]]  # initialisation
        bloc.append(critical_path[0])

        for task in critical_path:
            if precedent_machine == sch.get_ressource(machines, task[0], task[1]):
                bloc.append(task)
            else:
                blocks.append(bloc)
                bloc = [task]

            precedent_machine = sch.get_ressource(machines, task[0], task[1])  # mise à jour machine prcedente

        blocks.append(bloc)

        blocks = [b for b in blocks if len(b) > 1]

        return blocks

    def choose_best_neighbor(self, all_neighbors, instance):

        best_neighbor = math.inf
        for solution in all_neighbors:
            new_detail= sch.detailed_representation(solution, instance)
            new_eval  = sch.evaluate_detailed_represenation(new_detail, instance)

            if new_eval < best_neighbor:
                best_neighbor = new_eval
                best_neighbor_solution = solution
                best_neighbor_detail = new_detail
        return best_neighbor, best_neighbor_solution, best_neighbor_detail
