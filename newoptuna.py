import optuna
from operators.selection_algorithms import *
from operators.crossovers import *
from operators.mutators import *
from operators.optimizations import *
from pop.population import *
from utils.utils import *
from main.genetic_algorithm import *
import matplotlib.pyplot as plt
from tqdm import tqdm

areas = ['D', 'FC', 'G', 'QS', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN']
size = len(areas)
geo_gain_matrix = geo_matrix_generator(min_value=-500, max_value=500,size=size)
fitness_scores = []
initializer = population

# Defining the mappings
INITIALIZERS = {'population': population}
EVALUATORS = {'fitness_function': fitness_function}
CROSSOVERS = {
    'partially_mapped_crossover': partially_mapped_crossover,
    'fast_ordered_mapped_crossover': fast_ordered_mapped_crossover,
    'ordered_crossover': ordered_crossover,
    'cycle_crossover': cycle_crossover
}
MUTATIONS = {
    'simple_mutation': simple_mutation,
    'scramble_mutation': scramble_mutation,
    'displacement_mutation': displacement_mutation
}
SELECTIONS = {
    'roulette_selection': roulette_selection,
    'rank_selection': rank_selection,
    'tournament_selection': tournament_selection
}

# Defining the objective function 
def objective(trial):
    initializer = INITIALIZERS[trial.suggest_categorical('initializer', list(INITIALIZERS.keys()))]
    evaluator = EVALUATORS[trial.suggest_categorical('evaluator', list(EVALUATORS.keys()))]
    crossover = CROSSOVERS[trial.suggest_categorical('crossover', list(CROSSOVERS.keys()))]
    mutation = MUTATIONS[trial.suggest_categorical('mutation', list(MUTATIONS.keys()))]
    population_size = trial.suggest_categorical('population_size', [50, 100, 200])
    num_generations = trial.suggest_categorical('num_generations', [50, 100, 200])
    mutation_rate = trial.suggest_float('mutation_rate', 0.01, 0.4, log=True)
    crossover_rate = trial.suggest_float('crossover_rate', 0.6, 0.9)
    elitism_size = trial.suggest_int('elitism_size', 1, 10)
    selection = SELECTIONS[trial.suggest_categorical('selection', list(SELECTIONS.keys()))]
    
    # Running genetic algorithm with the different parameters
    solution, best_fitness = ga(initializer=initializer,
                                evaluator=evaluator,
                                selection=selection,
                                crossover=crossover,
                                mutation=mutation,
                                mutation_rate=mutation_rate,
                                population_size=population_size,
                                num_generations=num_generations,
                                elitism_size=elitism_size,
                                crossover_rate=crossover_rate,
                                verbose=False, 
                                elitism=False, 
                                matrix_to_use=geo_gain_matrix)

    # Evaluating the given solution
    fitness_scores.append(best_fitness)
    
    return best_fitness

def optimize_optuna(n_trials):
    # Running and tuning parameters with Optuna optimization
    study = optuna.create_study(direction='maximize')

    # Use tqdm to create a progress bar
    for _ in tqdm(range(n_trials), desc="Optimization Progress"):
        study.optimize(lambda trial: objective(trial), n_trials=1)

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

optimize_optuna(20)