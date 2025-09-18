import random
import time
from typing import List, Optional, Dict, Any, Tuple

import numpy as np

from utils import objective_h, permutation_random_board


def ga_fitness(ind: List[int]) -> int:
    return objective_h(ind)


def tournament_selection(pop: List[List[int]], k: int) -> List[int]:
    best = None
    for _ in range(k):
        cand = random.choice(pop)
        if best is None or ga_fitness(cand) < ga_fitness(best):
            best = cand
    return best[:]


def pmx_crossover(p1: List[int], p2: List[int]) -> Tuple[List[int], List[int]]:
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))

    def pmx(c1, c2):
        child = [-1] * n
        for i in range(a, b + 1): child[i] = c1[i]
        for i in range(a, b + 1):
            if c2[i] not in child:
                pos, val = i, c2[i]
                while True:
                    conflict = c1[pos]
                    pos = c2.index(conflict)
                    if child[pos] == -1:
                        child[pos] = val;
                        break
        for i in range(n):
            if child[i] == -1: child[i] = c2[i]
        return child

    return pmx(p1, p2), pmx(p2, p1)


def swap_mutation(ind: List[int], rate: float) -> List[int]:
    ind = ind[:]
    if random.random() < rate:
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
    return ind


def genetic_algorithm(n: int,
                      pop_size: int = 100,
                      generations: int = 200,
                      tournament_k: int = 3,
                      crossover_rate: float = 0.9,
                      mutation_rate: float = 0.2,
                      elitism: int = 2,
                      seed: Optional[int] = None,
                      max_states: int = 10000,
                      return_history: bool = False) -> Dict[str, Any]:
    if seed is not None: random.seed(seed)
    start_time = time.time()
    states = 0
    pop = [permutation_random_board(n) for _ in range(pop_size)]
    fitness = [ga_fitness(ind) for ind in pop];
    states += len(pop)
    best_idx = int(np.argmin(fitness))
    best_ind, best_h = pop[best_idx][:], fitness[best_idx]
    history = [best_h] if return_history else None

    gen = 0
    while gen < generations and states < max_states and best_h > 0:
        new_pop = []
        sorted_idx = sorted(range(len(pop)), key=lambda i: fitness[i])
        for i in range(min(elitism, pop_size)):
            new_pop.append(pop[sorted_idx[i]][:])
        while len(new_pop) < pop_size and states < max_states:
            p1, p2 = tournament_selection(pop, tournament_k), tournament_selection(pop, tournament_k)
            if random.random() < crossover_rate:
                c1, c2 = pmx_crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]
            new_pop.append(swap_mutation(c1, mutation_rate))
            if len(new_pop) < pop_size: new_pop.append(swap_mutation(c2, mutation_rate))
        pop = new_pop
        fitness = [ga_fitness(ind) for ind in pop];
        states += len(pop)
        cur_best = int(np.argmin(fitness))
        if fitness[cur_best] < best_h:
            best_h, best_ind = fitness[cur_best], pop[cur_best][:]
        if return_history: history.append(best_h)
        gen += 1

    elapsed = time.time() - start_time
    out = {"solution": best_ind, "H": best_h, "states": states, "time": elapsed}
    if return_history: out["history"] = history
    return out
