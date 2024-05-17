import sys
import os
import optuna
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from operators.optimizations import *
from pop.population import *
from utils.utils import *
from main.genetic_algorithm import *

# Stationary parameters
areas = ['D', 'FC', 'G', 'QS', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN']
geo_gain_matrix = geo_matrix_generator(min_value=-500, max_value=500, size=len(areas))
initializer = population(50)
#evaluator = evaluate_population(geo_gain_matrix)
#elite_func = get_n_elites(3)
selection_pressure = 5

# Lists to plot the model comparison
fitness_scores = []

# Defining the objective function 
def objective(trial):
    initializer = trial.suggest_categorical('initializer', [population])
    evaluator = trial.suggest_categorical('evaluator', [fitness_function])
    crossover = trial.suggest_categorical('crossover', [partially_mapped_crossover, fast_ordered_mapped_crossover, 
                                                        ordered_crossover, cycle_crossover])
    mutation = trial.suggest_categorical('mutation', [simple_mutation, scramble_mutation, displacement_mutation])
    population_size = trial.suggest_categorical('population_size', [50, 100, 200])
    num_generations = trial.suggest_categorical('num_generations', [50, 100, 200])
    mutation_rate = trial.suggest_float('mutation_rate', 0.01, 0.6, log=True)
    crossover_rate = trial.suggest_float('crossover_rate', 0.6, 0.9)
    elitism_size = trial.suggest_int('elitism_size', 1, 10)
    selection = trial.suggest_categorical('selection', [roulette_selection, rank_selection, tournament_selection])
    
    # Running genetic algorithm with the different parameters
    solution = ga(initializer=initializer,
                  evaluator=evaluator,
                  selection=selection,
                  crossover=crossover,
                  mutation=mutation,
                  mutation_rate=mutation_rate,
                  population_size=population_size,
                  num_generations=num_generations,
                  elitism_size=elitism_size,
                  crossover_rate=crossover_rate,
                  #elite_func=elite_func,
                  verbose=False, 
                  #log_path=None,
                  elitism=False, 
                  #seed=None,
                  matrix_to_use=geo_gain_matrix)

    # Evaluating the given solution
    distance = fitness_function(solution, geo_gain_matrix)
    fitness_scores.append(distance)
    
    return distance

def optimize_optuna(n_trials):
    # Running and tunning parameters with Optuna optimization
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial), n_trials=n_trials)

    # Get the best parameters and their corresponding fitness
    best_params = study.best_params
    best_value = study.best_value

    print("Best Parameters:", best_params)
    print("Best Distance:", best_value)

    # Plot the evolution of fitness values
    plt.plot(fitness_scores, label='Fitness Scores')
    plt.xlabel('Trials')
    plt.ylabel('Fitness Score')
    plt.legend()
    plt.show()

optimize_optuna(2)
