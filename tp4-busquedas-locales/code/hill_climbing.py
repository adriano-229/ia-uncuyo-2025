import random, time
from typing import List, Optional, Dict, Any
from utils import objective_h, random_board

def hill_climbing(n: int,
                  initial_board: Optional[List[int]] = None,
                  max_states: int = 10000,
                  seed: Optional[int] = None,
                  return_history: bool = False) -> Dict[str, Any]:
    if seed is not None:
        random.seed(seed)
    board = initial_board.copy() if initial_board else random_board(n)

    start_time = time.time()
    states = 0
    current = board[:]
    current_h = objective_h(current); states += 1
    best_board, best_h = current[:], current_h
    history = [current_h] if return_history else None

    while states < max_states and current_h > 0:
        neighbors = []
        for col in range(n):
            orig_row = current[col]
            for row in range(n):
                if row == orig_row:
                    continue
                neighbor = current[:]
                neighbor[col] = row
                h = objective_h(neighbor); states += 1
                neighbors.append((h, neighbor))
                if h < best_h:
                    best_board, best_h = neighbor[:], h
        if not neighbors:
            break
        min_h = min(neighbors, key=lambda x: x[0])[0]
        best_neighbors = [nb for (h, nb) in neighbors if h == min_h]
        chosen = random.choice(best_neighbors)
        if min_h < current_h:
            current, current_h = chosen[:], min_h
            if return_history: history.append(current_h)
        else:
            break
    elapsed = time.time() - start_time
    out = {"solution": best_board, "H": best_h, "states": states, "time": elapsed}
    if return_history: out["history"] = history
    return out
