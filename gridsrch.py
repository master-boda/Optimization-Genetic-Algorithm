import random
import numpy as np
import sys
import os
from copy import deepcopy
import gc
import multiprocessing

from itertools import product
import statistics as stat
from typing import Callable, Dict, List, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import genetic_algorithm as ga
from pop import population as pop
from operators import selection_algorithms as sel
from operators import crossovers as cross
from operators import mutators as mut
from operators import optimizations as opt
from utils import utils

def run_algorithm(args):
    """Runs an algorithm with the given parameters and returns the best fitness value.

    Args:
        args (tuple): A tuple containing the algorithm function, its parameters, and the geo_matrix.

    Returns:
        float: The best fitness value obtained from the algorithm.
    """
    algorithm, params, geo_matrix = args
    try:
        # Execute the algorithm
        result = algorithm(**params)
        
        # Ensure the result has the expected structure
        if isinstance(result, tuple) and len(result) == 4:
            _, _, best_solution, best_fitness = result
            best_fitness = utils.fitness_function(best_solution, geo_matrix)
            return best_fitness
        else:
            raise ValueError("Algorithm did not return the expected result structure")
    except Exception as e:
        print(f"Error in run_algorithm: {str(e)}")
        return -1

def grid_search(ga_variation: Callable, num_runs: int, parameter_options: Dict[str, List[Any]], geo_matrix: List[List[int]]) -> Dict[str, Dict[str, Any]]:
    """
    Explore various parameter combinations to optimize the performance of a genetic algorithm.

    Args:
        ga_variation (Callable): The genetic algorithm variation to be optimized.
        num_runs (int): The number of iterations to be executed for each parameter combination.
        parameter_options (Dict[str, List[Any]]): A dictionary specifying the parameter names as keys
                                                   and a list of potential values for each parameter.
        geo_matrix (List[List[int]]): The Geo matrix to be used for the fitness calculation.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary containing the search results, including the combination
                                   with the highest average fitness and the most consistent results.
                                   Each result entry includes the model parameters, average fitness,
                                   and standard deviation.
    """
    # Use multiprocessing to improve efficiency
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Prepare the combinations to be tested
    keys = parameter_options.keys()
    values = parameter_options.values()
    combinations = list(product(*values))

    # Initialize lists for storing metrics
    model_combs = []
    avg_fit = []
    avg_std = []

    print(f"There are {len(combinations)} possible combinations...\nStarted!")

    for i, combination in enumerate(combinations):
        # Prepare the parameter dictionary for the combination
        params = dict(zip(keys, combination))
        model_combs.append(params)

        # Prepare the arguments for the run_algorithm function
        run_args = [(ga_variation, params, geo_matrix)] * num_runs

        # Find the combinations with the best metrics
        results = pool.map(run_algorithm, run_args)
        final_fits = results

        # Calculate metrics only if there are valid fitness values
        if -1 in final_fits or not final_fits:
            print(f'Invalid combination in: {combination}')
            avg_fit.append(float('inf'))  # Use infinity as a placeholder for invalid combinations
            avg_std.append(float('inf'))  # Use infinity as a placeholder for invalid combinations
        else:
            avg_fit.append(stat.mean(final_fits))
            avg_std.append(stat.stdev(final_fits))

        # Clear memory
        del final_fits, results
        gc.collect()

        if i % 10 == 0:
            print(f'{i} combinations were completed as of now!')

    print('Combinations concluded! ')
    print('The results shall be displayed...')

    pool.close()
    pool.join()

    fittest_idx = avg_fit.index(min(avg_fit))
    consistent_idx = avg_std.index(min(avg_std))

    results = {
        'Fittest': {
            'model_parameters': model_combs[fittest_idx],
            'avg_fit': avg_fit[fittest_idx],
            'std': avg_std[fittest_idx]
        },
        'Most consistent': {
            'model_parameters': model_combs[consistent_idx],
            'avg_fit': avg_fit[consistent_idx],
            'std': avg_std[consistent_idx]
        }
    }

    return results

if __name__ == '__main__':
    # Generate the Geo matrix using the geo_matrix_generator
    geo_matrix = utils.geo_matrix_generator(min_value=-500, max_value=500, size=10)
    
    result = grid_search(ga.ga, 20, {
        'initializer': [pop.population],
        'evaluator': [utils.fitness_function],
        'selection': [sel.rank_selection, sel.tournament_selection],
        'crossover': [cross.fast_ordered_mapped_crossover, cross.ordered_crossover, cross.partially_mapped_crossover],
        'mutation': [mut.simple_mutation, mut.scramble_mutation, mut.displacement_mutation],
        'crossover_rate': [0.5],
        'mutation_rate': [0.05],
        'elitism_size': [2],
        'verbose': [False],
        'maximize': [True],
    }, geo_matrix)

    print(result)
