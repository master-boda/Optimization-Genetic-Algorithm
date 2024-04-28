import random

class OptimizationProblem:
    def __init__(self, objective_function):
        self.objective_function = objective_function

    def fitness(self, solution):
        return -self.objective_function(solution)  # Suponha minimização

    def generate_random_solution(self):
        solution = [random.randint(0, 100) for _ in range(10)]
        return solution

