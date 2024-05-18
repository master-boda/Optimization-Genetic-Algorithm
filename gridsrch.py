import numpy as np
import sys
import os
import itertools
from multiprocessing import Pool
from main.genetic_algorithm import *
from pop.population import *
from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from operators.optimizations import *
from utils.utils import *
from tqdm import tqdm


def generate_matrix_gs(seed):
    np.random.seed(seed)
    matrix = geo_matrix_generator(seed=seed)
    return matrix

def evaluate_combinations(combo):
    try:
        seed, parameters = combo
        matrix = generate_matrix_gs(seed)
        best_individual, best_fitness = ga(**parameters, matrix_to_use=matrix, verbose=False)
        return (parameters, best_fitness)
    except Exception as e:
        print(f"Error in combination {parameters}: {e}")
        return (parameters, float('inf'))

def perform_grid_search(param_grid, n_seeds=15):
    seeds = [np.random.randint(1, 10000) for _ in range(n_seeds)]
    combinations = [dict(zip(param_grid.keys(), values)) for values in itertools.product(*param_grid.values())]
    
    # Prepare combination and seed pairs for grid search
    combos_with_seeds = [(seed, combo) for seed in seeds for combo in combinations]

    results = []
    with tqdm(total=len(combos_with_seeds)) as pbar, Pool() as pool:
        for i, combo in enumerate(combos_with_seeds):
            pbar.set_description(f"Running combination {i+1}/{len(combos_with_seeds)}")
            results.append(pool.apply_async(evaluate_combinations, (combo,)))
            pbar.update(1)
        with tqdm(total=len(results), desc="Gathering results") as pbar:
             for res in results:
                results.append(res.get())
                pbar.update(1)
        # Wait for all processes to finish and get the results
        
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

if __name__ == '__main__':
    param_grid = {
    'initializer': [population],
    'evaluator': [fitness_function],
    'population_size': [50, 100],
    'num_generations': [50, 100],
    'mutation_rate': [0.05],
    'crossover_rate': [0.8],
    'elitism_size': [2, 5],
    'selection': [tournament_selection, roulette_selection, rank_selection],
    'crossover': [partially_mapped_crossover, fast_order_mapped_crossover, order_crossover, cycle_crossover],
    'mutation': [simple_mutation, inversion_mutation, displacement_mutation],
}

    perform_grid_search(param_grid, n_seeds=15)
