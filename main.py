import logging
import json
from Instance import Instance
from tabulate import tabulate
import solvers.greedy_solver as gs
import solvers.descend_solver as ds
import solvers.taboo_solver as tb
import solvers.exact_solver as es

bestKnown = { "aaa1": 11,
              "ft06": 55,
              "ft10": 930,
              "ft20": 1165,
              "la01": 666,
              "la02": 655,
             }

def main():

    
    solve_problem(list(bestKnown.keys()),descend=True, taboo=True)
    #compare_taboo_to_exact(list(bestKnown.keys()), taboo=True, exact=True)


def solve_problem(instances,  method_list=['spt', 'lpt','lrpt', 'est_spt', 'est_lrpt'], descend=False, taboo=False,
                  timeout=60, timeTaboo=10, maxiter=200):
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
        print(tabulate(results, headers=['solver', 'method', 'runtime [s]', 'makespan', 'ecart [%]']))

    dest_file = "results.json"
    with open(dest_file, "w") as a_file:
        json.dump(global_results, a_file)

    return global_results




def compare_taboo_to_exact(instances, method_list=['spt', 'lpt', 'lrpt', 'est_spt', 'est_lrpt'], taboo=True, exact= True, timeout=60,
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

        if exact == True :
            result, runtime = es.resolve_exact('instances/'+inst)
            for i in range(len(method_list)):
                res = result
                results.append(
                    ['Exact', method_list[i], round(runtime, 2), res, round((res / bestKnown[inst] - 1) * 100, 2)])
                global_results[inst]['Exact'][method_list[i]] = res


        print('\n\n  Instances : %s  | Size : %s x %s \n' % (inst, instance.numJobs, instance.numTasks))
        print(tabulate(results, headers=['solver', 'method', 'runtime [s]', 'makespan', 'ecart [%]']))

    dest_file = "results_compare.json"
    with open(dest_file, "w") as a_file:
        json.dump(global_results, a_file)

    return global_results


if __name__ == '__main__':
    main()