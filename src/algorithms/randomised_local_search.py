import numpy as np
import time
import sys
import random
from typing import List, Tuple

logfile = open('logfile2.txt', 'a')
def custom_print(*args, **kwargs):
    output = ' '.join(map(str, args))
    sys.stdout.write(output + '\n')
    logfile.write(output + '\n')
    logfile.flush()

built_in_print = print
print = custom_print

class RandomisedLocalSearch:
    def __init__(self, adjacency_matrix: List[List[int]]):

        """
        Initializes the Randomised Local Search algorithm with an adjacency matrix.

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

        tour2 = tour.copy()

        tour2.append(tour[0])

        for i in range(len(tour2) - 1):

            distance += self.adjacency_matrix[tour2[i]][tour2[i+1]]

        distance += self.adjacency_matrix[tour2[-1]][tour2[0]]

        return distance

    def RandomSearch(self, adjacency_matrix: List[List[int]]) -> Tuple[List[int], int, float]:

        """
        Applies the Randomised Local Search algorithm to find an improved tour.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.

        Returns:
            Tuple[List[int], int, float]: Tuple containing the best tour found, its distance, and the execution time.
        """

        iterations = max(1000, 10000 // len(adjacency_matrix))  # fewer iterations for bigger graphs, min 1000

        num_cities = len(self.adjacency_matrix)
        current_tour = list(range(num_cities))

        random.shuffle(current_tour)
        start_node = random.choice(current_tour)

        start_index = current_tour.index(start_node)
        current_tour = current_tour[start_index:] + current_tour[:start_index]

        best_tour = list(current_tour)
        best_distance = self.total_distance(current_tour)

        start_time = time.time()

        for _ in range(iterations):

            i, j = random.sample(range(num_cities), 2)

            current_tour[i], current_tour[j] = current_tour[j], current_tour[i]

            current_distance = self.total_distance(current_tour)

            if current_distance < best_distance:

                print("Current Tour:", best_tour)

                best_tour = list(current_tour)

                best_distance = current_distance

        end_time = time.time()

        execution_time = end_time - start_time

        best_tour.append(best_tour[0])

        return best_tour, best_distance, execution_time
