import random
import time
import numpy as np
import sys
from typing import List, Tuple

logfile = open('logfile2.txt', 'a')
def custom_print(*args, **kwargs):
    output = ' '.join(map(str, args))
    sys.stdout.write(output + '\\n')
    logfile.write(output + '\\n')
    logfile.flush()

built_in_print = print
print = custom_print

class Insertion:
    def __init__(self, adjacency_matrix, start_node: int = 0):

        """
        Initializes the Insertion algorithm with an adjacency matrix and starting node.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
            start_node (int): The starting node for the traversal.
        """

        self.adjacency_matrix = adjacency_matrix
        self.start_node = start_node

        self.tour = [start_node]

        self.unvisited = list(range(len(adjacency_matrix)))

        self.unvisited.remove(start_node)

        self.execution_time = 0

    def calculate_tour_length(self, tour: List[int]) -> int:

        """
        Calculates the total length of a tour.

        Args:
            tour (List[int]): The tour to calculate the length for.

        Returns:
            int: The total length of the tour.
        """

        tour_length = 0

        for i in range(len(tour) - 1):
            tour_length += self.adjacency_matrix[tour[i]][tour[i + 1]]

        return tour_length

class NearestInsertion(Insertion):

    def solve(self, start_node: int = 0):
        self.start_node = start_node
        t, d = self.run()
        return t, float(d), getattr(self, 'execution_time', 0.0)

    def run(self):

        """
        Executes the Nearest Insertion algorithm to construct a tour.

        Returns:
            Tuple[List[int], int]: The constructed tour and its total length.
        """

        start_time = time.time()

        print("Current Tour:", self.tour)

        while self.unvisited:

            min_distance = float('inf')
            nearest_city = None
            insert_position = None

            for city in self.tour:
                for unvisited_city in self.unvisited:
                    if self.adjacency_matrix[city][unvisited_city] < min_distance:

                        min_distance = self.adjacency_matrix[city][unvisited_city]

                        nearest_city = unvisited_city
                        insert_position = city

            self.tour.insert(self.tour.index(insert_position) + 1, nearest_city)

            print("Current Tour:", self.tour)

            self.unvisited.remove(nearest_city)

        self.tour.append(self.tour[0])

        tour_length = self.calculate_tour_length(self.tour)

        end_time = time.time()
        self.execution_time = end_time - start_time

        return self.tour, tour_length

class FarthestInsertion(Insertion):

    def find_farthest_city(self):
        """
        Finds the farthest unvisited city from the current tour.

        Returns:
            int: The farthest unvisited city.
        """

        return max(self.unvisited, key=lambda city: min(self.adjacency_matrix[city][self.tour[i]] for i in range(len(self.tour))))

    def find_best_insertion(self, farthest_city):

        """
        Finds the best position to insert the farthest city into the tour.

        Args:
            farthest_city (int): The farthest unvisited city.

        Returns:
            int: The best position for insertion.
        """

        min_insertion_cost = float('inf')
        best_position = 0

        for i in range(len(self.tour) - 1):
            for j in range(i + 1, len(self.tour)):

                cost_increase = (
                    self.adjacency_matrix[self.tour[i]][farthest_city]
                    + self.adjacency_matrix[farthest_city][self.tour[j]]
                    - self.adjacency_matrix[self.tour[i]][self.tour[j]]
                )

                if cost_increase < min_insertion_cost:

                    min_insertion_cost = cost_increase
                    best_position = j

        return best_position

    def solve(self, start_node: int = 0):
        self.start_node = start_node
        t, d = self.run()
        return t, float(d), getattr(self, 'execution_time', 0.0)

    def run(self):
        """
        Executes the Farthest Insertion algorithm to construct a tour.

        Returns:
            Tuple[List[int], int]: The constructed tour and its total length.
        """
        start_time = time.time()
        print("Current Tour:", self.tour)

        while self.unvisited:
            farthest_city = self.find_farthest_city()
            best_position = self.find_best_insertion(farthest_city)

            self.tour.insert(best_position, farthest_city)

            print("Current Tour:", self.tour)

            self.unvisited.remove(farthest_city)

        self.tour.insert(0, self.start_node)
        tour_length = self.calculate_tour_length(self.tour)

        end_time = time.time()
        self.execution_time = end_time - start_time

        return self.tour, tour_length
class RandomInsertion(Insertion):

    def find_tour(self):
        """
        Finds a tour using random insertion heuristic.
        """
        current_city = random.choice(self.unvisited)

        self.tour.append(current_city)

        print("Current Tour:", self.tour)

        self.unvisited.remove(current_city)

        while self.unvisited:

            random_city = random.choice(self.unvisited)
            min_increase = float('inf')

            best_position = 0

            for i in range(len(self.tour)):

                temp_tour = self.tour[:]
                temp_tour.insert(i, random_city)

                tour_length = 0

                for j in range(len(temp_tour) - 1):
                    tour_length += self.adjacency_matrix[temp_tour[j]][temp_tour[j+1]]

                tour_length += self.adjacency_matrix[temp_tour[-1]][temp_tour[0]]

                if tour_length < min_increase:
                    min_increase = tour_length
                    best_position = i

            self.tour.insert(best_position, random_city)

            print("Current Tour:", self.tour)

            self.unvisited.remove(random_city)

        self.tour.append(self.tour[0])

    def solve(self, start_node: int = 0):
        self.start_node = start_node
        t, d, time = self.run()
        return t, float(d), time

    def run(self):
        """
        Executes the Random Insertion algorithm to construct a tour.

        Returns:
            Tuple[List[int], int, float]: The constructed tour, its total length, and the execution time.
        """

        start_time = time.time()

        self.find_tour()

        total_distance = self.calculate_tour_length(self.tour)

        end_time = time.time()
        self.execution_time = end_time - start_time

        return self.tour, total_distance, self.execution_time

class CheapestInsertion(Insertion):

    def solve(self, start_node: int = 0):
        self.start_node = start_node
        t, d, time = self.run()
        return t, float(d), time

    def run(self):

        """
        Executes the Cheapest Insertion algorithm to construct a tour.

        Returns:
            Tuple[List[int], int, float]: The constructed tour, its total length, and the execution time.
        """

        start_time = time.time()

        num_cities = len(self.adjacency_matrix)

        unvisited_cities = set(range(num_cities))

        tour = [self.start_node, self.start_node + 1]
        print("Current Tour:", tour)

        unvisited_cities.remove(self.start_node)
        unvisited_cities.remove(self.start_node + 1)

        while len(tour) < num_cities:

            min_cost = float('inf')
            cheapest_city = -1

            for current_city in tour:
                for candidate_city in unvisited_cities:

                    cost = self.adjacency_matrix[current_city][candidate_city]

                    if cost < min_cost:
                        min_cost = cost
                        cheapest_city = candidate_city

            best_position = 0
            best_cost = float('inf')

            for i in range(len(tour)):

                new_cost = (
                    self.adjacency_matrix[tour[i]][cheapest_city] +
                    self.adjacency_matrix[cheapest_city][tour[(i + 1) % len(tour)]] -
                    self.adjacency_matrix[tour[i]][tour[(i + 1) % len(tour)]]
                )

                if new_cost < best_cost:
                    best_cost = new_cost
                    best_position = i

            tour.insert((best_position + 1) % len(tour), cheapest_city)

            print("Current Tour:", tour)

            unvisited_cities.remove(cheapest_city)

        tour.append(self.start_node)
        tour_length = self.calculate_tour_length(tour)

        end_time = time.time()
        execution_time = end_time - start_time
        return tour, tour_length, execution_time

