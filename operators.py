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

# order and cycle crossover

def simple_mutation(individual, config):
    if random.random() < config.mutation_rate:
        size = len(individual)
        
        # prevents mutation of Dirtmouth
        idx1, idx2 = random.sample(range(1, size-1), 2)
        
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

    return individual


def FOMX_Crossover(parent1, parent2):
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

import random

def Ordered_crossover(parent1, parent2):
    size = len(parent1)
    cut_point1, cut_point2 = sorted(random.sample(range(1, size-1), 2))
    
    offspring1 = [None] * size
    offspring2 = [None] * size
    
    # Copy the segment
    for i in range(cut_point1, cut_point2 + 1):
        offspring1[i] = parent1[i]
        offspring2[i] = parent2[i]
        
    # Function to fill the rest of the offspring
    def fill_offspring(offspring, parent):
        fill_index = cut_point2 + 1
        used_indices = set(range(cut_point1, cut_point2 + 1))
        for gene in parent:
            if gene not in offspring:
                while offspring[fill_index % len(offspring)] is not None:
                    fill_index += 1
                offspring[fill_index % len(offspring)] = gene
                fill_index += 1


    # Fill offspring1 with elements from parent2 starting after the segment
    fill_offspring(offspring1, parent2) 
    # Fill offspring2 with elements from parent1 starting after the segment
    fill_offspring(offspring2, parent1)
    
    return offspring1, offspring2 # in progress 

Def cycle_crossover(parent1, parent2): 
    size = len(parent1)
    
    
    
    
    
    