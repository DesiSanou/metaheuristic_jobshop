from collections import OrderedDict
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np

def save_result_figs(makespans, best_known_value, instance_name, dest_folder ="figures" ,show=False):
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

    ax.bar_label(p2, labels=[f"{e}%" for e in ecart], padding=8, color='b', fontsize=18)

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