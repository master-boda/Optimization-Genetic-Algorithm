class GAConfig:
    def __init__(self):
        self.population_size = 100
        self.num_generations = 50
        self.crossover_rate = 0.8
        self.mutation_rate = 0.05
        self.elitism = True
        self.elitism_size = 2
        self.selection = None
        self.crossover = None
        self.mutation = None
        self.evaluator = None

        