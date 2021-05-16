import logging
import time
from tabulate import tabulate
import argparse

from BasicSolver import BasicSolver
from solvers.greedy_solver import GreedySolver
from Instance import Instance
from ResourceOrder import ResourceOrder
from JobNumbers import JobNumbers

bestKnown = {"la01": 666,
             "la02": 655,
             "aaa1": 11,
             "ft06": 55,
             "ft10": 930,
             "ft20": 1165
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
        else:
            logging.error("%s not Implemented", criteria)
            exit()
        logging.debug(f"job_list:{job_list}")
        logging.debug(f"task_by_machines: {task_by_machines}")
        resource_order = ResourceOrder(instance=instance,
                                       task_by_machines=task_by_machines)
        job_numbers = JobNumbers(instance, job_list)
        logging.debug("resource_order: %s", str(resource_order))
        schedule_repr = job_numbers.toSchedule()
        response = format_result(schedule_repr, instance_name=inst, start_time=start)
        results.append([inst, response[0], response[1], response[2], response[3], response[4]])
    print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))


if __name__ == '__main__':

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--instances', default=None, type=str)
    args = parser.parse_args()
    instances = args.instances.split('-')
    results = []
    criterias = ["spt", "lrpt", "est_spt", "est_lrpt"]
    for criteria in criterias:
        solve_problem(instances, criteria=criteria)

    if True:
        print('\n')
        print('Basic Result : \n')

        for inst in instances:
            try:
                instance = Instance.fromFile('tests/instances/' + inst)
            except(FileNotFoundError, IOError):
                print('File not found')
            start = time.time()
            result, sol_basic = BasicSolver().solve(instance=instance, deadline=None)
            response = format_result(sol_basic.toSchedule(), inst, start)

            results.append([inst, response[0], response[1], response[2], response[3], response[4]])
        print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))






