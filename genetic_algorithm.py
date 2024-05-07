import random
import numpy as np
from config import GAConfig
from utils import geo_matrix
from population import population
from utils import fitness_function
from operators import crossover
from operators import mutate

def ga(initializer, evaluator, selection, crossover, mutation, og_matrix=False, maximize=True, verbose=True):
    config = GAConfig()
    
    # initialize the population
    population = initializer(config.population_size)
    
    # select the Geo matrix to use (original=True uses the original matrix from the project instructions)
    matrix = geo_matrix(original=og_matrix)
    
    # compute fitness for each individual in the population
    fitnesses = [evaluator(ind, matrix) for ind in population]
    
    if verbose:
        print(f'Initial best fitness: {max(fitnesses) if maximize else min(fitnesses)}') 
        print(f'Population size: {config.population_size}')
        print(f'Number of generations: {config.num_generations}')
        print(f'Geo matrix {"(original)" if og_matrix==True else ""}: {matrix.head(15)}')
    
    for generation in range(config.num_generations):   
        
        if config.elitism:
            # select the individuals to be carried over to the next generation
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
            
        population = offspring[:config.population_size]
        fitnesses = [evaluator(ind, matrix) for ind in population]
                
        if verbose:
            current_best_fitness = max(fitnesses) if maximize else min(fitnesses)
            print(f'Generation {generation} best fitness: {current_best_fitness}')
            
    return population[np.argmin(fitnesses)], min(fitnesses)


# expected parameters:
# initializer:  population(number)
# evaluator:    fitness_function(route, geo_matrix)
# crossover:    crossover(p1, p2) -> c1, c2, ect.
# mutation:     mutate(individual) -> individual
# selection:    selection(population, fitnesses)