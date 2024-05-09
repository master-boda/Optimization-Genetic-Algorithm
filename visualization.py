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


def plot_geo_matrix_heatmap(matrix):
    """
    Creates a heatmap for the geographic matrix used in a genetic algorithm.

    Parameters:
    - matrix (2D list or 2D numpy array): The geographic matrix where each element is a geo score.

    Returns:
    - None: Displays an interactive heatmap in the browser.
    """
    fig = px.imshow(matrix,
                    labels=dict(x="Position X", y="Position Y", color="Geo"),
                    title="Geo Matrix Heatmap")
    fig.show()


def plot_genetic_diversity_per_generation(diversity_history):
    """
    Plots the genetic diversity per generation as a scatter plot.

    Parameters:
    - diversity_history (list of float): A list of diversity scores, one for each generation.

    Returns:
    - None: Displays an interactive scatter plot in the browser.
    """
    generations = list(range(len(diversity_history)))
    fig = go.Figure(data=go.Scatter(x=generations, y=diversity_history, mode='markers'))
    fig.update_layout(title='Genetic Diversity per Generation',
                      xaxis_title='Generation',
                      yaxis_title='Diversity',
                      template='plotly_white')
    fig.show()


def plot_fitness_distribution_per_generation(fitness_distributions, generation_labels):
    """
    Plots a bar chart showing the number of individuals per fitness range for multiple generations.

    Parameters:
    - fitness_distributions (list of dicts): A list where each element is a dictionary mapping fitness ranges to individual counts for a generation.
    - generation_labels (list of int or str): Labels for each generation, corresponding to each element in fitness_distributions.

    Returns:
    - None: Displays an interactive bar chart in the browser.
    """
    fig = go.Figure()
    for gen, dist in zip(generation_labels, fitness_distributions):
        fig.add_trace(go.Bar(x=list(dist.keys()), y=list(dist.values()), name=f'Generation {gen}'))

    fig.update_layout(title='Fitness Distribution per Generation',
                      xaxis_title='Fitness Ranges',
                      yaxis_title='Number of Individuals',
                      barmode='group',
                      template='plotly_white')
    fig.show()
