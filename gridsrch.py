import random
import numpy as np
import sys
import os
from copy import deepcopy
import random
import csv
import time
import gc
import multiprocessing

from itertools import product, chain
import statistics as stat
from typing import Callable, Dict, List, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.genetic_algorithm import *
from pop.population import *
from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from operators.optimizations import *
from utils.utils import *

def run_algorithm(args):
    """Runs an algorithm with the given parameters and returns the best fitness value.

    Args:
        args (tuple): A tuple containing the algorithm function and its parameters.

    Returns:
        float: The best fitness value obtained from the algorithm.
    """
    algorithm, params = args
    try:
        _, _, _, best_fit = algorithm(**params)
        return best_fit
    except Exception as e:
        print(f"Error in run_algorithm: {str(e)}")
        return -1

def grid_search(ga_variation: Callable, num_runs: int, parameter_options: Dict[str, List[Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Explore various parameter combinations to optimize the performance of a genetic algorithm.

    Args:
        ga_variation (Callable): The genetic algorithm variation to be optimized.
        num_runs (int): The number of iterations to be executed for each parameter combination.
        parameter_options (Dict[str, List[Any]]): A dictionary specifying the parameter names as keys
                                                   and a list of potential values for each parameter.

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

        # Find the combinations with the best metrics
        results = pool.map(run_algorithm, [(ga_variation, params)] * num_runs)
        final_fits = results

        # Calculate metrics only if there are valid fitness values
        if -1 in final_fits:
            print(f'Invalid combination in: {combination}')
            avg_fit.append(999)  # Assign 999 as a placeholder
            avg_std.append(999)  # Assign 999 as a placeholder
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
    result = grid_search(ga, 20, {
        'initializer': [population],
        'evaluator': [fitness_function],
        'selection': [rank_selection, tournament_selection, rank_selection],
        'crossover': [fast_ordered_mapped_crossover, ordered_crossover, partially_mapped_crossover],
        'mutation': [simple_mutation, scramble_mutation, displacement_mutation],
        #'crossover_rate': [0.5, 0.8, 0.9],
        #'mutation_rate': [0.01, 0.05, 0.1, 0.2],
        #'elitism_size': [0, 1, 2, 5],
        #'verbose': [False],
        #'maximise': [True],
    })

    print(result)
