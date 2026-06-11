from typing import List

class BlossomAlgo:
    def __init__(self, adjacency_matrix: List[List[int]]):
        """
        Initializes the Blossom algorithm with an adjacency matrix.

        Args:
            adjacency_matrix (List[List[int]]): The adjacency matrix representing the graph.
        """
        self.adjacency_matrix = adjacency_matrix

    def blossom(self, odd_vertices: List[int]) -> List[int]:
        """
        Finds a maximum matching in a graph using the Blossom algorithm.

        Args:
            odd_vertices (List[int]): List of odd-degree vertices in the graph.

        Returns:
            List[int]: List representing the matching where matching[i] = j indicates vertex i is matched with vertex j (-1 if unmatched).
        """
        n = self.adjacency_matrix.shape[0]  # Number of vertices
        unmatched = odd_vertices.copy()  # Copying odd vertices to keep track of unmatched ones

        matching = [-1] * n  # Initialize matching with all vertices unmatched

        blossoms = [-1] * n  # Initialize blossoms array to keep track of contracted vertices

        def find_augmenting_path(start: int) -> tuple[int, List[int]]:
            """
            Finds an augmenting path in the graph starting from the given vertex.

            Args:
                start (int): The starting vertex for the BFS.

            Returns:
                Tuple[int, List[int]]: Tuple containing the endpoint of the augmenting path and the parents of vertices in the path.
            """

            visited = [False] * n

            parent = [-1] * n

            queue = [start]

            while queue:
                u = queue.pop(0)

                visited[u] = True

                for v in range(n):
                    if self.adjacency_matrix[u][v] and not visited[v] and blossoms[u] != blossoms[v]:

                        if matching[v] == -1:
                            # Found an augmenting path
                            parent[v] = u

                            return v, parent

                        elif matching[v] != -1:
                            # Continue BFS
                            parent[v] = u

                            queue.append(matching[v])
                            visited[v] = True

            return -1, parent

        def contract_blossom(x: int, y: int, parent: List[int]):
            """
            Contracts a blossom in the graph.

            Args:
                x (int): One vertex of the blossom.
                y (int): Another vertex of the blossom.
                parent (List[int]): The parents of vertices in the blossom.
            """

            base = -1
            in_blossom = [False] * n

            while x != -1 or y != -1:

                if x != -1:
                    in_blossom[x] = True

                    if matching[x] == -1:
                        base = x

                    x = parent[x]

                if y != -1:
                    in_blossom[y] = True

                    if matching[y] == -1:
                        base = y

                    y = parent[y]

            for i in range(n):

                if in_blossom[i]:

                    blossoms[i] = base

        # Start finding augmenting paths and contracting blossoms
        for i in range(n):

            if unmatched[i] and matching[i] == -1:
                blossom_base = find_augmenting_path(i)[0]

                if blossom_base != -1:

                    contract_blossom(blossom_base, find_augmenting_path(blossom_base)[0], find_augmenting_path(blossom_base)[1])

        # Second pass to handle remaining unmatched vertices
        for i in range(n):

            if unmatched[i] and matching[i] == -1:

                blossom_base = find_augmenting_path(i)[0]

                if blossom_base != -1:
                    contract_blossom(blossom_base, find_augmenting_path(blossom_base)[0], find_augmenting_path(blossom_base)[1])

        # Assign unmatched vertices to augmenting paths
        for i in range(n):
            if unmatched[i]:

                matching[i] = find_augmenting_path(i)[0]

        return matching

# Algorithms used:
# - Breadth-First Search (BFS) is utilized to find augmenting paths in the graph.

# Data Structures used:
# - Adjacency Matrix: Represents the graph connections.
# - Lists: Used for storing odd-degree vertices, unmatched vertices, matching information, etc.
# - Queue: Employed in BFS to maintain the vertices to be visited.
# - Parent Array: Keeps track of the parent vertices during BFS.