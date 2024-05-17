import random
import numpy as np

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from operators.optimizations import *
from pop.population import *
from utils.utils import *

def ga(initializer,
    evaluator,
    selection,
    crossover,
    mutation,
    matrix_to_use=None,
    matrix_seed=None,
    mutation_rate=0.05,
    population_size=200,
    num_generations=50,
    crossover_rate=0.8,
    elitism_size=2,
    elitism=True,
    og_matrix=False,
    maximize=True,
    verbose=True):    
    # initialize the population
    population = initializer(population_size)
    
    # select the Geo matrix to use (original=True uses the original matrix from the project instructions)
    if matrix_to_use is None:
        matrix = geo_matrix_generator(seed=matrix_seed)
    else:
        matrix = np.array(matrix_to_use)
            
    # compute fitness for each individual in the population
    fitnesses = [evaluator(ind, matrix) for ind in population]
    
    if verbose:
     print(f'Initial best fitness: {max(fitnesses) if maximize else min(fitnesses)}') 
     print(f'Population size: {population_size}')
     print(f'Number of generations: {num_generations}')
     print(f'Geo matrix {"(original)" if og_matrix==True else ""}: {matrix}')
    
    for generation in range(num_generations):    
     if elitism:
         # select the individuals to be carried over to the next generation
         sorted_indices = np.argsort(fitnesses)
         sorted_indices = sorted_indices if maximize else sorted_indices[::-1]
         
         elite_indices = sorted_indices[-elitism_size:]
         
         offspring = [population[i] for i in elite_indices]

     else :
         offspring = []
         
     while len(offspring) < population_size:
         
         p1 = selection(population, fitnesses)
         p2 = selection(population, fitnesses)
         
         if random.random() < crossover_rate:
          c1, c2 = crossover(p1, p2)
         else:
          c1, c2 = p1, p2
          
         c1 = mutation(c1, mutation_rate)
         c2 = mutation(c2, mutation_rate)
         
         c1 = two_opt(c1, matrix)
         c2 = two_opt(c2, matrix)
         
         offspring.extend([c1, c2])
         
     population = offspring[:population_size]
     fitnesses = [evaluator(ind, matrix) for ind in population]
          
     if verbose:
        current_best_fitness = max(fitnesses) if maximize else min(fitnesses)
        best_individual = population[np.argmax(fitnesses)]
        phenotypic_diversity = np.std(fitnesses)
        genotypic_diversity_value = genotypic_diversity(population)
    
        print(f"{'-'*40}")
        print(f"Generation {generation}")
        print(f"{'-'*40}")
        print(f"Best Fitness: {current_best_fitness}")
        print(f"Best Individual: {best_individual}")
        print(f"Phenotypic Diversity: {phenotypic_diversity:.2f}")
        print(f"Genotypic Diversity: {genotypic_diversity_value:.2f}")
        print(f"{'-'*40}\n")
    return population[np.argmax(fitnesses)], max(fitnesses)

ga(population, fitness_function, roulette_selection, partially_mapped_crossover, simple_mutation)