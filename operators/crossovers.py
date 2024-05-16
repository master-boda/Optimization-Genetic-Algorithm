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

def fast_ordered_mapped_crossover(parent1, parent2):
    """
    Performs a Fast Ordered Mapped Crossover (FOMX) on two parent genomes.

    This function first selects two random cut points in the parent genomes. It then swaps the segments between these cut points 
    to create two offspring. The remaining areas in each offspring are filled with the areas from the other parent that are not already 
    in the offspring, preserving the order of appearance in the parent.

    Args:
        parent1 (list): The first parent genome.
        parent2 (list): The second parent genome.

    Returns:
        tuple: A tuple containing two offspring genomes.

    Note:
        This function assumes that the parent genomes are lists of the same length and that they do not contain any None values.
    """
    size = len(parent1)
    
    #random cut points
    cutpoint1, cutpoint2 = sorted(random.sample(range(1, size-1), 2))
    
    #  Extract segment from parent1
    segment1 = parent1[cutpoint1:cutpoint2+1]
    segment2 = parent2[cutpoint1:cutpoint2+1]
    
    # initialize children
    offspring1 = [None]*size
    offspring2 = [None]*size
    
    #Place segments in the corresponding positions
    offspring1[cutpoint1:cutpoint2+1] = segment2
    offspring2[cutpoint1:cutpoint2+1] = segment1
    
    # Create mappings for remaining cities
    remaining_areas1 = [area for area in parent2 if area not in segment2]
    remaining_areas2 = [area for area in parent1 if area not in segment1]
    
    # Fill the remaining areas
    current_pos1 = 0 
    current_pos2 = 0
    
    for area in remaining_areas1:
        while offspring1[current_pos1] is not None:
            current_pos1 += 1
        offspring1[current_pos1] = area
        
    for area in remaining_areas2:    
        while offspring2[current_pos2] is not None:
            current_pos2 += 1
        offspring2[current_pos2] = area
    
    return offspring1, offspring2   



def ordered_crossover(parent1, parent2):
    """
    Perform an ordered crossover between two parents to generate two children.

    The function selects a random subset from each parent and maintains the order of these elements in the respective child.
    It then fills the rest of each child's genome with genes from the other parent in the order they appear,
    skipping genes already included from the selected subset.

    Parameters:
    - parent1 (list): The first parent's genome.
    - parent2 (list): The second parent's genome.

    Returns:
    - tuple of lists: A tuple containing the genomes of the two children resulting from the crossover.
    """
    size = len(parent1)
    # Generate two random crossover points
    start, end = sorted(random.sample(range(1, size - 1), 2))
    
    # Initialize children with None placeholders
    child1 = [None] * size
    child2 = [None] * size
    
    # Include the subset from each parent into the respective child
    child1[start:end+1] = parent2[start:end+1]
    child2[start:end+1] = parent1[start:end+1]
    
    # Fill the remaining positions in child1 with the elements from parent1 in order
    fill_pos1 = (item for item in parent1 if item not in child1[start:end+1])
    index1 = 0
    for gene in fill_pos1:
        while child1[index1] is not None:
            index1 += 1
        if index1 < size:
            child1[index1] = gene
            index1 += 1
    
    # Fill the remaining positions in child2 with the elements from parent2 in order
    fill_pos2 = (item for item in parent2 if item not in child2[start:end+1])
    index2 = 0
    for gene in fill_pos2:
        while child2[index2] is not None:
            index2 += 1
        if index2 < size:
            child2[index2] = gene
            index2 += 1
    
    return child1, child2

def cycle_crossover(parent1, parent2):
    """
    Perform a cycle crossover on two parent lists to produce two offspring lists.

    Cycle crossover (CX) is a crossover operator used in genetic algorithms
    where cycles in the parent permutations are identified and copied directly
    to the offspring.

    Parameters:
    parent1 (list): The first parent permutation.
    parent2 (list): The second parent permutation.

    Returns:
    tuple: Two offspring permutations generated from the parents.
    """
    
    size = len(parent1)
    offspring1 = [0] * size
    offspring2 = [0] * size
    visited = [False] * size
    
    # Randomly select the starting position for the cycle
    start_pos = random.randint(0, size - 1)
    cycle = []
    while True:
        cycle.append(start_pos)
        visited[start_pos] = True
        value = parent1[start_pos]
        next_pos = parent2.index(value)
        if visited[next_pos]:
            break
        else:
            start_pos = next_pos
    
    for pos in cycle:
        offspring1[pos] = parent1[pos]
        offspring2[pos] = parent2[pos]
    
    # Fill in the remaining positions with the other parent's genes
    for i in range(size):
        if offspring1[i] == 0:
            offspring1[i] = parent2[i]
        if offspring2[i] == 0:
            offspring2[i] = parent1[i]
    
    return offspring1, offspring2