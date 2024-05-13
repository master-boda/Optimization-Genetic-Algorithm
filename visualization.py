import plotly.graph_objs as go
import plotly.express as px

def plot_best_fitness_per_generation(best_fitness_history):
    """
    Plots the best fitness value per generation as a line chart.

    Parameters:
    - best_fitness_history (list of float): A list of the best fitness values, one for each generation.

    Returns:
    - None: Displays an interactive line chart in the browser.
    """
    generations = list(range(len(best_fitness_history)))
    fig = go.Figure(data=go.Scatter(x=generations, y=best_fitness_history, mode='lines+markers'))
    fig.update_layout(title='Best Fitness per Generation',
                      xaxis_title='Generation',
                      yaxis_title='Best Fitness',
                      template='plotly_white')
    fig.show()


def plot_fitness_histogram(initial_fitnesses, final_fitnesses):
    """
    Plots histograms for the initial and final fitness distributions of a population.

    Parameters:
    - initial_fitnesses (list of float): Fitness values of the initial population.
    - final_fitnesses (list of float): Fitness values of the final population after running the genetic algorithm.

    Returns:
    - None: Displays an interactive histogram comparison in the browser.
    """
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=initial_fitnesses, name='Initial', opacity=0.75))
    fig.add_trace(go.Histogram(x=final_fitnesses, name='Final', opacity=0.75))

    fig.update_layout(title='Initial vs Final Fitness Distribution',
                      xaxis_title='Fitness',
                      yaxis_title='Count',
                      barmode='overlay',
                      template='plotly_white')
    fig.show()

from utils import *
from population import *
from experiment import *

def compare_individuals(n=5):
    matrix = geo_matrix()
    
    for _ in range(n):
        ind1 = generate_individual()
        ind2 = insertion_algorithm(matrix)
        print(f"Individual 1: {ind1}, Fitness: {fitness_function(ind1, matrix)}")
        print(f"Individual 2: {ind2}, Fitness: {fitness_function(ind2, matrix)}")
        
compare_individuals()