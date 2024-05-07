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


