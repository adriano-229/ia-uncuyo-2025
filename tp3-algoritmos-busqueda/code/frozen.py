import gymnasium as gym
import heapq
import plot
from collections import deque

from gymnasium import wrappers


def run_random_episode(env, env_n=0, scenario=1):
    start_time = time.time()
    state, _ = env.reset()
    explored = 0
    path, cost = [], 0

    done = truncated = False
    while not (done or truncated):
        action = env.action_space.sample()
        next_state, reward, done, truncated, _ = env.step(action)

        # cost model
        if scenario == 1:
            step_cost = 1
        else:
            step_cost = 1 if action in (0, 2) else 10

        path.append(action)
        cost += step_cost
        explored += 1

        if reward > 0:
            elapsed = time.time() - start_time
            return {
                "algorithm_name": "Random",
                "env_n": env_n,
                "states_n": explored,
                "actions_count": len(path),
                "actions_cost": cost,
                "time": elapsed,
                "solution_found": True,
                "path": path
            }

    elapsed = time.time() - start_time
    return {
        "algorithm_name": "Random",
        "env_n": env_n,
        "states_n": explored,
        "actions_count": len(path),
        "actions_cost": cost,
        "time": elapsed,
        "solution_found": False,
        "path": path
    }


def run_bfs_episode(env, env_n=0, scenario=1):
    start_time = time.time()
    state, _ = env.reset()
    explored = 0
    visited = set()

    queue = deque([(state, [], 0)])  # (state, path, cost)

    while queue:
        current_state, path, cost = queue.popleft()
        if current_state in visited:
            continue
        visited.add(current_state)
        explored += 1

        for action in range(env.action_space.n):
            prob, next_state, reward, done = env.unwrapped.P[current_state][action][0]
            if next_state == current_state:
                continue

            step_cost = 1 if scenario == 1 else (1 if action in (0, 2) else 10)
            new_path = path + [action]
            new_cost = cost + step_cost

            if reward > 0:
                elapsed = time.time() - start_time
                return {
                    "algorithm_name": "BFS",
                    "env_n": env_n,
                    "states_n": explored,
                    "actions_count": len(new_path),
                    "actions_cost": new_cost,
                    "time": elapsed,
                    "solution_found": True,
                    "path": new_path
                }
            queue.append((next_state, new_path, new_cost))

    elapsed = time.time() - start_time
    return {
        "algorithm_name": "BFS",
        "env_n": env_n,
        "states_n": explored,
        "actions_count": 0,
        "actions_cost": 0,
        "time": elapsed,
        "solution_found": False,
        "path": []
    }


def run_dfs_episode(env, env_n=0, scenario=1, limit=None):
    start_time = time.time()
    state, _ = env.reset()
    explored = 0
    visited = set()

    stack = [(state, [], 0, 0)]  # (state, path, cost, depth)

    while stack:
        current_state, path, cost, depth = stack.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        explored += 1

        if limit is not None and depth > limit:
            continue

        for action in range(env.action_space.n):
            prob, next_state, reward, done = env.unwrapped.P[current_state][action][0]
            if next_state == current_state:
                continue

            step_cost = 1 if scenario == 1 else (1 if action in (0, 2) else 10)
            new_path = path + [action]
            new_cost = cost + step_cost

            if reward > 0:
                elapsed = time.time() - start_time
                return {
                    "algorithm_name": "DFS" if limit is None else f"DLS-{limit}",
                    "env_n": env_n,
                    "states_n": explored,
                    "actions_count": len(new_path),
                    "actions_cost": new_cost,
                    "time": elapsed,
                    "solution_found": True,
                    "path": new_path
                }

            stack.append((next_state, new_path, new_cost, depth + 1))

    elapsed = time.time() - start_time
    return {
        "algorithm_name": "DFS" if limit is None else f"DLS-{limit}",
        "env_n": env_n,
        "states_n": explored,
        "actions_count": 0,
        "actions_cost": 0,
        "time": elapsed,
        "solution_found": False,
        "path": []
    }


def run_ucs_episode(env, env_n=0, scenario=1):
    start_time = time.time()
    state, _ = env.reset()
    explored = 0
    visited = set()

    frontier = [(0, state, [])]  # (cost, state, path)

    while frontier:
        cost, current_state, path = heapq.heappop(frontier)
        if current_state in visited:
            continue
        visited.add(current_state)
        explored += 1

        for action in range(env.action_space.n):
            prob, next_state, reward, done = env.unwrapped.P[current_state][action][0]
            if next_state == current_state:
                continue

            step_cost = 1 if scenario == 1 else (1 if action in (0, 2) else 10)
            new_path = path + [action]
            new_cost = cost + step_cost

            if reward > 0:
                elapsed = time.time() - start_time
                return {
                    "algorithm_name": "UCS",
                    "env_n": env_n,
                    "states_n": explored,
                    "actions_count": len(new_path),
                    "actions_cost": new_cost,
                    "time": elapsed,
                    "solution_found": True,
                    "path": new_path
                }

            heapq.heappush(frontier, (new_cost, next_state, new_path))

    elapsed = time.time() - start_time
    return {
        "algorithm_name": "UCS",
        "env_n": env_n,
        "states_n": explored,
        "actions_count": 0,
        "actions_cost": 0,
        "time": elapsed,
        "solution_found": False,
        "path": []
    }


def run_a_star_episode(env, env_n=0, scenario=1):
    start_time = time.time()
    state, _ = env.reset()
    explored = 0
    visited = set()

    # find goal in env.desc
    goal_state = None
    for r in range(len(env.unwrapped.desc)):
        for c in range(len(env.unwrapped.desc[r])):
            if env.unwrapped.desc[r][c] == b'G':
                goal_state = r * len(env.unwrapped.desc) + c
                break
        if goal_state is not None:
            break

    size = int(env.observation_space.n ** 0.5)

    def heuristic(s):
        x1, y1 = divmod(s, size)
        x2, y2 = divmod(goal_state, size)
        return abs(x1 - x2) + abs(y1 - y2)

    frontier = [(heuristic(state), 0, state, [])]  # (f, g, state, path)

    while frontier:
        f, g, current_state, path = heapq.heappop(frontier)
        if current_state in visited:
            continue
        visited.add(current_state)
        explored += 1

        for action in range(env.action_space.n):
            prob, next_state, reward, done = env.unwrapped.P[current_state][action][0]
            if next_state == current_state:
                continue

            step_cost = 1 if scenario == 1 else (1 if action in (0, 2) else 10)
            new_path = path + [action]
            new_cost = g + step_cost

            if reward > 0:
                elapsed = time.time() - start_time
                return {
                    "algorithm_name": "A*",
                    "env_n": env_n,
                    "states_n": explored,
                    "actions_count": len(new_path),
                    "actions_cost": new_cost,
                    "time": elapsed,
                    "solution_found": True,
                    "path": new_path
                }

            heapq.heappush(frontier, (new_cost + heuristic(next_state), new_cost, next_state, new_path))

    elapsed = time.time() - start_time
    return {
        "algorithm_name": "A*",
        "env_n": env_n,
        "states_n": explored,
        "actions_count": 0,
        "actions_cost": 0,
        "time": elapsed,
        "solution_found": False,
        "path": []
    }


import csv


# Import the algorithms defined earlier
# (assuming they are in the same file or imported properly)
# run_random_episode, run_bfs_episode, run_dfs_episode, run_ucs_episode, run_a_star_episode

def generate_exercise_map(my_size=100, my_frozen_prob=0.92, slippery=False, max_steps=1000, render_mode=None):
    from gymnasium.envs.toy_text.frozen_lake import generate_random_map
    my_map = generate_random_map(size=my_size, p=my_frozen_prob)
    my_env = gym.make("FrozenLake-v1", desc=my_map, is_slippery=slippery, render_mode=render_mode)
    my_env = wrappers.TimeLimit(my_env, max_episode_steps=max_steps)
    return my_map, my_env


def run_experiments(num_envs=30, output_file="results.csv"):
    algorithms = [
        ("Random", run_random_episode),
        ("BFS", run_bfs_episode),
        ("DFS", lambda env, env_n, scenario: run_dfs_episode(env, env_n, scenario)),
        ("DLS-300", lambda env, env_n, scenario: run_dfs_episode(env, env_n, scenario, limit=300)),
        ("DLS-400", lambda env, env_n, scenario: run_dfs_episode(env, env_n, scenario, limit=400)),
        ("DLS-500", lambda env, env_n, scenario: run_dfs_episode(env, env_n, scenario, limit=500)),
        ("UCS", run_ucs_episode),
        ("A*", run_a_star_episode),
    ]

    fieldnames = [
        "algorithm_name",
        "env_n",
        "scenario",
        "states_n",
        "actions_count",
        "actions_cost",
        "time",
        "solution_found"
    ]

    results = []

    for env_n in range(1, num_envs + 1):
        print(f"\n=== Environment {env_n} ===")
        my_map, my_env = generate_exercise_map()

        for algo_name, algo_fn in algorithms:
            for scenario in [1, 2]:
                print(f"Running {algo_name} on scenario {scenario}...")
                try:
                    result = algo_fn(my_env, env_n, scenario)
                    result["algorithm_name"] = algo_name
                    result["env_n"] = env_n
                    result["scenario"] = scenario
                    # remove path before saving to CSV
                    if "path" in result:
                        result.pop("path")
                    results.append(result)
                except Exception as e:
                    print(f"Error running {algo_name} on env {env_n}, scenario {scenario}: {e}")
                    results.append({
                        "algorithm_name": algo_name,
                        "env_n": env_n,
                        "scenario": scenario,
                        "states_n": 0,
                        "actions_count": 0,
                        "actions_cost": 0,
                        "time": 0.0,
                        "solution_found": False
                    })

        my_env.close()

    # Save to CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {output_file}")


import time


def visualize_solution(env, path, delay=0.5):
    """
    Replay the solution path in the environment with rendering.
    """
    state, _ = env.reset()
    env.render()
    for action in path:
        state, reward, done, truncated, _ = env.step(action)
        env.render()
        time.sleep(delay)
        if done or truncated:
            break
    env.close()


if __name__ == "__main__":
    # run_experiments(num_envs=30, output_file="../results.csv")
    plot.plot_boxplots("../results.csv")

    # TESTING
    # from gymnasium import wrappers
    # import gymnasium as gym
    #
    # _, env = generate_exercise_map(my_size=50, my_frozen_prob=0.8, slippery=False, max_steps=100, render_mode="human")
    #
    # result = run_bfs_episode(env, env_n=0, scenario=1)
    #
    # if result["solution_found"]:
    #     print("Visualizing BFS solution...")
    #     visualize_solution(env, result["path"], delay=0.5)
    # else:
    #     print("No solution found to visualize.")
