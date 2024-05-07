import random 

def mutate(individual, mutation_rate=0.05):
    """ Aplica mutação aleatória em um indivíduo com uma dada taxa de mutação. """
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(min(individual), max(individual))
    return individual
