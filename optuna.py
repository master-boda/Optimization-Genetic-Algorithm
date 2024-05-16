from pop.population import population
from operators.selection_algorithms import roulette_selection, rank_selection, tournament_selection #check
from operators.crossovers import partially_mapped_crossover, fast_ordered_mapped_crossover, ordered_crossover, cycle_crossover #CHECK
from operators.mutators import simple_mutation, scramble_mutation, displacement_mutation#check
from main.genetic_algorithm import ga#check
from utils.utils import geo_matrix_generator, fitness_function#check
import optuna
import matplotlib.pyplot as plt


# Stationary parameters
areas = ['D', 'FC', 'G', 'QS', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN']
geo_gain_matrix = geo_matrix_generator(0.8, areas)
initializer = population(areas)
#evaluator = evaluate_population(geo_gain_matrix)
#elite_func = get_n_elites(3)
selection_pressure = 5

# Lists to plot the model comparison
fitness_scores = []

# Defining the objective function 
def objective(trial):
    pop_size = trial.suggest_categorical('pop_size', [25, 50, 100])
    n_gens = trial.suggest_categorical('n_gens', [50, 100, 200])
    mutation_rate = trial.suggest_float('mutation_rate', 0.01, 0.1, log=True)
    crossover_rate = trial.suggest_float('crossover_rate', 0.7, 0.9)
    selector= trial.suggest_categorical('selector', [roulette_selection, rank_selection, tournament_selection])
    mutator= trial.suggest_categorical('mutator', [simple_mutation, scramble_mutation, displacement_mutation])
    crossover= trial.suggest_categorical('crossover', [partially_mapped_crossover, fast_ordered_mapped_crossover, ordered_crossover, cycle_crossover])
   
    # Running genetic algorithm with the different parameters
    solution = ga(initializer, 
                  #evaluator, 
                  selector, crossover, mutator, 
                  pop_size, n_gens, crossover_rate, mutation_rate,
                  #elite_func, 
                  verbose=False, log_path=None, elitism=False, seed=42,
                  geo_matrix = geo_gain_matrix)
    
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