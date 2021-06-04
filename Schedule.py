import numpy as np
import pandas as pd
import math
import hashlib

infini = math.inf



def detailed_representation(ressource, instance):
    machines = instance.machines
    durations = instance.durations
    number_of_jobs = instance.numJobs
    number_of_tasks = instance.numTasks

    # initialize state with first state of all tasks
    first_state = 0
    state = [first_state for _ in range(number_of_tasks)]

    # initialize detailled representation
    detailed_resource = [[infini]*number_of_tasks for _ in range(number_of_jobs)]

    detailed_resource_exists = True

    while (max([sum(detailed_resource[i]) for i in range(number_of_jobs)]) >= infini):

        move = 0

        # fillin detailed representation
        for j in range(number_of_tasks):
            for i in range(number_of_jobs):

                # time where task j-1 of job i will be finished
                if detailed_resource[i][j]==infini:
                    if j==0:
                        previous_time = 0
                    if j > 0 :
                        previous_time = detailed_resource[i][j-1] + durations[i,j-1]

                    used_machine = machines[i,j]
                    new_state = state[used_machine]

                    job, num_operation = ressource[used_machine][new_state]

                    if job == i:
                        if new_state == 0:
                            mac_time = 0
                        if new_state != 0:
                            previous_j, previous_task_machine = ressource[used_machine][new_state - 1]
                            mac_time = detailed_resource[previous_j][previous_task_machine] + durations[previous_j, previous_task_machine]

                    if job != i:
                        mac_time = infini

                    start_date = max(mac_time, previous_time)
                    detailed_resource[i][j] = start_date

                    #update state
                    if start_date < infini:
                        state[used_machine] += 1
                        move += 1

        if move == 0:
            break
    return detailed_resource

def evaluate_detailed_represenation(detail, instance):

    durations = instance.durations
    number_of_jobs = instance.numJobs
    number_of_tasks = instance.numTasks

    ends = []
    for i in range(number_of_jobs):
        end = detail[i][number_of_tasks - 1] + durations[i, number_of_tasks - 1]
        ends.append(end)

    return max(ends)


def critical_path(instance, start_time, makespan, ressource):
    machines = instance.machines
    durations = instance.durations
    number_of_jobs = instance.numJobs
    number_of_tasks = instance.numTasks

    critical_tasks = []
    end_list = []
    durations = durations.tolist()

    for i in range(number_of_jobs):
        for j in range(number_of_tasks):
            end_list.append(
                ["Job " + str(i) + " /op " + str(j), i, j, durations[i][j], start_time[i][j],
                 start_time[i][j]+ durations[i][j]])

    endTime = int(makespan)

    path = []
    path.append(in_list(endTime, end_list))

    while endTime != 0:
        current_task = path[-1]

        latest_predecessor = []

        # get previous task in the job
        if current_task[2] > 0:
            task_pred_on_job = get_pred_task(current_task[1], current_task[2] - 1, end_list)

            # if it was the delaying task, save it to predecessor
            if task_pred_on_job[5] == current_task[4]:
                latest_predecessor = task_pred_on_job

        # if there is not predecessor currently, get previous task of the machine
        if not latest_predecessor:
            machine = get_ressource(machines, current_task[1], current_task[2])
            index_previous_task = ressource[machine].index((current_task[1], current_task[2])) - 1
            pred_task_machine = get_pred_task(ressource[machine][index_previous_task][0],
                                              ressource[machine][index_previous_task][1], end_list)

            # if it was the delaying task, save it to predecessor
            if pred_task_machine[5] == current_task[4]:
                latest_predecessor = pred_task_machine

        path.append(latest_predecessor)

        if latest_predecessor[4] == 0:
            break

        endTime = latest_predecessor[5]

    path.reverse()

    return get_tuples(path)

def in_list(c, classes):
    for i, sublist in enumerate(classes):
        if c == sublist[5]:
            return sublist
    return -1

def get_pred_task(c, d, classes):
    for i, sublist in enumerate(classes):
        if c == sublist[1] and d == sublist[2]:
            return sublist
    return -1

def get_tuples(path):
    blocks = []
    for i in path:
        blocks.append((i[1], i[2]))
    return blocks

def get_ressource(machines, job, operation):
    """
     :param machines: tableau comportant la liste des machines
     :param job: job associé à une tâches
     :param operation: numéro d'opération associé à une tâche
     :return: ressource associée à la tache passée en paramètre à l'aide de "job" et "opération"
     """
    return machines[job, operation]

def duplicate_ressource(resource):
    new_resource = []
    for r in resource:
        r_new = []
        for t in r:
            r_new.append(t)
        new_resource.append(r_new)

    return new_resource

def choose_best_neighbor(all_neighbors,number_of_jobs, number_of_tasks,  durations, machines):
    """
    :param all_neighbors: liste de tous les voisins
    :param n:
    :param m:
    :param durations:
    :param machines:
    :return: meilleur voisin : makespan, solution, détaille des horaires de la solution
    """
    best_neighbor = math.inf
    for solution in all_neighbors:
        new_detail = detailed_representation(solution, number_of_jobs, number_of_tasks,  durations, machines)
        new_eval = evaluate_detailed_represenation(new_detail, number_of_jobs, number_of_tasks,  durations)  # memo makespan sol
        if new_eval < best_neighbor:
            best_neighbor = new_eval
            best_neighbor_solution = solution
            best_neighbor_detail = new_detail
    return best_neighbor, best_neighbor_solution, best_neighbor_detail

def extractBlocksCriticalPath(critiques, machines):
    blocks = []

    list_mac = []  # debug

    bloc = []

    prec_mac = machines[critiques[0]]  # initialisation
    bloc.append(critiques[0])

    list_mac.append(machines[critiques[0]])

    for i in range(1, len(critiques)):
        j, o = critiques[i]
        if prec_mac == machines[j, o]:
            bloc.append(critiques[i])
        else:
            blocks.append(bloc)  # on ajoute l'ancien bloc
            bloc = [critiques[i]]  # on en commence un nouveau

        prec_mac = machines[j, o]  # mise à jour machine prcedente
        list_mac.append(machines[critiques[i]])

    blocks.append(bloc)  # on ajoute le dernier bloc

    blocks = [b for b in blocks if len(b) > 1]  # on enleve les blocs de taille <2

    return blocks, list_mac

def path_critic(detail, instance, ressource):
    machines = instance.machines
    durations = instance.durations
    number_of_jobs = instance.numJobs
    number_of_tasks = instance.numTasks
    # Calculer le chemin critique et retourner la liste de tâches qui le compose
    makespan = evaluate_detailed_represenation(detail, instance)

    critiques = []  # contient des taches (j,o)
    times = []  # contient les endtimes le long du chemin critique

    longest_time = makespan
    times.append(makespan)

    # initialisation, on commence par la fin
    for i in range(number_of_jobs):
        if detail[i][number_of_tasks - 1] + durations[i, number_of_tasks - 1] == longest_time:
            # tache i, m-1 est sur chemin_critique
            tache = (i, number_of_tasks - 1)
            critiques.append(tache)
            longest_time -= durations[i, number_of_tasks - 1]
            times.insert(0, longest_time)
            break  # on ajoute qu'un élément si égalité

    while longest_time != 0:

        # print(critiques) #debug
        last = critiques[0]

        j, o = last
        mac = machines[j, o]

        # pred_job = [] #tache precedente du job et precedente de la machine

        # tache precedente du job
        if detail[j][o - 1] + durations[j, o - 1] == detail[j][o]:
            tache = (j, o - 1)  # debug
            critiques.insert(0, tache)
            longest_time -= durations[j, o - 1]
            times.insert(0, longest_time)
            # print('job prec: ', critiques)

        else:
            # tache precedente de la machine
            mac_index = ressource[mac].index(last)
            jm, om = ressource[mac][mac_index - 1]  # tache recedente machine

            if detail[jm][om] + durations[jm, om] == detail[j][o]:
                critiques.insert(0, (jm, om))
                longest_time -= durations[jm, om]
                times.insert(0, longest_time)
                # print('machine prec: ', critiques)

            else:
                print("no tache correspondante, probleme?")

    # Methode PERT? TODO

    return critiques, times

def validate_detail(detail, instance):
    machines = instance.machines
    durations = instance.durations
    number_of_jobs = instance.numJobs
    number_of_tasks = instance.numTasks

    val = True  # initialisation à valider = True, si une contrainte est violée, on passe à False et on arrete

    # precedence
    for i in range(number_of_jobs):
        for j in range(number_of_tasks - 1):
            if detail[i][j + 1] < detail[i][j] + durations[i, j]:
                print("not correct precedence for ligne ", i, 'colonne: ', j)
                val = False
                break

    # index ne peut traiter qu'une tache à la fois
    # on verifie qu'un index ne fait qu'une tache à la fois

    for k in range(number_of_tasks):
        # retrouver toutes les taches de la index et stocker les startdates
        list_start = []
        list_start_durations = []
        for i in range(number_of_jobs):
            j = machines[[i], :].tolist()[0].index(k)  # j contient le numéro d'op
            start = detail[i][j]
            list_start.append((start, j))
        # les ordonner par startdate
        list_start = sorted(list_start, key=lambda tache: tache[0])
        for s, j in list_start:
            end = s + durations[i, j]
            list_start_durations.append((start, end))

        # verifier que startdate+duration<nextstartdate
        for i in range(len(list_start_durations) - 1):
            s = list_start_durations[i + 1]  # date de début de la prochaine tache
            e = list_start_durations[i]
            if s < e:
                print("not correct, plus d'une tache à la fois pour index ", k, 'start: ', s)
                val = False
                break

    return val



