import argparse
import logging
import json
import time
from collections import OrderedDict
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np


from Instance import Instance
from tabulate import tabulate
import solvers.greedy_solver as gs
import solvers.descend_solver as ds
import solvers.taboo_solver as tb
import plot_figure

bestKnown = { "aaa1": 11,
              "ft06": 55,
              "ft10": 930,
              "ft20": 1165,
              "la01": 666,
              "la02": 655,
             }



def solve_problem(instances,  method_list=['spt', 'lpt','lrpt', 'est_spt', 'est_lrpt'], descend=False, taboo=False,
                  save_result= True, create_figs=True, show_figs = True, timeout=60, timeTaboo=10, maxiter=200):
    global_results = dict()



    solver_list = ['Gloutone', 'Descend', 'Taboo']
    for inst in instances:
        global_results[inst] = dict()
        for solver in solver_list:
            global_results[inst][solver] = dict()
            for method in method_list:
                global_results[inst][solver][method] = list()

    for inst in instances:
        results = list()
        logging.debug(inst)
        try:
            instance = Instance.fromFile('instances/' + inst)
        except(FileNotFoundError, IOError):
            logging.error('File not found')
            exit()

        greedy_solver = gs.GreedySolver(instance)
        result = greedy_solver.solve_gredy(method_list)


        for i in range(len(method_list)):
            res = result[i]
            results.append(['Gloutone', method_list[i], round(res[0],2), res[1], round((res[1]/bestKnown[inst] - 1)*100,2)])
            global_results[inst]['Gloutone'][method_list[i]] = res[1]
        if descend == True:

            descend_solver = ds.DescendSolver(instance)

            result = descend_solver.solve_descend(method_list, timeout)
            for i in range(len(method_list)):
                res = result[i]
                results.append(['Descend', method_list[i], round(res[0],2), res[1], round((res[1]/bestKnown[inst] - 1)*100,2)])
                global_results[inst]['Descend'][method_list[i]] = res[1]

        if taboo == True:

            taboo_solver = tb.TabooSolver(instance)

            result = taboo_solver.solve_taboo(method_list, timeout,timeTaboo, maxiter)
            for i in range(len(method_list)):
                res = result[i]
                results.append(['Taboo', method_list[i], round(res[0],2), res[1], round((res[1]/bestKnown[inst] - 1)*100,2)])
                global_results[inst]['Taboo'][method_list[i]] = res[1]

        print('\n\n  Instances : %s  | Size : %s x %s \n' % (inst,instance.numJobs, instance.numTasks ))
        print(tabulate(results, headers=['solver', 'criteria', 'runtime [s]', 'makespan', 'ecart [%]']))

    if save_result==True:
        dest_file = 'results/result_' + str(time.strftime('%Y_%m_%d_%Hh_%M')) + '.json'
        with open(dest_file, "w") as a_file:
            json.dump(global_results, a_file)

    if create_figs==True:
        for inst, solved_results in global_results.items():
            for heuristic, makespans in solved_results.items():
                plot_figure.save_result_figs(makespans, bestKnown[inst], instance_name=inst + "_" + heuristic,  show=show_figs,)

    return global_results




def compare_taboo_to_exact(instances, method_list=['spt', 'lpt', 'lrpt', 'est_spt', 'est_lrpt'], taboo=True,
                            create_figs=True, timeout=60,
                           timeTaboo=10, maxiter=200):
    global_results = dict()

    solver_list = [ 'Taboo', 'Exact']
    for inst in instances:
        global_results[inst] = dict()
        for solver in solver_list:
            global_results[inst][solver] = dict()
            for method in method_list:
                global_results[inst][solver][method] = list()

    for inst in instances:
        results = list()
        logging.debug(inst)
        try:
            instance = Instance.fromFile('instances/' + inst)
        except(FileNotFoundError, IOError):
            logging.error('File not found')
            exit()




        if taboo == True:

            taboo_solver = tb.TabooSolver(instance)

            result = taboo_solver.solve_taboo(method_list, timeout, timeTaboo, maxiter)
            for i in range(len(method_list)):
                res = result[i]
                results.append(
                    ['Taboo', method_list[i], round(res[0], 2), res[1], round((res[1] / bestKnown[inst] - 1) * 100, 2)])
                global_results[inst]['Taboo'][method_list[i]] = res[1]


        print('\n\n  Instances : %s  | Size : %s x %s \n' % (inst, instance.numJobs, instance.numTasks))
        print(tabulate(results, headers=['solver', 'criteria', 'runtime [s]', 'makespan', 'ecart [%]']))




    return global_results


if __name__ == '__main__':

    save_result = False
    create_figs = False
    show_figs = False

    parser = argparse.ArgumentParser()
    parser.add_argument('--instances',
                        default=None,
                        type=str)
    parser.add_argument('--save_result',
                        action="store_true")

    parser.add_argument('--create_figs',
                        action="store_true")
    parser.add_argument('--show_figs',
                        action="store_true")

    args = parser.parse_args()
    if args.instances == "all":
        instances = bestKnown.keys()
    else:
        instances = args.instances.split('-')

    if args.save_result:
        save_result = True

    if args.create_figs:
        create_figs = True

    if args.show_figs:
        show_figs = True

    solve_problem(list(instances), descend=True, taboo=True, save_result=save_result, create_figs=create_figs, show_figs=show_figs)