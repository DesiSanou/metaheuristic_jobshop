import numpy as np
import time
from docplex.cp.model import CpoModel
from docplex.cp.parameters import CpoParameters
import os


def resolve_exact(filename):
    searchtype = "Restart"
    interference = "Low"
    timelimit = 500000
    params = CpoParameters(TimeLimit=10, LogPeriod=100000)

    sol, time_cplex = cplex_solve_instance2(filename, 4, searchtype, interference, timelimit)

    return sol.get_value("makespan"), time_cplex


def cplex_makespan_model(n: int, m: int, durations, machines) -> CpoModel:
    # n number of jobs, m machines
    # 1 line for un job with tasks on m machines

    naive = np.sum(durations)

    mdl = CpoModel()

    # Une variable est l'intervalle de durée pour une tache
    x = [[mdl.interval_var(size=durations[i, j], name="O{}-{}".format(i, j)) for j in range(m)] for i in range(n)]

    # contrainte end max d'une tache calculée avant
    for i in range(n):
        for j in range(m):
            mdl.add(mdl.end_of(x[i][j]) <= naive)

    # precedence
    for i in range(n):  # for each job
        for j in range(m - 1):  # taches ordonnées
            mdl.add(mdl.end_before_start(x[i][j], x[i][j + 1]))

    # une machine ne peut faire qu'une tache à la fois
    listtaches = [[] for k in range(m)]
    for i in range(n):
        for j in range(m):
            listtaches[machines[i, j]].append(x[i][j])

    for k in range(m):
        mdl.add(mdl.no_overlap(listtaches[k]))

    makespan = mdl.integer_var(0, naive, name="makespan")
    # le makespan est le max des tps pour chaque job
    mdl.add(makespan == mdl.max([mdl.end_of(x[i][m - 1]) for i in range(n)]))

    mdl.add(mdl.minimize(makespan))

    return mdl, x


def cplex_solve_instance2(filename, start, searchtype, interference, timelimit):
    f = open(filename, "r")
    content = f.read()
    f.close()
    # print(content)
    lines = content.split("\n")

    array = []

    for i in lines[start:]:
        numbers = i.split(" ")
        while numbers.count('') > 0:
            numbers.remove('')
        for j in range(len(numbers)):
            numbers[j] = int(numbers[j])
        # print(numbers)
        if numbers != []:
            array.append(numbers)

    n = array[0][0]  # number of jobs
    m = array[0][1]  # number of machines

    machines = np.matrix(array[1:])[:, ::2]

    durations = np.matrix(array[1:])[:, 1::2]

    mdl, x = cplex_makespan_model(n, m, durations, machines)
    start = time.time()
    sol = mdl.start_search(TimeLimit=timelimit, SearchType=searchtype, DefaultInferenceLevel=interference).solve()
    end = time.time()
    # sol.print_solution()
    # display_sol (sol)

    return sol, end - start




    """# test PPC solver (CPLEX)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = ROOT_DIR + '/../instances/ft10'

    searchtype = "Restart"
    interference = "Low"
    timelimit = 500000
    params = CpoParameters(TimeLimit=10, LogPeriod=100000)

    sol, time_cplex = cplex_solve_instance2(filename, 4, searchtype, interference, timelimit)

    print("instance:", filename)
    print("time: ", time_cplex)
    print("makespan: ", sol.get_value("makespan"))"""