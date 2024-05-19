import numpy as np
import itertools
from multiprocessing import Pool, Manager
from tqdm import tqdm
from main.genetic_algorithm import ga
from pop.population import population
from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from utils.utils import *
import csv

def generate_matrix_gs(seed):
    """
    Generate a Geo matrix with a given seed.

    Parameters:
        - seed (int): The seed value for random number generation.

    Returns:
        - list of lists: The generated Geo matrix.

    Example Usage:
        matrix = generate_matrix_gs(42)
    """
    np.random.seed(seed)
    matrix = geo_matrix_generator(seed=seed)
    return matrix

def evaluate_combination(combo):
    """
    Evaluate a combination of genetic algorithm parameters using a specific seed.

    Parameters:
        - combo (tuple): A tuple containing a seed and a dictionary of parameters.

    Returns:
        - tuple: A tuple containing the parameters and the best fitness achieved.
    
    Example Usage:
        combo = (42, {'population_size': 50, 'num_generations': 50, 'mutation_rate': 0.05})
        evaluate_combination(combo)
    """
    seed, parameters = combo
    try:
        matrix = generate_matrix_gs(seed)
        best_individual, best_fitness = ga(**parameters, matrix_to_use=matrix, verbose=False, dashboard=False, visualize=False, fitness_sharing=True)
        return (parameters, best_fitness)
    except Exception as e:
        print(f"Error in combination {parameters}: {e}")
        return (parameters, float('inf'))

def perform_grid_search(param_grid, n_seeds=15):
    """
    Perform a grid search over the specified parameter grid using multiple seeds.

    Parameters:
        - param_grid (dict): A dictionary specifying the parameter grid for the grid search.
        - n_seeds (int): The number of seeds to use for random number generation.

    Returns:
        - None: Prints the best parameter combination and its average fitness.

    Example Usage:
        param_grid = {
            'population_size': [50, 100],
            'num_generations': [50, 100],
            'mutation_rate': [0.05, 0.1],
        }
        perform_grid_search(param_grid, n_seeds=15)
    """
    seeds = [np.random.randint(1, 10000) for _ in range(n_seeds)]
    combinations = [dict(zip(param_grid.keys(), values)) for values in itertools.product(*param_grid.values())]
    
    # Prepare combination and seed pairs for grid search
    combos_with_seeds = [(seed, combo) for seed in seeds for combo in combinations]

    with Pool() as pool, Manager() as manager:
        results = manager.list()
        with tqdm(total=len(combos_with_seeds)) as pbar:
            for result in pool.imap_unordered(evaluate_combination, combos_with_seeds):
                results.append(result)
                pbar.update(1)

        # Aggregate results
        combination_scores = {}
        for (parameters, fitness) in results:
            combo_key = tuple(sorted(parameters.items()))  # Create a hashable representation of the dictionary
            if combo_key not in combination_scores:
                combination_scores[combo_key] = []
            combination_scores[combo_key].append(fitness)

        # Calculate average fitness for each combination
        average_scores = {combo: np.mean(scores) for combo, scores in combination_scores.items()}

        # Find the combination with the highest average fitness
        best_combo = max(average_scores, key=average_scores.get)
        print("Overall best combination:", dict(best_combo))
        print("Average fitness:", average_scores[best_combo])

        # Export results to CSV file
        with open('grid_search_results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Parameters', 'Average Fitness'])
            for combo, score in average_scores.items():
                writer.writerow([str(combo), score])

if __name__ == '__main__':
    # Define the parameter grid for the grid search
    param_grid = {
        'initializer': [population],
        'evaluator': [fitness_function],
        'population_size': [50, 100],
        'num_generations': [50, 100],
        'mutation_rate': [0.05, 0.1],
        'crossover_rate': [0.7, 0.9],
        'elitism_size': [2, 5],
        'selection': [tournament_selection, roulette_selection, rank_selection],
        'crossover': [partially_mapped_crossover, fast_order_mapped_crossover, order_crossover, cycle_crossover],
        'mutation': [swap_mutation, displacement_mutation, inversion_mutation],
    }

    perform_grid_search(param_grid, n_seeds=15)
