import numpy as np
import time
import sys

logfile = open('logfile2.txt', 'a')
def custom_print(*args, **kwargs):
    output = ' '.join(map(str, args))
    sys.stdout.write(output + '\n')
    logfile.write(output + '\n')
    logfile.flush()

built_in_print = print
print = custom_print

class HeldKarp:

    def __init__(self, adjacency_matrix, start_node=0):
        """
        Initializes the Held-Karp algorithm with an adjacency matrix and starting node.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
            start_node (int, optional): The starting node for the traversal. Defaults to 0.
        """

        self.adjacency_matrix = adjacency_matrix
        self.num_cities = len(adjacency_matrix)

        self.start_node = start_node
        # 1 << num_cities = 2^n possible subsets of cities (bitmask DP), each cell stores min cost for that subset+position
        self.memo = np.full((1 << self.num_cities, self.num_cities), -1, dtype=np.int64)

        self.execution_time = None

    def held_karp(self):
        """
        Runs the Held-Karp algorithm to find the minimum-cost Hamiltonian cycle.

        Returns:
            Tuple[int, List[int], float]: Tuple containing the minimum cost, optimal path, and execution time.
        """

        start_time = time.time()

        min_cost = self.calculate_minimum_cost(1 << self.start_node, self.start_node)
        optimal_path = self.reconstruct_path()

        end_time = time.time()
        execution_time = end_time - start_time

        return min_cost, optimal_path, execution_time

    def calculate_minimum_cost(self, mask, pos):
        """
        Calculates the minimum cost of the Hamiltonian cycle starting from the given position.

        Args:
            mask (int): A bitmask representing visited cities.
            pos (int): The current position in the cycle.

        Returns:
            int: The minimum cost of the Hamiltonian cycle.
        """

        # all bits set means every city has been visited, so just return cost of going back to start
        if mask == (1 << self.num_cities) - 1:
            return self.adjacency_matrix[pos][self.start_node]

        if self.memo[mask][pos] != -1:
            return self.memo[mask][pos]

        min_cost = float('inf')

        for next_city in range(self.num_cities):
            if (mask >> next_city) & 1 == 0:  # bit not set = city not visited yet
                new_mask = mask | (1 << next_city)
                cost = self.adjacency_matrix[pos][next_city] + self.calculate_minimum_cost(new_mask, next_city)

                if cost < min_cost:
                    min_cost = cost

            print("Iteration: mask={}, pos={}, next_city={}, min_cost={}".format(mask, pos, next_city, min_cost))

        self.memo[mask][pos] = min_cost

        return min_cost

    def reconstruct_path(self):

        """
        Reconstructs the optimal path for the minimum-cost Hamiltonian cycle.

        Returns:
            List[int]: The optimal path.
        """

        path = [self.start_node]
        mask = 1 << self.start_node

        current_city = self.start_node

        while len(path) < self.num_cities:

            min_cost = float('inf')
            next_city = None

            for city in range(self.num_cities):
                if (mask >> city) & 1 == 0:
                    cost = self.adjacency_matrix[current_city][city] + self.memo[mask][city]
                    if cost < min_cost:
                        min_cost = cost
                        next_city = city

            path.append(next_city)
            mask |= (1 << next_city)
            current_city = next_city

        path.append(self.start_node)

        return path

