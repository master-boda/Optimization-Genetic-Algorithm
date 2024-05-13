import random

def roulette_selection(population, fitnesses, maximize=True):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    
    if not maximize:
        selection_probs = [1 - p for p in selection_probs]
        
    return population[random.choices(range(len(population)), weights=selection_probs, k=1)[0]]

def tournament_selection(population, fitnesses, maximize=True, tournament_size=15):
    selected_indices = random.sample(range(len(population)), tournament_size)
    
    if maximize:
        best_index = max(selected_indices, key=lambda idx: fitnesses[idx])
    else:
        best_index = min(selected_indices, key=lambda idx: fitnesses[idx])
        
    return population[best_index]

def rank_selection(population, fitnesses, maximize=True):
    ranked_indices = sorted(range(len(population)), key=lambda idx: fitnesses[idx], reverse=maximize)
    rank_weights = [len(population) - rank for rank in range(len(population))]
    
    if not maximize:
        rank_weights = [1 / w for w in rank_weights]
        
    return population[random.choices(ranked_indices, weights=rank_weights, k=1)[0]]
