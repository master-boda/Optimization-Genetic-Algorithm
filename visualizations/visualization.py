import plotly.graph_objs as go
import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

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


# Example data: Replace these with your actual game areas and Geo earnings/losses
areas = ["D", "FC", "G", "QS", "QG", "CS", "KS", "RG", "DV", "SN"]
coordinates = {
    "D": (0, 0),
    "FC": (1, 2),
    "G": (3, 3),
    "QS": (4, 1),
    "QG": (6, 2),
    "CS": (7, 4),
    "KS": (9, 0),
    "RG": (5, 6),
    "DV": (2, 7),
    "SN": (8, 5)
}

# Function to plot a single route with enhanced aesthetics
def plot_route(route, ax, title, color='skyblue'):
    x = [coordinates[area][0] for area in route]
    y = [coordinates[area][1] for area in route]
    ax.clear()
    ax.plot(x, y, marker='o', markersize=8, markerfacecolor='blue', markeredgewidth=2, markeredgecolor='black', color=color, linewidth=2)
    for area in route:
        ax.text(coordinates[area][0], coordinates[area][1], area, fontsize=12, ha='right', color='darkred', fontweight='bold')
    ax.set_xlabel('X Coordinate', fontsize=14)
    ax.set_ylabel('Y Coordinate', fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 8)

# Function to visualize routes over generations with enhanced aesthetics
def visualize_routes(routes, best_route, interval=500):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    def update(num):
        plot_route(routes[num], ax1, f"Generation {num+1}")
        plot_route(best_route, ax2, "Best Route", color='limegreen')
    
    ani = animation.FuncAnimation(fig, update, frames=len(routes), interval=interval)
    plt.show()
