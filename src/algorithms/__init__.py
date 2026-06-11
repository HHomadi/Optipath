"""
TSP algorithms with a common interface: solve(start_node) -> (tour, length, time).
"""
from algorithms.ant_colony import AntColony
from algorithms.brute_force import BruteForce
from algorithms.christofides import Christofides
from algorithms.two_opt import TwoOpt
from algorithms.three_opt import ThreeOpt
from algorithms.held_karp import HeldKarp
from algorithms.lin_kernighan import LinKernighan
from algorithms.nearest_neighbour import NearestNeighbour
from algorithms.insertion_algorithms import (
    CheapestInsertion,
    FarthestInsertion,
    NearestInsertion,
    RandomInsertion,
)
from algorithms.randomised_local_search import RandomisedLocalSearch

__all__ = [
    "AntColony",
    "BruteForce",
    "Christofides",
    "TwoOpt",
    "ThreeOpt",
    "HeldKarp",
    "LinKernighan",
    "NearestNeighbour",
    "CheapestInsertion",
    "FarthestInsertion",
    "NearestInsertion",
    "RandomInsertion",
    "RandomisedLocalSearch",
]

ALGORITHMS = [
    ("Ant Colony", AntColony),
    ("Brute Force", BruteForce),
    ("Christofides", Christofides),
    ("2-Opt", TwoOpt),
    ("3-Opt", ThreeOpt),
    ("Held-Karp", HeldKarp),
    ("Lin-Kernighan", LinKernighan),
    ("Nearest Neighbour", NearestNeighbour),
    ("Cheapest Insertion", CheapestInsertion),
    ("Farthest Insertion", FarthestInsertion),
    ("Nearest Insertion", NearestInsertion),
    ("Random Insertion", RandomInsertion),
    ("Randomised Local Search", RandomisedLocalSearch),
]
