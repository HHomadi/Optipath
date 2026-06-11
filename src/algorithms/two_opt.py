import numpy as np
import time
import sys
from typing import List, Tuple

logfile = open('logfile2.txt', 'a')
def custom_print(*args, **kwargs):
    output = ' '.join(map(str, args))
    sys.stdout.write(output + '\n')
    logfile.write(output + '\n')
    logfile.flush()

built_in_print = print
print = custom_print

class TwoOpt:

    def __init__(self, adjacency_matrix: List[List[int]]):

        """
        Initializes the Two-Opt algorithm with an adjacency matrix.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
        """

        self.adjacency_matrix = adjacency_matrix

    def total_distance(self, tour: List[int]) -> int:

        """
        Calculates the total distance of a tour.

        Args:
            tour (List[int]): The tour represented as a list of nodes.

        Returns:
            int: The total distance of the tour.
        """

        distance = 0

        for i in range(len(tour) - 1):
            distance += self.adjacency_matrix[tour[i]][tour[i+1]]

        distance += self.adjacency_matrix[tour[-1]][tour[0]]

        return distance

    def dos_opt(self, tour: List[int]) -> List[int]:

        """
        Applies the Two-Opt algorithm to improve a tour.

        Args:
            tour (List[int]): The initial tour.

        Returns:
            List[int]: The optimized tour.
        """

        n = len(tour)

        best_tour = tour[:]

        improved = True

        while improved:
            improved = False

            for i in range(1, n - 2):
                for j in range(i + 1, n):

                    if j - i == 1:
                        continue

                    new_tour = tour[:]

                    new_tour[i:j] = tour[j - 1:i - 1:-1]  # reverse the segment between i and j

                    if self.total_distance(new_tour) < self.total_distance(best_tour):

                        best_tour = new_tour

                        improved = True

                        print("Current Tour:", best_tour)

            tour = best_tour

        return best_tour

    def solve(self, start_node: int = 0) -> Tuple[List[int], int, float]:

        """
        Solves the TSP using the Two-Opt algorithm.

        Args:
            start_node (int): The starting node for the tour. Defaults to 0.

        Returns:
            Tuple[List[int], int, float]: Tuple containing the optimized tour, its distance, and the execution time.
        """

        initial_tour = list(range(len(self.adjacency_matrix)))

        initial_tour.remove(start_node)

        initial_tour = [start_node] + initial_tour

        start_time = time.time()

        initial_tour.append(start_node)

        optimized_tour = self.dos_opt(initial_tour)

        end_time = time.time()

        execution_time = end_time - start_time

        optimized_tour.append(start_node)

        optimal_distance = self.total_distance(optimized_tour)

        return optimized_tour, optimal_distance, execution_time

