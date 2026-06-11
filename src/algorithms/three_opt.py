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

class ThreeOpt:

    def __init__(self, adjacency_matrix):

        """
        Initializes the Three-Opt algorithm with an adjacency matrix.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
        """

        self.adjacency_matrix = adjacency_matrix

    def total_distance(self, route):

        """

        Calculates the total distance of a route.

        Args:
            route (List[int]): The route represented as a list of nodes.

        Returns:
            int: The total distance of the route.
        """

        distance = 0

        for i in range(len(route)):
            distance += self.adjacency_matrix[route[i - 1]][route[i]]  # when i=0, route[-1] wraps to last element

        return distance

    def tres_opt(self, route):

        """
        Applies the Three-Opt algorithm to improve a route.

        Args:
            route (List[int]): The initial route.

        Returns:
            Tuple[List[int], int]: Tuple containing the optimized route and its distance.
        """

        n = len(route)

        min_distance = self.total_distance(route)

        improved = True

        iteration = 0

        while improved:

            improved = False

            for i in range(1, n - 2):
                for j in range(i + 2, n):

                    new_route = route[:i] + route[i:j][::-1] + route[j:]
                    new_distance = self.total_distance(new_route)

                    if new_distance < min_distance:

                        route = new_route

                        min_distance = new_distance

                        improved = True

                        iteration += 1

                        print(f"Best tour: {route}")

        return route, min_distance

    def solve(self, start_node=0):

        """
        Solves the TSP using the Three-Opt algorithm.

        Args:
            start_node (int): The starting node for the tour. Defaults to 0.

        Returns:
            Tuple[List[int], int, float]: Tuple containing the optimized route, its distance, and the execution time.
        """

        initial_route = list(range(len(self.adjacency_matrix)))

        initial_route.remove(start_node)

        initial_route = [start_node] + initial_route

        initial_route.append(start_node)

        start_time = time.time()

        optimized_route, optimized_distance = self.tres_opt(initial_route)

        end_time = time.time()

        execution_time = end_time - start_time

        return optimized_route, optimized_distance, execution_time