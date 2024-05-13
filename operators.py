import random

def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(1, size-1), 2))
    child1, child2 = [None]*size, [None]*size

    child1[0], child1[-1] = parent1[0], parent1[-1]
    child2[0], child2[-1] = parent2[0], parent2[-1]

    child1[idx1:idx2+1] = parent2[idx1:idx2+1]
    child2[idx1:idx2+1] = parent1[idx1:idx2+1]

    mapping1 = {parent2[i]: parent1[i] for i in range(idx1, idx2+1)}
    mapping2 = {parent1[i]: parent2[i] for i in range(idx1, idx2+1)}

    def apply_mapping(child, mapping):
        for i in range(1, size - 1):
            if child[i] is None:
                child[i] = mapping.get(parent2[i], parent2[i])

    apply_mapping(child1, mapping1)
    apply_mapping(child2, mapping2)
    
    return child1, child2

def fomx_crossover(parent1, parent2):
    size = len(parent1)
    # Select two random crossover points
    cut_point1, cut_point2 = sorted(random.sample(range(1, size-1), 2))

    # Initialize offspring with null values
    offspring1 = [None] * size
    offspring2 = [None] * size

    # Copy the segments between cut points from each parent to the other offspring
    for i in range(cut_point1, cut_point2 + 1):
        offspring1[i] = parent2[i]
        offspring2[i] = parent1[i]

    # Initialize mapping dictionaries to track duplications
    map1 = {parent2[i]: parent1[i] for i in range(cut_point1, cut_point2 + 1)}
    map2 = {parent1[i]: parent2[i] for i in range(cut_point1, cut_point2 + 1)}

    # Fill the rest of the offspring, avoiding duplicates
    def fill_offspring(offspring, parent, map):
        j = 0
        for i in range(size):
            if cut_point1 <= i <= cut_point2:
                continue
            gene = parent[i]
            original_gene = gene
            seen = set()
            while gene in map:
                if gene in seen or gene == offspring[j]:  # Detect cycle or already placed gene
                    gene = None  # Break the cycle, place None temporarily
                    break
                seen.add(gene)
                gene = map[gene]

            while offspring[j] is not None:
                j += 1  # Find the next available spot
            offspring[j] = gene if gene is not None else original_gene  # Place the gene or the original if unresolved

    # Fill both offspring using the helper function
    fill_offspring(offspring1, parent1, map2)
    fill_offspring(offspring2, parent2, map1)

    # Set first and last elements if not already set (for path integrity in some problems)
    offspring1[0], offspring1[-1] = parent1[0], parent1[-1]
    offspring2[0], offspring2[-1] = parent2[0], parent2[-1]

    return offspring1, offspring2
    
    
def simple_mutation(individual, rate):
    if random.random() < rate:
        size = len(individual)
        
        # prevents mutation of Dirtmouth
        idx1, idx2 = random.sample(range(1, size-1), 2)
        
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

    return individual
    
from utils import fitness_function

def two_opt(route, geo_matrix, max_iterations=100000):
    """
    Implements the 2-opt optimization algorithm to improve the route.

    Parameters:
    route (list): Initial route, with the first and last elements fixed.
    geo_matrix (DataFrame): DataFrame where indices and columns represent areas, and values indicate Geo changes between areas.
    max_iterations (int): Maximum number of iterations to perform without improvement before stopping.

    Returns:
    list: Optimized route.
    """
    best_route = route[:]
    improved = False
    iteration = 0

    while not improved and iteration < max_iterations:
        improved = False
        best_fit = fitness_function(best_route, geo_matrix)  # Use the custom fitness function
        # Note: start i from 1 and stop j at len(route) - 2 to keep endpoints fixed
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1: continue  # No need to swap adjacent elements
                new_route = best_route[:]
                # Reverse the segment between i and j+1
                new_route[i:j + 1] = new_route[i:j + 1][::-1]
                new_fit = fitness_function(new_route, geo_matrix)  # Use the custom fitness function
                if new_fit > best_fit:
                    best_route = new_route
                    best_fit = new_fit
                    improved = True
                    break
            if improved:
                break
        iteration += 1

    return best_route

def two_opt(route, geo_matrix, max_iterations=1):
    """
    Implements the 2-opt optimization algorithm to improve the route.

    Parameters:
    route (list): Initial route, with the first and last elements fixed.
    geo_matrix (DataFrame): DataFrame where indices and columns represent areas, and values indicate Geo changes between areas.
    max_iterations (int): Maximum number of iterations to perform without improvement before stopping.

    Returns:
    list: Optimized route.
    """
    best_route = route[:]
    improved = False
    iteration = 0

    while not improved and iteration < max_iterations:
        improved = False
        best_fit = fitness_function(best_route, geo_matrix)  # Use the custom fitness function
        # Note: start i from 1 and stop j at len(route) - 2 to keep endpoints fixed
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1: continue  # No need to swap adjacent elements
                new_route = best_route[:]
                # Reverse the segment between i and j+1
                new_route[i:j + 1] = new_route[i:j + 1][::-1]
                new_fit = fitness_function(new_route, geo_matrix)  # Use the custom fitness function
                if new_fit > best_fit:
                    best_route = new_route
                    best_fit = new_fit
                    improved = True
                    break
            if improved:
                break
        iteration += 1

    return best_route