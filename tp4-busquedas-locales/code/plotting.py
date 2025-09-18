import matplotlib.pyplot as plt
import os

from genetic_algorithm import genetic_algorithm
from hill_climbing import hill_climbing
from random_search import random_search
from simulated_annealing import simulated_annealing


def plot_boxplots(df, sizes, images_dir):
    for size in sizes:
        subset = df[df['size'] == size]
        if subset.empty: continue
        plt.figure(dpi=200)
        subset.boxplot(column='H', by='algorithm_name')
        plt.title(f"H distribution (N={size})")
        plt.suptitle("")
        plt.ylabel("H")
        path = os.path.join(images_dir, f"boxplot_H_N{size}.png")
        plt.savefig(path)
        plt.close()


def plot_example_histories(size, seed, images_dir):
    results = {
        "HC": hill_climbing(size, seed=seed, return_history=True),
        "SA": simulated_annealing(size, seed=seed, return_history=True),
        "GA": genetic_algorithm(size, seed=seed, return_history=True),
        "random": random_search(size, seed=seed, return_history=True),
    }
    plt.figure(dpi=200)
    for algo, res in results.items():
        if "history" in res: plt.plot(res["history"], label=algo)
    plt.legend()
    plt.xscale("log")
    plt.xlabel("log Step")
    plt.ylabel("H")
    path = os.path.join(images_dir, f"H_history_N{size}_seed{seed}.png")
    plt.savefig(path)
    plt.close()
