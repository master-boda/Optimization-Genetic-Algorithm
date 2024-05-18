import sys
import os
import random
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from operators.optimizations import *
from pop.population import *
from utils.utils import *
from visualizations.visualization import *
from visualizations.dashboard import run_dashboard

# Genetic Algorithm Function
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
       verbose=True,
       visualize=True,
       dashboard=True):
    # Initialize the population
    population = initializer(population_size)
    
    # Select the Geo matrix to use (original=True uses the original matrix from the project instructions)
    if matrix_to_use is None:
        matrix = geo_matrix_generator(seed=matrix_seed)
    else:
        matrix = np.array(matrix_to_use)
            
    # Compute fitness for each individual in the population
    fitnesses = [evaluator(ind, matrix) for ind in population]
    
    if verbose:
        print('RESULTS START')
        print("="*50)
        print(f"{'Initial Best Fitness:':<30} {max(fitnesses)}")
        print(f"{'Population Size:':<30} {population_size}")
        print(f"{'Number of Generations:':<30} {num_generations}")
        print(f"{'Geo Matrix:':<30}")
        print(matrix)
        print("="*50)
    
    routes_per_generation = []  # Store routes here
    fitness_per_generation = []  # Store fitness scores here
    
    for generation in range(num_generations):    
        if elitism:
            # Select the individuals to be carried over to the next generation
            sorted_indices = np.argsort(fitnesses)
            elite_indices = sorted_indices[-elitism_size:]
            offspring = [population[i] for i in elite_indices]
        else:
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
            current_best_fitness = max(fitnesses)
            best_individual = population[np.argmax(fitnesses)]
            print(f"\nGeneration {generation + 1:>3}")
            print("-" * 50)
            print(f"{'Best Fitness:':<20} {current_best_fitness}")
            print(f"{'Best Individual:':<20} {best_individual}")
            print("-" * 50)
        
        # Store the best route and fitness of this generation
        best_individual = population[np.argmax(fitnesses)]
        routes_per_generation.append(best_individual)
        fitness_per_generation.append(current_best_fitness)
    
    # Get the best individual and its fitness
    best_individual, best_fitness = population[np.argmax(fitnesses)], max(fitnesses)
    
    # Visualize the routes if the visualize parameter is True
    if visualize:
        visualize_routes(routes_per_generation, best_individual)
    
    if dashboard:
        print('INITIALIZING DASHBOARD....')
        return routes_per_generation, fitness_per_generation, best_individual, best_fitness, matrix
    
    return best_individual, best_fitness

# Example call to ga function with dashboard parameter
if __name__ == "__main__":
    result = ga(
        population,
        fitness_function,
        roulette_selection,
        order_crossover,
        inversion_mutation,
        dashboard=True
    )

    if isinstance(result, tuple) and len(result) == 5: #aqui para ver se corre o dash, visto que o output só tem len 5 se o coiso tiver True
        routes, fitnesses, best_route, best_fitness, matrix = result
        # Call the dashboard function with the GA results only if dashboard=True
        run_dashboard(routes, fitnesses, best_route, matrix)
