import sys
import os
from utils.utils import fitness_function
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def two_opt(route: list[int], geo_matrix: list[list[float]], max_iterations: int = 5) -> list[int]:
    """
    Optimizes a given route using the 2-opt algorithm. This algorithm attempts to reduce the travel
    cost by iteratively reversing segments of the route. It is commonly used in solving routing problems
    such as the Traveling Salesman Problem (TSP).

    Parameters:
    - route (List[int]): The initial route as a list of node indices.
    - geo_matrix (List[List[float]]): A matrix representing the distances or costs between nodes.
    - max_iterations (int): The maximum number of iterations to run the optimization. Defaults to 2.

    Returns:
    - List[int]: The optimized route, potentially improved from the initial route if better configurations are found.

    Example Usage:
        route = [0, 1, 2, 3, 0]
        geo_matrix = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
        optimized_route = two_opt(route, geo_matrix, max_iterations=5)
    """
    best_route = route[:]
    improved = False
    iteration = 0

    while not improved and iteration < max_iterations:
        improved = False
        best_fit = fitness_function(best_route, geo_matrix)
        # keep endpoints fixed
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1:
                    continue  # dont need to swap adjacent elements
                new_route = best_route[:]
                # reverse the segment between i and j+1
                new_route[i:j + 1] = reversed(new_route[i:j + 1])
                new_fit = fitness_function(new_route, geo_matrix)
                if new_fit > best_fit:
                    best_route = new_route
                    best_fit = new_fit
                    improved = True
                    break
            if improved:
                break
        iteration += 1

    return best_route