from config import GAConfig
from optimization_problem import OptimizationProblem
import random

class GeneticAlgorithm:
    def __init__(self, config, problem):
        self.config = config
        self.problem = problem
        self.population = [self.problem.generate_random_solution() for _ in range(self.config.population_size)]

    def evolve(self):
        for _ in range(self.config.num_generations):
            self.population = self.select()
            self.crossover()
            self.mutate()
            if self.config.elitism:
                self.elitism()

    def select(self):
        # Implemente a seleção aqui (e.g., torneio)
        return self.population

    def crossover(self):
        # Implemente o cruzamento aqui
        pass

    def mutate(self):
        # Implemente a mutação aqui
        pass

    def elitism(self):
        # Implemente o elitismo aqui
        pass

    def run(self):
        self.evolve()
        best_solution = min(self.population, key=self.problem.fitness)
        return best_solution
