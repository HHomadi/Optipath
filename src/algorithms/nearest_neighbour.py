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

class NearestNeighbour:
    def __init__(self, adjacency_matrix: List[List[int]], start_node: int = 0):
        """
        Initializes the Nearest Neighbour algorithm with a starting node and an adjacency matrix.

        Args:
            start_node (int): The starting node for the tour.
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
        """

        self.adjacency_matrix = adjacency_matrix

        self.num_points = 0

        self.unvisited = set()

        self.tour = []

        self.execution_time = 0

        self.start_node = start_node

    def run(self):

        """
        Runs the Nearest Neighbour algorithm to construct a tour.
        """

        self.num_points = len(self.adjacency_matrix)

        self.unvisited = set(range(self.num_points))

        self.tour = [self.start_node]

        self.unvisited.remove(self.start_node)

        start_time = time.time()

        while self.unvisited:
            current_point = self.tour[-1]

            nearest_point = min(self.unvisited, key=lambda x: self.adjacency_matrix[current_point][x])

            self.tour.append(nearest_point)

            self.unvisited.remove(nearest_point)
            print(self.tour)

        self.tour.append(self.tour[0])
        end_time = time.time()

        self.execution_time = end_time - start_time
    def calculate_tour_length(self) -> int:

        """
        Calculates the total length of the constructed tour.

        Returns:
            int: The total length of the tour.
        """

        length = 0

        for i in range(len(self.tour) - 1):

            length += self.adjacency_matrix[self.tour[i]][self.tour[i + 1]]

        return length


    def solve(self, start_node: int = 0):
        self.start_node = start_node
        self.run()
        return self.tour, float(self.calculate_tour_length()), self.execution_time

