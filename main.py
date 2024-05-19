from operators.crossovers import *
from operators.mutators import *    
from pop.population import *
from utils.utils import *
from main.genetic_algorithm import *
from operators.selection_algorithms import *

# insert matrix in "matrix_to_use" parameter

ga(initializer=population,
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
    matrix_to_use=,
    matrix_seed=None,
    verbose=True,
    visualize=True,
    dashboard=True,
    fitness_sharing=True)