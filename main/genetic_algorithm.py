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
from visualizations.dashboard import *


def ga(initializer=population,
       evaluator=fitness_function,
       selection=tournament_selection,
       crossover=order_crossover,
       mutation=swap_mutation,
       mutation_rate=0.1,
       population_size=100,
       num_generations=50,
       crossover_rate=0.7,
       elitism_size=2,
       elitism=True,
       matrix_to_use=None,
       matrix_seed=None,
       verbose=True,
       visualize=True,
       dashboard=True,
       fitness_sharing=True):
    """
    This algorithm simulates natural selection by evolving a population of candidate solutions
    through selection, crossover, and mutation. Over successive generations, it selects the fittest
    individuals, combines them to produce offspring, and introduces mutations to maintain diversity,
    aiming to find the best solution.

    Parameters:
    - initializer (function): Function to initialize the population.
    - evaluator (function): Function to evaluate the fitness of individuals.
    - selection (function): Function to select individuals for crossover.
    - crossover (function): Function to perform crossover between individuals.
    - mutation (function): Function to mutate individuals.
    - matrix_to_use (list of lists, optional): Predefined Geo matrix to use.
    - matrix_seed (int, optional): Seed for Geo matrix generation.
    - mutation_rate (float): Probability of mutation.
    - population_size (int): Number of individuals in the population.
    - num_generations (int): Number of generations to run the algorithm.
    - crossover_rate (float): Probability of crossover.
    - elitism_size (int): Number of top individuals to carry over to the next generation.
    - elitism (bool): Whether to use elitism.
    - verbose (bool): Whether to print verbose output.
    - visualize (bool): Whether to visualize the routes.
    - dashboard (bool): Whether to run the dashboard.
    - fitness_sharing (bool): Whether to use fitness sharing.

    Returns:
    - tuple: Contains routes per generation, fitness per generation, best individual, best fitness, and Geo matrix if dashboard is True.
    - tuple: Contains best individual and best fitness if dashboard is False.

    Example Usage: 
    if __name__ == "__main__":
        result = ga(
            population,
            fitness_function,
            roulette_selection,
            order_crossover,
            inversion_mutation,
            dashboard=True)

        if isinstance(result, tuple) and len(result) == 5: #to generate dashboard
            routes, fitnesses, best_route, best_fitness, matrix = result
            run_dashboard(routes, fitnesses, best_route, matrix)
    """
    # Initialize the population
    population = initializer(population_size)
    
    # Select the Geo matrix to use (original=True uses the original matrix from the project instructions)
    if matrix_to_use is None:
        matrix = geo_matrix_generator(seed=matrix_seed)
    else:
        matrix = np.array(matrix_to_use)
    
    # Compute fitness for each individual in the population
    fitness_results = [evaluator(ind, matrix) for ind in population]
    fitnesses = [result[0] for result in fitness_results]
    jumped_ks_flags = [result[1] for result in fitness_results]
    
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
        fitness_results = [evaluator(ind, matrix) for ind in population]
        fitnesses = [result[0] for result in fitness_results]
        jumped_ks_flags = [result[1] for result in fitness_results]
     
        if generation < num_generations - 1 and fitness_sharing:
            fitnesses = fitness_shared(population, fitnesses)
            
        current_best_fitness = max(fitnesses)
        phenotypic_diversity = np.std(fitnesses)
        genotypic_diversity_value = genotypic_diversity(population)
            
        if verbose:
            print(f"{'-'*40}")
            print(f'Generation {generation} best fitness {"(lowered due to sharing)" if fitness_sharing==True and generation<(num_generations-1) else ""}: {current_best_fitness}')
            print(f"{'-'*40}")
            print(f'Best individual: {population[np.argmax(fitnesses)]}')
            print(f"Phenotypic Diversity: {phenotypic_diversity:.2f}")
            print(f"Genotypic Diversity: {genotypic_diversity_value:.2f}")
            print(f"{'-'*40}\n")

        best_individual = population[np.argmax(fitnesses)]
        routes_per_generation.append(best_individual)
        fitness_per_generation.append(current_best_fitness)
    
    # Get the best individual and its fitness
    best_individual, best_fitness = population[np.argmax(fitnesses)], max(fitnesses)
    
    # Check if the best individual jumped KS
    jumped_ks = jumped_ks_flags[np.argmax(fitnesses)]
    
    # Print the jump status
    if verbose:
        if jumped_ks:
            print(f"The best individual in the last generation jumped KS.")
        else:
            print(f"The best individual in the last generation did not jump KS.")
    
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

    if isinstance(result, tuple) and len(result) == 5:
        routes, fitnesses, best_route, best_fitness, matrix = result
        # Call the dashboard function with the GA results only if dashboard=True
        run_dashboard(routes, fitnesses, best_route, matrix)

