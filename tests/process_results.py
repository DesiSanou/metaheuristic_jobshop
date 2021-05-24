import json
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas


def plot_data(xdata, ydata, title, xlabel, ylabel, fig_num):
    plt.figure(fig_num, figsize=(20, 10))
    """x_data = [i for i in range(len(xdata))]
    plt.xticks(x_data, list(xdata))"""
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.hist(ydata)


def plot_result(makespans, best_known_value, instance):
    fig, ax = plt.subplots(figsize=(20,10))
    N = len(makespans.keys())
    best_known_list = [best_known_value]*N

    all_makespans = [value[0] for value in makespans.values()]
    ecart = [round(100 * (val - best_known_value) / best_known_value, 1) for val in all_makespans]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    p1 = ax.bar(ind, best_known_list, width, label='best known makespan')
    p2 = ax.bar(ind, all_makespans, width, color='darkred',
                bottom=best_known_list, label='Actual makespan')

    ax.bar_label(p2, labels=[f"{e}%" for e in ecart],
                 padding=8, color='b', fontsize=18)

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_ylabel('Makespans')
    ax.set_title(instance+' Makespan for each criteria ')
    ax.set_xticks(ind)
    ax.set_xticklabels(makespans.keys())
    ax.legend()

    # Label with label_type 'center' instead of the default 'edge'
    ax.bar_label(p1, label_type='center')
    ax.bar_label(p2, label_type='center')
    plt.savefig(instance+"_results.png")
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
    global_results = read_json_file("results.json")
    for inst, makespans in global_results.items():
        plot_result(makespans, bestKnown[inst], inst)

    if False:
         for inst, makespans in global_results.items():
            title = inst+" results for each criteria"
            # plt.hist("best", bestKnown[inst])
            y_data = [value[0] for value in makespans.values()]
            df = pandas.DataFrame.from_dict(makespans, orient='index')
            df.index.name = "Makespan "+ inst
            ax = df.plot(kind='bar')
            ax.s
            ax.figure.savefig(inst+"_results.png")

            if False:
                x_data = [i+1 for i in range(len(makespans.keys()))]
                plot_data(xdata=makespans.keys(), ydata=y_data, xlabel="solver criteria", ylabel="makespan", title=title, fig_num=FIG_NUM)
                plt.xticks(x_data, list(makespans.keys()))
                # plt.plot(x_data, [bestKnown[inst]] * len(x_data))
                plt.savefig(inst+"_result.png")
            plt.show()
            FIG_NUM += 1
            break