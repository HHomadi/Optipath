import itertools
from typing import List, Tuple
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

class BruteForce:
    def __init__(self, adjacency_matrix: List[List[int]], start_node: int = 0, print_iterations: bool = False):
        """
        Initializes the brute-force algorithm with an adjacency matrix and starting node.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
            start_node (int): The starting node for the traversal.
            print_iterations (bool): Whether to print all permutations being evaluated.
        """
        self.adjacency_matrix = np.array(adjacency_matrix)

        self.instance_size = len(adjacency_matrix)

        self.start_node = start_node

        self.memo = {}

        self.print_iterations = print_iterations

    def calculate_route_cost(self, route: Tuple[int]) -> Tuple[Tuple[int], int]:
        """
        Calculates the cost of a given route.

        Args:
            route (Tuple[int]): The route to calculate the cost for.

        Returns:
            Tuple[Tuple[int], int]: Tuple containing the route and its corresponding cost.
        """

        if route in self.memo:
            return route, self.memo[route]

        travel_cost = 0
        for i in range(len(route) - 1):
            travel_cost += self.adjacency_matrix[route[i]][route[i + 1]]

        self.memo[route] = travel_cost
        return route, travel_cost

    def generate_routes(self) -> List[Tuple[int]]:
        """
        Generates all possible routes starting from the given start node.

        Returns:
            List[Tuple[int]]: List of all possible routes.
        """

        lang = [x for x in range(self.instance_size) if x != self.start_node]

        routes = list(itertools.permutations(lang))

        routes_with_return = [(self.start_node,) + route + (self.start_node,) for route in routes]

        return routes_with_return

    def solve(self, start_node: int = 0):
        self.start_node = start_node
        """
        Finds the shortest route and its cost among all possible routes.

        Returns:
            Tuple[Tuple[int], int, float]: Tuple containing the shortest route, its cost, and the elapsed time.
        """
        routes = self.generate_routes()

        if self.print_iterations:

            print("All permutations being evaluated:")

            for route in routes:
                print(list(route))

        start_time = time.time()

        results = [self.calculate_route_cost(route) for route in routes]

        shortest_route, shortest_cost = min(results, key=lambda x: x[1])

        end_time = time.time()

        elapsed_time = end_time - start_time

        return shortest_route, shortest_cost, elapsed_time

