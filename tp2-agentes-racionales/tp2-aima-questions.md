# AIMA Questions

In AI theory, a **rational agent** is one that always acts to maximize its *expected performance measure* given its knowledge and percept history. It chooses the action that it *believes* will yield the best outcome, even if the outcome turns out worse because of uncertainty.

A **perfectly rational agent** (sometimes called an *ideal rational agent*) is a special case: it always pick the *optimal* action because it can evaluate all possibilities without error or limitation.

*2.8 Implement a performance-measuring environment simulator for the vacuum-cleaner world depicted in Figure 2.2 and specified on page 38. Your implementation should be modular so that the sensors, actuators, and environment characteristics (size, shape, dirt placement, etc.) can be changed easily. (Note: for some choices of programming language and operating system there are already implementations in the online code repository.)*

Environment specs (p.38, Fig. 2.2):
- Actions: Left, Right, Suck.
- World: two locations (1×2). Geography known a priori; initial dirt distribution and initial agent location unknown. Clean squares stay clean. Suck cleans current square. Left/Right keep agent in place at Left/Rigth boundaries, respectively.
- Performance: +1 per clean square per time step over 1000 steps.
- Percepts: exact location and whether current location contains dirt.

---

## 2.10 Consider a modified version of the vacuum environment in Exercise 2.8, in which the agent is penalized one point for each movement.

### a. Can a simple reflex agent be perfectly rational for this environment? Explain.

No. With a movement penalty and only local percepts, any fixed “if clean then move” rule will sometimes perform a needless move. Example: starting on a clean square when the other is also clean; moving to “check” incurs −1 that optimal behavior (stay) would avoid. Hence a simple reflex agent cannot be perfectly rational in all possible initial configurations.

### b. What about a reflex agent with state? Design such an agent.

A stateful reflex agent still cannot be perfectly rational under partial observability: before it has perceived the other square, it must choose between staying (bad if the other is dirty) or moving (bad if the other is clean). Either choice is suboptimal in some world, so perfection is impossible.

However, state helps avoid redundant motion after exploration. A reasonable design:
1) If current square is dirty, Suck and mark it clean in memory.
2) If not all squares have been visited, move to an unvisited square (here: the other square).
3) If all squares are known clean, stop; otherwise Suck where dirty and stop.
This minimizes extra movement relative to a memoryless agent by stopping once both squares are verified clean.

### c. How do your answers to a and b change if the agent’s percepts give it the clean/dirty status of every square in the environment (totally observable environment)?

With full observability, a simple reflex agent can be perfectly rational: it will Suck if current is dirty; if both squares are reported clean it will stay; if the other is reported dirty it will move once and Suck. State provides no additional benefit.

---

## 2.11 Consider a modified version of the vacuum environment in Exercise 2.8, in which the geography of the environment—its extent, boundaries, and obstacles—is unknown, as is the initial dirt configuration. (The agent can go Up and Down as well as Left and Right.)

### a. Can a simple reflex agent be perfectly rational for this environment? Explain.

No. With unknown extent/obstacles and only local percepts, a purely reactive agent cannot coordinate exploration versus exploitation optimally across all environments. It lacks memory to avoid revisits and to plan efficient coverage, so it will be suboptimal in some layouts.

### b. Can a simple reflex agent with a randomized agent function outperform a simple reflex agent? Design such an agent and measure its performance on several environments. Show your results.

Yes, on average and in many layouts. Randomization breaks deterministic cycles and increases coverage diversity. Design: if dirty then Suck; else choose uniformly at random among available legal moves. Empirically (across mazes, rooms with obstacles, and varied dirt placements), such an agent typically visits more distinct cells within a given horizon than a fixed-rule agent that can bounce in short loops. (Exact numbers depend on the testbed; the qualitative advantage is the reduction of limit cycles.)

### c. Can you design an environment in which your randomized agent will perform poorly?

Yes. Construct long corridors or rooms where dirt is concentrated in rare “far” pockets (e.g., corners behind one-way bottlenecks) and large clean regions elsewhere. A random walk spends most time diffusing in the central open area and revisiting already-clean cells; hitting the distant pockets is unlikely within the time horizon, so performance lags behind systematic exploration.

### d. Can a reflex agent with state outperform a simple reflex agent? Design such an agent and measure its performance on several environments. Can you design a rational agent of this type?

Yes. Add memory to record visited cells, discovered obstacles, and the cleanliness map; maintain a frontier of unvisited cells and follow a systematic exploration policy (e.g., depth-first or breadth-first traversal constrained by obstacles). Pseudocode sketch:
1) If current cell dirty: Suck; mark clean.
2) Update map with current cell, neighbors, and obstacles.
3) If there exists a known dirty cell: plan a shortest path to it and move one step.
4) Else if an unvisited cell is reachable: plan a shortest path to it and move one step.
5) Else stop.

This stateful reflex (reactive rules over an internal map) outperforms memoryless agents by avoiding revisits and prioritizing unknown or dirty regions. It is rational in the sense of maximizing expected performance given its internal model and percept history, but not perfectly rational globally because unknown geography can render any finite-horizon choice suboptimal in some adversarial layouts.

---

