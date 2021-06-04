import time
import math
from Instance import Instance
import Schedule as sch
import solvers.greedy_solver as gs



class TabooSolver(object):

    def __init__(self, instance: Instance):
        self.machines = instance.machines
        self.durations = instance.durations
        self.number_of_jobs = instance.numJobs
        self.number_of_tasks = instance.numTasks


    def solve_taboo(self, method_list,timeout, dureeTaboo, maxiter):
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
            makespan= self.taboo_solver(resource, timeout, dureeTaboo, maxiter)
            end = time.time()
            results.append([end - start, makespan])


        return results



    def voisinage_bloc_taboo(self,bloc, ressource, machines):

        j, o = bloc[0]
        mac = machines[j, o]


        new_sols = []
        liste_voisins = []
        liste_interdit = []

        # permutation
        voisin1 = []
        voisin1.extend(bloc)
        interdit = (voisin1[0][0], voisin1[1][0])
        voisin1[1], voisin1[0] = voisin1[0], voisin1[1]
        liste_voisins.append(voisin1)
        liste_interdit.append(interdit)

        new_sol = sch.duplicate_ressource(ressource)
        i = new_sol[mac].index((bloc[0]))
        new_sol[mac][i], new_sol[mac][i + 1] = new_sol[mac][i + 1], new_sol[mac][i]
        new_sols.append(new_sol)

        if len(bloc) > 2:
            voisin2 = []
            voisin2.extend(bloc)
            interdit = (voisin2[-2][0], voisin2[-1][0])
            voisin2[-1], voisin2[-2] = voisin2[-2], voisin2[-1]
            liste_voisins.append(voisin2)
            liste_interdit.append(interdit)

            new_sol = sch.duplicate_ressource(ressource)
            i = new_sol[mac].index((bloc[-1]))
            new_sol[mac][i - 1], new_sol[mac][i] = new_sol[mac][i], new_sol[mac][i - 1]
            new_sols.append(new_sol)

        return liste_voisins, new_sols, liste_interdit



    def taboo_solver(self,current_sol, timeout, dureeTaboo, maxiter):

        instance = Instance()
        instance.durations = self.durations
        instance.machines = self.machines
        instance.numJobs = self.number_of_jobs
        instance.numTasks = self.number_of_tasks



        current_detail = sch.detailed_representation(current_sol, instance)
        makespan = sch.evaluate_detailed_represenation(current_detail, instance)
        critic, times = sch.path_critic(current_detail, instance, current_sol)
        list_makespan = [makespan]


        listes_taboo = [[[0] * self.number_of_jobs] * self.number_of_jobs] * self.number_of_tasks

        start = time.time()

        it = 0

        while (time.time() < start + timeout and it < maxiter):

            it += 1

            # bloc of critical path
            blocks, list_mac = sch.extractBlocksCriticalPath(critic,  self.machines)



            best_voisin = math.inf


            for i in range(len(blocks)):
                b = blocks[i]
                liste_voisins, new_sols, liste_interdit = self.voisinage_bloc_taboo(b, current_sol, self.machines)


                mac = self.machines[b[0]]

                for v in range(len(liste_voisins)):

                    if listes_taboo[mac][liste_interdit[v][1]][liste_interdit[v][0]] < it:  # tocheck

                        s = new_sols[v]
                        new_detail = sch.detailed_representation(s, instance)
                        new_eval = sch.evaluate_detailed_represenation(new_detail, instance)

                        if new_eval < best_voisin:
                            best_voisin = new_eval
                            best_voisin_sol = s
                            best_voisin_detail = new_detail
                            interdit = liste_interdit[v]
                            mac_best = mac

            listes_taboo[mac_best][interdit[0]][interdit[1]] = it + dureeTaboo

            current_makespan = best_voisin
            current_sol = best_voisin_sol
            current_detail = best_voisin_detail
            critic, times = sch.path_critic(current_detail, instance, current_sol)
            list_makespan.append(current_makespan)

            if current_makespan < makespan:
                makespan = current_makespan



        return makespan




