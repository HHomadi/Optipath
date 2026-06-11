import numpy as np
import itertools
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

class LinKernighan:

    def __init__(self, adjacency_matrix: List[List[int]]):

        """
        Initializes the Lin-Kernighan algorithm with an adjacency matrix.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
        """

        self.adjacency_matrix = adjacency_matrix

    def calculate_tour_length(self, tour: List[int]) -> int:

        """
        Calculates the total length of a tour.

        Args:
            tour (List[int]): The tour represented as a list of nodes.

        Returns:
            int: The total length of the tour.
        """

        length = 0

        n = len(tour)

        for i in range(n):
            length += self.adjacency_matrix[tour[i]][tour[(i + 1) % n]]

        return length

    def lin_kernighan(self, start_node: int) -> Tuple[List[int], int, float]:

        """
        Applies the Lin-Kernighan algorithm to find an improved tour.

        Args:
            start_node (int): The starting node for the tour.

        Returns:
            Tuple[List[int], int, float]: Tuple containing the best tour found, its length, and the execution time.
        """

        n = len(self.adjacency_matrix)

        best_tour = list(range(n))
        best_length = self.calculate_tour_length(best_tour)

        start_index = best_tour.index(start_node)
        best_tour = best_tour[start_index:] + best_tour[:start_index]

        start_time = time.time()

        for K in range(2, n):
            for subset in itertools.combinations(range(n), K):
                subset = list(subset)

                for i in range(K):
                    j = (i + 1) % K  # wraps so the last element pairs with the first
                    tour = best_tour[:]
                    tour[subset[i]], tour[subset[j]] = tour[subset[j]], tour[subset[i]]

                    tour_length = self.calculate_tour_length(tour)

                    if tour_length < best_length:
                        best_tour = tour
                        print("Current Tour:", best_tour)
                        best_length = tour_length

        end_time = time.time()
        execution_time = end_time - start_time

        start_index = best_tour.index(start_node)
        best_tour = best_tour[start_index:] + best_tour[:start_index]
        best_tour.append(start_node)

        return best_tour, best_length, execution_time

