import json
import logging
import time
from collections import OrderedDict
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np
import pandas
from icecream import ic


def save_to_json_file(data, dest_file):
    with open(dest_file, "w") as a_file:
        json.dump(data, a_file)


def plot_data(xdata, ydata, title, xlabel, ylabel, fig_num):
    plt.figure(fig_num, figsize=(20, 10))
    """x_data = [i for i in range(len(xdata))]
    plt.xticks(x_data, list(xdata))"""
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.hist(ydata)


def save_result_figs(makespans, best_known_value, instance_name, dest_folder ="" ,show=False):
    fig, ax = plt.subplots(figsize=(8, 10))
    N = len(makespans.keys())
    best_known_list = [best_known_value]*N
    makespans = OrderedDict(sorted(makespans.items(), key=itemgetter(1)))
    all_makespans = [value[0] for value in makespans.values()] if isinstance(list(makespans.values())[0], list) \
        else [value for value in makespans.values()]

    ecart = [round(100 * (val - best_known_value) / best_known_value, 1) for val in all_makespans]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    p1 = ax.bar(ind, best_known_list, width, label='best known makespan')
    p2 = ax.bar(ind, np.array(all_makespans)-np.array(best_known_list), width, color='darkred',
                bottom=best_known_list, label='Actual makespan difference')

    ax.bar_label(p2, labels=[f"{e}%" for e in ecart],
                 padding=8, color='b', fontsize=18)

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_ylabel('Makespans')
    ax.set_title(instance_name+' Makespan for each criteria ')
    ax.set_xticks(ind)
    ax.set_xticklabels(makespans.keys())
    ax.legend()

    # Label with label_type 'center' instead of the default 'edge'
    ax.bar_label(p1, label_type='center')
    ax.bar_label(p2, label_type='center')
    plt.savefig(dest_folder+"/"+instance_name+"_results.png")
    if show:
        plt.show()


def read_json_file(file_path):
    data = dict()
    try:
        with open(file_path, 'r') as tw_file:
            data = json.load(tw_file)
    except FileNotFoundError:
        data = None
    finally:
        return data


if __name__ == '__main__':
    FIG_NUM = 0
    bestKnown = {"aaa1": 11,
                 "ft06": 55,
                 "ft10": 930,
                 "ft20": 1165,
                 "la01": 666,
                 "la02": 655,
                 }
    complete_results = read_json_file("tests/complete_results.json")
    heuristics_comparison_dict = dict() # compare Greedy, Descent and Taboo for a given instance and a given criteria

    if True:
        for inst, solved_results in complete_results.items():
            for heuristic, makespans in solved_results.items():
                save_result_figs(makespans, bestKnown[inst], dest_folder="complete_results/heuristic_results",
                                 instance_name=inst + "_" + heuristic)

    for inst, solved_results in complete_results.items():

        heuristics_comparison_dict[inst] = dict()
        makespans_criteria_and_value = solved_results.values()
        heuristics = list(solved_results.keys())
        criterias = solved_results[heuristics[0]].keys()
        makespans = dict()
        for criteria in criterias:
            makespans = dict()
            for heuristic in heuristics:
                makespans[heuristic] = solved_results[heuristic][criteria]
            heuristics_comparison_dict[inst][criteria] = makespans
            ic(makespans)
            save_result_figs(makespans, bestKnown[inst],dest_folder="complete_results/heuristics_comparison",
                             instance_name= inst + "_" + criteria)
    save_to_json_file(data=heuristics_comparison_dict, dest_file="tests/heuristic_comparison_results.json")


