import numpy as np
import time
import sys
import queue
from typing import List, Tuple

if __name__ == '__main__': # conditional import when running standalone
    from blossom import BlossomAlgo
else:
    from algorithms.blossom import BlossomAlgo

logfile = open('logfile2.txt', 'a')
def custom_print(*args, **kwargs):
    output = ' '.join(map(str, args))
    sys.stdout.write(output + '\n')
    logfile.write(output + '\n')
    logfile.flush()

built_in_print = print
print = custom_print

sys.setrecursionlimit(10000) # DFS in find_eulerian_circuit can go very deep on large graphs

class Christofides:

    def __init__(self, adjacency_matrix: List[List[int]]):

        """
        Initializes the Christofides algorithm with an adjacency matrix.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.

        """

        self.adjacency_matrix = adjacency_matrix

    def solve(self, start_node: int) -> Tuple[List[int], float, float]:

        """
        Solves the TSP using the Christofides algorithm.

        Args:
            start_node (int): The starting node for the tour.

        Returns:
            Tuple[List[int], float, float]: Tuple containing the optimized tour, its total weighting, and the execution time.
        """

        start_time = time.time()

        n = self.adjacency_matrix.shape[0]

        # Step 1: Create a minimum spanning tree
        mst = self.minimum_spanning_tree()

        # Step 2: Find the odd-degree vertices in the MST
        odd_vertices = self.find_odd_vertices(mst)

        # Step 3: Find a minimum weight perfect matching in the subgraph induced by odd-degree vertices
        g = BlossomAlgo(self.adjacency_matrix)

        perfect_matching = g.blossom(odd_vertices)

        # Step 4: Combine the MST and the perfect matching to form a multigraph
        multigraph = self.combine_multigraph(mst, perfect_matching)

        # Step 5: Find an Eulerian circuit in the multigraph
        eulerian_circuit = self.find_eulerian_circuit(multigraph, start_node) #

        # Step 6: Create a tour from the Eulerian circuit
        tour = self.create_tour(eulerian_circuit, start_node)

        # Calculate the total weighting
        total_weighting = self.calculate_total_weighting(tour)

        end_time = time.time()

        execution_time = end_time - start_time

        return tour, total_weighting, execution_time

    def calculate_total_weighting(self, tour: List[int]) -> float:

        """
        Calculates the total weighting of a tour.

        Args:
            tour (List[int]): The tour represented as a list of nodes.

        Returns:
            float: The total weighting of the tour.
        """

        total_weighting = 0

        for i in range(len(tour) - 1):
            total_weighting += self.adjacency_matrix[tour[i]][tour[i + 1]]

        total_weighting += self.adjacency_matrix[tour[-1]][tour[0]]  # Return to the starting node

        return total_weighting

    def minimum_spanning_tree(self) -> List[List[int]]:
        """
        Creates a minimum spanning tree from the graph using Prims algorithm.

        Returns:
            List[List[int]]: The minimum spanning tree represented as an adjacency matrix.
        """
        n = self.adjacency_matrix.shape[0]

        mst = np.zeros_like(self.adjacency_matrix)
        visited = np.zeros(n, dtype=bool)

        visited[0] = True

        pq = queue.PriorityQueue()

        for i in range(n):
            if self.adjacency_matrix[0][i] > 0:
                pq.put((self.adjacency_matrix[0][i], 0, i))

        while not pq.empty():

            weight, src, dest = pq.get()

            if not visited[dest]:
                mst[src][dest] = mst[dest][src] = weight
                visited[dest] = True

                for i in range(n):
                    if not visited[i] and self.adjacency_matrix[dest][i] > 0:
                        pq.put((self.adjacency_matrix[dest][i], dest, i))

        return mst

    def find_odd_vertices(self, mst: List[List[int]]) -> List[bool]:
        """
        Finds the odd-degree vertices in the minimum spanning tree.

        Args:
            mst (List[List[int]]): The minimum spanning tree represented as an adjacency matrix.

        Returns:
            List[bool]: A boolean list indicating odd-degree vertices.
        """

        return np.sum(mst, axis=1) % 2 == 1

    def combine_multigraph(self, mst: List[List[int]], perfect_matching: List[int]) -> List[List[int]]:
        """
        Combines the MST and the perfect matching to form a multigraph.

        Args:
            mst (List[List[int]]): The minimum spanning tree represented as an adjacency matrix.
            perfect_matching (List[int]): The perfect matching represented as a list of matched vertices.

        Returns:
            List[List[int]]: The multigraph represented as an adjacency matrix.
        """

        multigraph = mst.copy()

        for i in range(len(perfect_matching)):
            if perfect_matching[i] != -1:

                multigraph[i][perfect_matching[i]] = multigraph[perfect_matching[i]][i] = 0

        return multigraph

    def find_eulerian_circuit(self, multigraph: List[List[int]], start_node: int ) -> List[int]:
        """
        Finds an Eulerian circuit in the multigraph.

        Args:
            multigraph (List[List[int]]): The multigraph represented as an adjacency matrix.
            start_node (int): The starting node for the circuit.

        Returns:
            List[int]: The Eulerian circuit represented as a list of nodes.
        """

        n = len(multigraph)
        n = multigraph.shape[0]
        circuit = []

        def dfs(start_node: int, multigraph: List[List[int]]):
            stack = [start_node]
            while stack:
                current_node = stack[-1]
                found = False
                for i in range(n):
                    if multigraph[current_node][i] > 0:
                        multigraph[current_node][i] -= 1
                        multigraph[i][current_node] -= 1
                        stack.append(i)
                        found = True
                        break
                if not found:
                    circuit.append(stack.pop())

        dfs(start_node, multigraph.copy())  # Pass a copy of the multigraph

        return circuit[::-1]  # Reverse the circuit to get the correct order

    def create_tour(self, eulerian_circuit: List[int], start_node: int) -> List[int]:
        """
        Creates a tour from the Eulerian circuit.

        Args:
            eulerian_circuit (List[int]): The Eulerian circuit represented as a list of nodes.
            start_node (int): The starting node for the tour.

        Returns:
            List[int]: The tour represented as a list of nodes.
        """

        tour = [start_node]

        visited = np.zeros(len(eulerian_circuit), dtype=bool)

        visited[start_node] = True

        for node in eulerian_circuit:
            if not visited[node]:
                tour.append(node)
                visited[node] = True
                print(f"Current Tour: {tour}")
        tour.append(start_node)  # Close the tour by returning to the starting node

        return tour

