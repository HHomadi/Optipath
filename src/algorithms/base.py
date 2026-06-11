"""
Common interface for all TSP algorithms.
Every solver returns (tour, length, time) from solve(start_node).
"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class TspSolver(ABC):
    """Base class for TSP solvers. All return (tour, length, execution_time)."""

    @abstractmethod
    def solve(self, start_node: int) -> Tuple[List[int], float, float]:
        """
        Run the algorithm from start_node.
        Returns (tour as list of node indices, tour length, execution time in seconds).
        """
        pass
