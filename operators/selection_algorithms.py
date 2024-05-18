import random

def roulette_selection(population, fitnesses):
    """
    Selects an individual from the population using roulette wheel selection.

    This selection method mimics the concept of a roulette wheel in a casino,
    where each individual is assigned a slice of the wheel proportional to their
    fitness score. Higher fitness individuals have larger slices, increasing
    their chances of selection.

    Args:
        population (list): A list of individuals in the population.
        fitnesses (list): A list of fitness scores corresponding to each individual.

    Returns:
        object: The selected individual from the population.

    Example:
        >>> population = ['A', 'B', 'C']
        >>> fitnesses = [0.2, 0.5, 0.3]
        >>> selected_individual = roulette_selection(population, fitnesses)
    """
    # Calculate the total fitness of the population
    total_fitness = sum(fitnesses)
    
    # Calculate the selection probabilities for each individual
    selection_probs = [f / total_fitness for f in fitnesses]
    
    # Select an individual based on the calculated probabilities
    return random.choices(population, weights=selection_probs)[0]

def tournament_selection(population, fitnesses):
    """
    Selects an individual from the population using tournament selection.

    Tournament selection works by randomly selecting a subset of individuals
    from the population (typically between 3 to 6 individuals). From this
    subset, the individual with the highest fitness score is chosen as the
    selected individual.

    Args:
        population (list): A list of individuals in the population.
        fitnesses (list): A list of fitness scores corresponding to each individual.

    Returns:
        object: The selected individual from the population.

    Example:
        >>> population = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> fitnesses = [0.7, 0.4, 0.9, 0.5, 0.6, 0.8]
        >>> selected_individual = tournament_selection(population, fitnesses)
    """
    # Randomly select a subset of individuals from the population (between 3 to 6 individuals)
    selected_individuals = random.choices(population, k=random.randint(3, 6))
    
    # Find the individual with the highest fitness score in the selected subset
    best_individual = max(selected_individuals, key=lambda ind: fitnesses[population.index(ind)])
    
    return best_individual

def rank_selection(population, fitnesses):
    """
    Selects an individual from the population using rank-based selection.

    Rank-based selection assigns probabilities to individuals based on their
    ranks in terms of fitness scores. Individuals with higher ranks are assigned
    higher probabilities of selection.

    Args:
        population (list): A list of individuals in the population.
        fitnesses (list): A list of fitness scores corresponding to each individual.

    Returns:
        object: The selected individual from the population.

    Example:
        >>> population = ['A', 'B', 'C', 'D', 'E', 'F']
        >>> fitnesses = [0.7, 0.4, 0.9, 0.5, 0.6, 0.8]
        >>> selected_individual = rank_selection(population, fitnesses)
    """
    # Rank individuals by fitness in descending order
    ranked_indices = sorted(range(len(population)), key=lambda idx: fitnesses[idx], reverse=True)
    
    # Assign weights based on ranks
    rank_weights = [len(population) - rank for rank in range(len(population))]
    
    # Select an individual based on rank weights
    selected_index = random.choices(ranked_indices, weights=rank_weights, k=1)[0]
    
    return population[selected_index]

