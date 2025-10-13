import pandas as pd

from genetic_algorithm import genetic_algorithm
from hill_climbing import hill_climbing
from random_search import random_search
from simulated_annealing import simulated_annealing


def run_experiments(sizes, algos, n_seeds, max_states, csv_path):
    rows = []
    for size in sizes:
        for algo in algos:
            for seed in range(n_seeds):
                if algo == "HC":
                    res = hill_climbing(size, max_states=max_states, seed=seed)
                elif algo == "SA":
                    res = simulated_annealing(size, max_states=max_states, seed=seed)
                elif algo == "GA":
                    res = genetic_algorithm(size, max_states=max_states, seed=seed)
                elif algo == "random":
                    res = random_search(size, max_states=max_states, seed=seed)
                rows.append({
                    "algorithm_name": algo,
                    "env_n": seed,
                    "size": size,
                    "best_solution": res["solution"],
                    "H": res["H"],
                    "states": res["states"],
                    "time": res["time"]
                })
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    return df


def compute_statistics(df, sizes):
    stats = {}
    for algo in df['algorithm_name'].unique():
        stats[algo] = {}
        df_algo = df[df['algorithm_name'] == algo]
        for size in sizes:
            sub = df_algo[df_algo['size'] == size]
            success = (sub['H'] == 0).sum()
            pct = 100.0 * success / len(sub) if len(sub) > 0 else 0
            stats[algo][size] = {
                "pct_success": pct,
                "H_mean": sub['H'].mean(),
                "H_std": sub['H'].std(),
                "time_mean": sub['time'].mean(),
                "time_std": sub['time'].std(),
                "states_mean": sub['states'].mean(),
                "states_std": sub['states'].std()
            }
    return stats
