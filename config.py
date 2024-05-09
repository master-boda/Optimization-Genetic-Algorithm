class GAConfig:
    def __init__(self, population_size=100, num_generations=50, mutation_rate=0.01, crossover_rate=0.7, elitism=True, elitism_size=2):
        """
        Initializes the configuration for a genetic algorithm.

        Parameters:
        population_size (int): Number of individuals in the population.
        num_generations (int): Number of generations to evolve the population.
        mutation_rate (float): Probability of mutating an individual.
        crossover_rate (float): Probability of crossing over parents to produce offspring.
        elitism (bool): Whether to carry the best individuals to the next generation without changes.
        elitism_size (int): Number of top individuals to carry over if elitism is True.
        """
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism #nao faz sentido, devia era ser parametro para trocarmos pa true ou false, n devoa tar aqui
        self.elitism_size = elitism_size

    def __repr__(self):
        return (f"GAConfig(population_size={self.population_size}, num_generations={self.num_generations}, "
                f"mutation_rate={self.mutation_rate}, crossover_rate={self.crossover_rate}, "
                f"elitism={self.elitism}, elitism_size={self.elitism_size})")
