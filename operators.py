import random
import numpy as np

def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(1, size-1), 2))
    child1, child2 = [None]*size, [None]*size

    # set fixed ends
    child1[0], child1[-1] = parent1[0], parent1[-1]
    child2[0], child2[-1] = parent2[0], parent2[-1]

    # copy segments between idx1 and idx2 from one parent to the other
    child1[idx1:idx2+1] = parent2[idx1:idx2+1]
    child2[idx1:idx2+1] = parent1[idx1:idx2+1]

    # create mapping based on copied segments
    mapping1 = {parent2[i]: parent1[i] for i in range(idx1, idx2+1)}
    mapping2 = {parent1[i]: parent2[i] for i in range(idx1, idx2+1)}

    # apply mappings to fill None values in the child arrays
    def apply_mapping(child, mapping, parent):
        for i in range(1, size - 1):
            if child[i] is None:
                mapped_value = parent[i]
                while mapped_value in mapping:
                    mapped_value = mapping[mapped_value]
                child[i] = mapped_value

    apply_mapping(child1, mapping1, parent1)
    apply_mapping(child2, mapping2, parent2)
    
    return child1, child2    
    
def simple_mutation(individual, rate):
    if random.random() < rate:
        size = len(individual)
        
        # prevents mutation of Dirtmouth
        idx1, idx2 = random.sample(range(1, size-1), 2)
        
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

    return individual
    
from utils import fitness_function

def two_opt(route, geo_matrix, max_iterations=2):
    best_route = route[:]
    improved = False
    iteration = 0

    while not improved and iteration < max_iterations:
        improved = False
        best_fit = fitness_function(best_route, geo_matrix)  # Use the custom fitness function
        # Note: start i from 1 and stop j at len(route) - 2 to keep endpoints fixed
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1:
                    continue  # No need to swap adjacent elements
                new_route = best_route[:]
                # Reverse the segment between i and j+1
                new_route[i:j + 1] = reversed(new_route[i:j + 1])
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