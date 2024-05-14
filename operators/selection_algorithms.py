import random


def roulette_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    return random.choices(population, weights = selection_probs)[0]


def tournament_selection(population, fitnesses):
    selected_individuals = random.choices(population, k=random.randint(3, 6))
    best_individual = max(selected_individuals, key=lambda ind: fitnesses[population.index(ind)])        
    return best_individual



def rank_selection(population, fitnesses):
    ranked_indices = sorted(range(len(population)), key=lambda idx: fitnesses[idx], reverse=True)
    rank_weights = [len(population) - rank+1 for rank in range(len(population))]
    return population[random.choices(ranked_indices, weights=rank_weights, k=1)[0]]

