import random

def crossover(parent1, parent2, crossover_rate=0.8):
    """ Realiza o cruzamento entre dois pais para produzir dois filhos. """
    if random.random() < crossover_rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    else:
        # Sem cruzamento, os filhos são cópias exatas dos pais
        return parent1, parent2

def mutate(individual, mutation_rate=0.05):
    """ Aplica mutação aleatória em um indivíduo com uma dada taxa de mutação. """
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(min(individual), max(individual))
    return individual

def tournament_selection(population, fitness_func, tournament_size=3):
    """ Seleciona um indivíduo usando seleção por torneio. """
    tournament = random.sample(population, tournament_size)
    fittest_individual = min(tournament, key=fitness_func)
    return fittest_individual
