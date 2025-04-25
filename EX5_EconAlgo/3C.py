from itertools import product
from typing import List
import copy
import time
import random
import matplotlib.pyplot as plt

MAX_VAL = 2**32  # value range according to assignment

def egalitarian_allocation(valuations: List[List[float]], use_gap_pruning=False):
    num_players = len(valuations)
    num_items = len(valuations[0])
    best_allocation = None
    best_min_value = float('-inf')
    seen_states = set()

    # optimistic bound calculation
    def optimistic_bound(current_values, remaining_items):
        bounds = current_values[:]
        for item in remaining_items:
            for i in range(num_players):
                bounds[i] += valuations[i][item]
        return min(bounds)

    # DFS with pruning
    def dfs(item_index, allocation, current_values):
        nonlocal best_allocation, best_min_value

        # Rule A: skip identical states
        state_key = (tuple(current_values), item_index)
        if state_key in seen_states:
            return
        seen_states.add(state_key)

        # All items assigned
        if item_index == num_items:
            min_value = min(current_values)
            if min_value > best_min_value:
                best_min_value = min_value
                best_allocation = copy.deepcopy(allocation)
            return

        # Rule B: optimistic bound
        optimistic = optimistic_bound(current_values, range(item_index, num_items))
        if optimistic <= best_min_value:
            return

        # Rule C: gap pruning
        if use_gap_pruning:
            remaining_max_gain = sum(
                max(valuations[i][item] for i in range(num_players))
                for item in range(item_index, num_items)
            )
            if max(current_values) - min(current_values) > remaining_max_gain:
                return

        # Try assigning current item to each player
        for player in range(num_players):
            allocation[player].append(item_index)
            current_values[player] += valuations[player][item_index]
            dfs(item_index + 1, allocation, current_values)
            current_values[player] -= valuations[player][item_index]
            allocation[player].pop()

    # Initialization
    allocation = [[] for _ in range(num_players)]
    current_values = [0] * num_players
    dfs(0, allocation, current_values)

def generate_random_valuations(num_players, num_items):
    return [[random.randint(1, MAX_VAL) for _ in range(num_items)] for _ in range(num_players)]

def measure_runtimes(num_players, max_items, use_gap_pruning=False):
    times = []
    for num_items in range(1, max_items + 1):
        valuations = generate_random_valuations(num_players, num_items)
        start = time.time()
        egalitarian_allocation(valuations, use_gap_pruning=use_gap_pruning)
        end = time.time()
        times.append(end - start)
    return times

# Compare runtimes with and without Gap Pruning
max_items = 10
item_counts = list(range(1, max_items + 1))

runtimes_no_gap = measure_runtimes(num_players=3, max_items=max_items, use_gap_pruning=False)
runtimes_with_gap = measure_runtimes(num_players=3, max_items=max_items, use_gap_pruning=True)

# Plot runtime comparison
plt.plot(item_counts, runtimes_no_gap, marker='o', label='Without Gap Pruning')
plt.plot(item_counts, runtimes_with_gap, marker='s', label='With Gap Pruning')

plt.title('Runtime Comparison (3 Players)')
plt.xlabel('Number of Items')
plt.ylabel('Runtime (seconds)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
