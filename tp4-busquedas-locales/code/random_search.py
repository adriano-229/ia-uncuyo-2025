import random
import time
from typing import Optional, Dict, Any

from utils import objective_h, random_board


def random_search(n: int,
                  max_states: int = 10000,
                  seed: Optional[int] = None,
                  return_history: bool = False) -> Dict[str, Any]:
    if seed is not None: random.seed(seed)
    start_time = time.time();
    states = 0
    best_board, best_h = None, float('inf')
    history = [] if return_history else None
    while states < max_states and best_h > 0:
        b = random_board(n)
        h = objective_h(b);
        states += 1
        if h < best_h: best_board, best_h = b[:], h
        if return_history: history.append(best_h)
    elapsed = time.time() - start_time
    out = {"solution": best_board, "H": int(best_h), "states": states, "time": elapsed}
    if return_history: out["history"] = history
    return out
