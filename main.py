from main.genetic_algorithm import *

# insert matrix in "matrix_to_use" parameter

if __name__ == "__main__":
    result = ga(initializer=population,
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
        matrix_to_use= None, #insert here list of lists, else None
        matrix_seed=None,
        verbose=True,
        visualize=True,
        dashboard=True,
        fitness_sharing=True)
    
    # If len(result) == 5 it means dashboard = True, then activate dash
    if isinstance(result, tuple) and len(result) == 5:
        routes, fitnesses, best_route, best_fitness, matrix = result
        # Call the dashboard function with the GA results only if dashboard=True
        run_dashboard(routes, fitnesses, best_route, matrix)    