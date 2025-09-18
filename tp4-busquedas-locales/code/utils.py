import random
from typing import List, Optional


def objective_h(board: List[int]) -> int:
    """Count number of attacking queen pairs (H)."""
    n = len(board)
    h = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                h += 1
    return h


def random_board(n: int, seed: Optional[int] = None) -> List[int]:
    if seed is not None:
        random.seed(seed)
    return [random.randrange(n) for _ in range(n)]


def permutation_random_board(n: int, seed: Optional[int] = None) -> List[int]:
    """For GA: permutation representation, no row conflicts."""
    if seed is not None:
        random.seed(seed)
    p = list(range(n))
    random.shuffle(p)
    return p
