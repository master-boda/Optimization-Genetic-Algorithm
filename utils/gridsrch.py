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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from main.genetic_algorithm import *
from pop.population import *
from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from operators.optimizations import *
from utils.utils import *

def grid_search( num_runs: int, parameter_options: dict[str, list[any]]) -> dict[
    str, dict[str, any]]:
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
    # Multiprocess to improve efficiency
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Prepare the combinations to be tested
    keys = parameter_options.keys()
    values = parameter_options.values()
    combinations = list(product(*values))

    # Initialise lists for storing metrics
    model_combs = []
    avg_fit = []
    avg_std = []

    print(f"There are {len(combinations)} possible combinations...\nStarted!")

    i = 0
    for combination in combinations:
        # Prepare the parameter dictionary for the combination
        params = dict(zip(keys, combination))
        model_combs.append(params)

        # Initialise lists for metrics of each iteration
        final_fits = []

        # Find the combinations with the best metrics
        results = pool.map(run_algorithm, [(ga_variation, params)] * num_runs)
        final_fits = results

        # Calculate metrics only if there are valid fitness values
        if -1 in final_fits:
            print('Invalid combination in:', combination)
            avg_fit.append(999)  # Assign 999 as a placeholder
            avg_std.append(999)  # Assign 999 as a placeholder

        else:
            avg_fit.append(stat.mean(final_fits))
            avg_std.append(stat.stdev(final_fits))

        # Clear memory
        del final_fits, results

        if i % 10 == 0:
            print(f'{i} combinations were completed as of now!')

        i += 1

    print('Combinations concluded! ')
    print('The results shall be displayed...')

    fittest = model_combs[avg_fit.index(min(avg_fit))]
    consistent = model_combs[avg_std.index(min(avg_std))]

    results = {'Fittest': {'model_parameters': fittest,
                           'avg_fit': avg_fit[model_combs.index(fittest)],
                           'std': avg_std[model_combs.index(fittest)]},
               'Most consistent': {'model_parameters': consistent,
                                   'avg_fit': avg_fit[model_combs.index(consistent)],
                                   'std': avg_std[model_combs.index(consistent)]}}

    return results


if __name__ == '__main__':
    result = grid_search(ga, 20, {'create_population': [population],
                                         'pop_size': [50, 100, 500],
                                         'selector': [rank_selection, tournament_selection,
                                                      rank_selection],
                                         'mutator': [simple_mutation, scramble_mutation,
                                                     displacement_mutation],
                                         'crossover_operator': [cv.order_based_crossover,
                                                                cv.partially_mapped_crossover],
                                         'p_c': [0.5, 0.8, 0.9],
                                         'p_m': [0.01, 0.05, 0.1, 0.2],
                                         'elitism': [0, 1, 2, 5],
                                         'verbose': [False],
                                         'log': [False],
                                         'path': [False],
                                         'plot': [False]
                                         })

    print(result)
