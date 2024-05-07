import random
import numpy as np
from config import GAConfig
from utils import geo_matrix

# expected parameters:
# initializer:  population(number)
# evaluator:    fitness_function(route, geo_matrix)
# crossover:    crossover(p1, p2) -> c1, c2, ect.
# mutation:     mutate(individual) -> individual
# selection:    selection(population, fitnesses)

def Genetic_Algorithm(initializer, evaluator, crossover, mutation, selection, config=GAConfig, og_matrix=False, maximize=True, verbose=True):
    # Initialize the population
    population = initializer(config.population_size)

    # Select the geo matrix to derive fitnesses from
    matrix = geo_matrix(og_matrix)
    
    # Precompute fitnesses
    fitnesses = [evaluator(ind, matrix) for ind in population]
    
    if verbose:
        print(f'Initial best fitness: {max(fitnesses) if maximize else min(fitnesses)}') 
    
    for generation in range(config.num_generations):   
        
        if config.elitism:
            # Keep the best individuals
            sorted_indices = np.argsort(fitnesses)
            sorted_indices = sorted_indices if maximize else sorted_indices[::-1]
            
            elite_indices = sorted_indices[-config.elitism_size:]
            
            offspring = [population[i] for i in elite_indices]
            
        else :
            offspring = []
            
        while len(offspring) < config.population_size:
            
            p1 = selection(population, fitnesses)
            p2 = selection(population, fitnesses)
            
            if random.random() < config.crossover_rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1, p2
                
            c1 = mutation(c1, config.mutation_rate)
            c2 = mutation(c2, config.mutation_rate)
            
            offspring.extend([c1, c2])
            
        offspring = offspring[:config.population_size]
        population = offspring
        fitnesses = [evaluator(ind, matrix) for ind in population]
        
        current_best_fitness = max(fitnesses) if maximize else min(fitnesses)
        print(f'Generation {generation} best fitness: {current_best_fitness}')
            
    return population[np.argmin(fitnesses)], min(fitnesses)