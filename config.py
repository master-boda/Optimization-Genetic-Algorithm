class GAConfig:
    def __init__(self):
        self.population_size = 100  # Número de indivíduos na população
        self.num_generations = 200  # Número de gerações
        self.crossover_rate = 0.8   # Probabilidade de cruzamento
        self.mutation_rate = 0.01   # Probabilidade de mutação
        self.tournament_size = 5    # Tamanho do torneio para seleção
        self.elitism = True         # Se deve usar elitismo
        self.elitism_size = 1       # Número de elites que passam direto para a próxima geração

# Exemplo de adição de parâmetros específicos do problema
        self.max_weight = 50        # Peso máximo para o problema da mochila, se aplicável
        self.problem_specific_parameter = 0.1  # Outro parâmetro específico do problema

