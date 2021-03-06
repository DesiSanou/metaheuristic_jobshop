import logging
import time
from tabulate import tabulate
import argparse
import json
from BasicSolver import BasicSolver
from solvers.greedy_solver import GreedySolver
from Instance import Instance
from ResourceOrder import ResourceOrder
from JobNumbers import JobNumbers
from process_results import read_json_file, save_result_figs, save_to_json_file

bestKnown = { "aaa1": 11,
              "ft06": 55,
              "ft10": 930,
              "ft20": 1165,
              "la01": 666,
              "la02": 655,
             }


def format_result(schedule_repr, instance_name, start_time):
    makespan = schedule_repr.makespan()
    best = bestKnown[instance_name]
    ecart = round(100 * (makespan - best) / best, 1)
    size = str(schedule_repr.pb.numJobs) + "x" + str(schedule_repr.pb.numTasks)
    runtime = time.time() - start_time

    return size, best, round(runtime, 2), makespan, ecart


def solve_problem(instances, criteria="spt"):
    results = list()

    print('\n\nSolver: Greedy | Criteria: %s \n'% criteria.upper())

    for inst in instances:
        logging.debug(inst)
        try:
            instance = Instance.fromFile('tests/instances/' + inst)
        except(FileNotFoundError, IOError):
            logging.error('File not found')
            exit()
        start = time.time()
        # inst_path = 'tests/instances/' + inst
        greedy_solver = GreedySolver(instance)
        if criteria == "spt":
            job_list, task_by_machines = greedy_solver.run_spt()
        elif criteria == "lrpt":
            job_list, task_by_machines = greedy_solver.run_lrpt()
        elif criteria == "est_spt":
            job_list, task_by_machines = greedy_solver.run_est_spt()
        elif criteria == "est_lrpt":
            job_list, task_by_machines = greedy_solver.run_est_lrpt()
        elif criteria == "lpt":
            job_list, task_by_machines = greedy_solver.run_lpt()
        else:
            logging.error("%s not Implemented", criteria)
            exit()
        logging.debug(f"job_list:{job_list}")
        logging.debug(f"task_by_machines: {task_by_machines}")
        resource_order = ResourceOrder(instance=instance,
                                       task_by_machines=task_by_machines)

        new_instance = Instance(numJobs=instance.numJobs, numTasks=instance.numTasks,
                                durations=instance.durations, machines=instance.machines)
        job_numbers = JobNumbers(new_instance, job_list)
        logging.debug("resource_order: %s", str(resource_order))
        schedule_repr = job_numbers.toSchedule()
        response = format_result(schedule_repr, instance_name=inst, start_time=start)
        global_results[inst][criteria].append(response[3])
        results.append([inst, response[0], response[1], response[2], response[3], response[4]])
    print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))


if __name__ == '__main__':

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
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

    dest_file = "tests/results_"+str(time.strftime("%Y_%m_%d_%Hh_%M"))+".json"
    args = parser.parse_args()
    if args.instances == "all":
        instances = bestKnown.keys()
    else:
        instances = args.instances.split('-')
    results = []
    criterias = ["spt", "lrpt", "est_spt", "est_lrpt", "lpt"]

    global_results = dict()
    for inst in instances:
        global_results[inst] = dict()
        for criteria in criterias:
            global_results[inst][criteria] = list()

    print("# metaheuristic_jobshop")
    print("<pre>")
    for criteria in criterias:
        solve_problem(instances, criteria=criteria)

    if True:
        print('\n')
        print('Basic Result : \n')

        for inst in instances:
            global_results[inst]["basic"] = list()
            try:
                instance = Instance.fromFile('tests/instances/' + inst)
            except(FileNotFoundError, IOError):
                print('File not found')
            start = time.time()
            result, sol_basic = BasicSolver().solve(instance=instance, deadline=None)
            response = format_result(sol_basic.toSchedule(), inst, start)
            global_results[inst]["basic"].append(response[3])
            results.append([inst, response[0], response[1], response[2], response[3], response[4]])
        print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))

        print("</pre>")
    if args.save_result:

        with open(dest_file, "w") as a_file:
            json.dump(global_results, a_file)

    if args.create_figs:
        global_results = read_json_file(dest_file)
        for inst, makespans in global_results.items():
            save_result_figs(makespans, bestKnown[inst], inst, show=args.show_figs)




