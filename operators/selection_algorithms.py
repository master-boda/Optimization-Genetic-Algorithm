import random

def roulette_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
        
    return population[random.choices(range(len(population)), weights=selection_probs, k=1)[0]]

def tournament_selection(population, fitnesses, tournament_size=15):
    selected_indices = random.sample(range(len(population)), tournament_size)
    best_index = max(selected_indices, key=lambda idx: fitnesses[idx])
        
    return population[best_index]

def rank_selection(population, fitnesses):
    ranked_indices = sorted(range(len(population)), key=lambda idx: fitnesses[idx], reverse=True)
    rank_weights = [len(population) - rank for rank in range(len(population))]
        
    return population[random.choices(ranked_indices, weights=rank_weights, k=1)[0]]
