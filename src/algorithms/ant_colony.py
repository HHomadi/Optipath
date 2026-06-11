import numpy as np
import random
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

class AntColony:
    def __init__(self, adjacency_matrix: List[List[float]], num_ants: int = 20, pheromone_evaporation_rate: float = 0.5, alpha: float = 1.0, beta: float = 2.0, starting_city: int = 0, elite_ants_percent: float = 0.1):
        """
        Initialize the AntColony instance with the given parameters.
        """
        self.adjacency_matrix = adjacency_matrix

        self.num_ants = num_ants

        self.pheromone_evaporation_rate = pheromone_evaporation_rate

        self.alpha = alpha
        self.beta = beta

        self.starting_city = starting_city

        self.elite_ants_percent = elite_ants_percent

    def solve(self, start_node: int = 0) -> Tuple[List[int], float, float]:
        self.starting_city = start_node
        """
        Perform Ant Colony Optimization to find the best tour.
        """

        num_cities = len(self.adjacency_matrix)

        num_iterations = num_cities * 5

        start_time = time.time()

        pheromone_levels = np.ones_like(self.adjacency_matrix) / num_cities

        best_tour = None
        best_tour_length = float('inf')

        for iteration in range(num_iterations):
            ant_tours = []

            for ant in range(self.num_ants):

                current_city = self.starting_city

                tour = [current_city]
                tour_length = 0

                for _ in range(num_cities - 1):

                    unvisited_cities = [city for city in range(num_cities) if city not in tour]

                    probabilities = [
                        (pheromone_levels[current_city][next_city] ** self.alpha) *
                        ((1 / self.adjacency_matrix[current_city][next_city]) ** self.beta) for next_city in unvisited_cities]

                    total_prob = sum(probabilities)

                    probabilities = [prob / total_prob for prob in probabilities]

                    next_city = random.choices(unvisited_cities, probabilities)[0]

                    tour.append(next_city)

                    tour_length += self.adjacency_matrix[current_city][next_city]

                    current_city = next_city

                tour_length += self.adjacency_matrix[tour[-1]][tour[0]]

                tour.append(tour[0])

                ant_tours.append((tour, tour_length))

                if tour_length < best_tour_length:

                    best_tour_length = tour_length

                    best_tour = tour

            pheromone_levels *= (1 - self.pheromone_evaporation_rate)

            # reinforce paths taken by the best ants
            num_elite_ants = int(self.elite_ants_percent * self.num_ants)

            elite_ants = sorted(ant_tours, key=lambda x: x[1])[:num_elite_ants]

            for tour, tour_length in elite_ants:
                for i in range(num_cities):

                    j = (i + 1) % num_cities
                    pheromone_levels[tour[i]][tour[j]] += 1 / tour_length

            print("Iteration:", iteration + 1, "Current Tour:", best_tour)

        end_time = time.time()

        elapsed_time = end_time - start_time

        return best_tour, best_tour_length, elapsed_time


