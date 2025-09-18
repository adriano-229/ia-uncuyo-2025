import math
import random
import time
from typing import List, Optional, Dict, Any

from utils import objective_h, random_board

SA_MIN_TEMP = 1e-3


def sa_schedule_exponential(t: float, alpha: float) -> float:
    return max(t * alpha, SA_MIN_TEMP)


def sa_schedule_lineal(t: float, alpha: float) -> float:
    return max(t - alpha, SA_MIN_TEMP)


def simulated_annealing(n: int,
                        initial_board: Optional[List[int]] = None,
                        max_states: int = 10000,
                        seed: Optional[int] = None,
                        schedule: str = "exponential",
                        t0: float = 10.0,
                        alpha: float = 0.9,
                        return_history: bool = False) -> Dict[str, Any]:
    if seed is not None:
        random.seed(seed)
    board = initial_board.copy() if initial_board else random_board(n)

    start_time = time.time()
    states = 0
    current = board[:]
    current_h = objective_h(current)
    states += 1
    best_board, best_h = current[:], current_h
    t = t0
    history = [current_h] if return_history else None

    while states < max_states and current_h > 0 and t > SA_MIN_TEMP:
        col = random.randrange(n)
        new_row = random.randrange(n - 1)
        if new_row >= current[col]: new_row += 1
        neighbor = current[:]
        neighbor[col] = new_row
        h_neighbor = objective_h(neighbor)
        states += 1

        delta = h_neighbor - current_h
        if delta <= 0 or random.random() < math.exp(-delta / t):
            current, current_h = neighbor, h_neighbor
            if current_h < best_h:
                best_board, best_h = current[:], current_h
            if return_history: history.append(current_h)

        if schedule == "exponential":
            t = sa_schedule_exponential(t, alpha)
        else:
            t = sa_schedule_lineal(t, alpha)  # fallback
        print(t)

    elapsed = time.time() - start_time
    out = {"solution": best_board, "H": best_h, "states": states, "time": elapsed}
    if return_history: out["history"] = history
    return out
