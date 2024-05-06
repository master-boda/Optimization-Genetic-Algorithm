import random
import numpy as np
from config import GAConfig

def Genetic_Algorithm(initializer, evaluator, crossover, mutation, selection, config: GAConfig, maximize=True, verbose=True):
    # Initialize the population
    population = initializer(config.population_size)

    # Precompute fitnesses
    fitnesses = [evaluator(ind) for ind in population]
    
    if verbose:
        print(f'Initial best fitness: {max(fitnesses)}') 
        
    for generation in range(config.generations):   
        if config.elitism:
            # Keep the best individuals
            elite = [population[i] for i in np.argsort(fitnesses)[-config.elitism_size:]]
            
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
        
        population = elite + offspring 
        fitness = evaluator(population)
        
        if verbose:
            print(f'Generation {generation} best fitness: {max(fitness)}')
            
        return population[np.argmin(fitnesses)], min(fitnesses)
                
            
        
    
    