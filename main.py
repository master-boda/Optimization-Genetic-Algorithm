from operators.crossovers import *
from operators.mutators import *    
from pop.population import *
from utils.utils import *
from main.genetic_algorithm import *
from operators.selection_algorithms import *


ga(population, fitness_function, roulette_selection, partially_mapped_crossover, simple_mutation, matrix_seed=42)

#ga(initializer=population,
#   evaluator=fitness_function,
#    selection=,
#    crossover=,
#    mutation=,
#    mutation_rate=,
#    population_size=,
#    num_generations=,
#    crossover_rate=,
#    elitism_size=,
#    elitisim=,
#    maximize=,
#    verbose=)
