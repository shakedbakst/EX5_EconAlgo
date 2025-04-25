from itertools import product
from typing import List
import copy
import time
import random
import matplotlib.pyplot as plt

"""Question 3A"""

print("Answer for 3A:")

def egalitarian_allocation(valuations: List[List[float]]):
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

        # Rule A: prune identical states
        state_key = (tuple(current_values), item_index)
        if state_key in seen_states:
            return
        seen_states.add(state_key)

        # all items allocated
        if item_index == num_items:
            min_value = min(current_values)
            if min_value > best_min_value:
                best_min_value = min_value
                best_allocation = copy.deepcopy(allocation)
            return

        # Rule B: prune by optimistic bound
        optimistic = optimistic_bound(current_values, range(item_index, num_items))
        if optimistic <= best_min_value:
            return

        # try assigning current item to each player
        for player in range(num_players):
            allocation[player].append(item_index)
            current_values[player] += valuations[player][item_index]
            dfs(item_index + 1, allocation, current_values)
            current_values[player] -= valuations[player][item_index]
            allocation[player].pop()

    # start: empty allocation
    allocation = [[] for _ in range(num_players)]
    current_values = [0] * num_players
    dfs(0, allocation, current_values)

    # print result
    for i, items in enumerate(best_allocation):
        total_value = sum(valuations[i][item] for item in items)
        print(f"Player {i} gets items {items} with value {total_value}")


# example run
egalitarian_allocation([[4, 5, 6, 7, 8], [8, 7, 6, 5, 4]])


"""Question 3B"""

print("Answer for 3B:")

MAX_VAL = 2**32  # value range according to assignment


# generate random valuation matrix
def generate_random_valuations(num_players, num_items):
    return [[random.randint(1, MAX_VAL) for _ in range(num_items)] for _ in range(num_players)]


# measure runtime for given number of players
def measure_runtimes(num_players, max_items):
    times = []
    for num_items in range(1, max_items + 1):
        valuations = generate_random_valuations(num_players, num_items)
        start = time.time()
        egalitarian_allocation(valuations)
        end = time.time()
        elapsed = end - start
        times.append(elapsed)
        print(f"Players: {num_players}, Items: {num_items}, Time: {elapsed:.4f} seconds")
    return times


# range of item counts
max_items = 10
item_counts = list(range(1, max_items + 1))

# run for 2, 3, and 4 players
runtimes_2 = measure_runtimes(num_players=2, max_items=max_items)
runtimes_3 = measure_runtimes(num_players=3, max_items=max_items)
runtimes_4 = measure_runtimes(num_players=4, max_items=max_items)

# plot results
plt.plot(item_counts, runtimes_2, marker='o', label='2 players')
plt.plot(item_counts, runtimes_3, marker='s', label='3 players')
plt.plot(item_counts, runtimes_4, marker='^', label='4 players')

plt.title('Runtime vs. Number of Items (values from 1 to 2^32)')
plt.xlabel('Number of Items')
plt.ylabel('Runtime (seconds)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
