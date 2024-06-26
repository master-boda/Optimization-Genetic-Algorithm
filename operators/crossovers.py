import random

def partially_mapped_crossover(parent1: list, parent2: list) -> tuple:
    """
    Perform a partially mapped crossover (PMX) between two parent sequences.
    
    PMX (Partially Mapped Crossover) is a crossover operator used in genetic algorithms that preserves
    the relative ordering of elements. It works by selecting a random segment from one parent and mapping
    the values to the corresponding segment in the other parent. The remaining values are then mapped based
    on the values in the selected segment.

    Args:
        parent1 (list): The first parent sequence.
        parent2 (list): The second parent sequence.

    Returns:
        tuple: Two offspring sequences resulting from the crossover.

    Example Usage:
        parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        parent2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
        child1, child2 = partially_mapped_crossover(parent1, parent2)
    """
    size = len(parent1)

    # select two crossover points
    idx1, idx2 = sorted(random.sample(range(1, size-1), 2))
    offspring1, offspring2 = [None] * size, [None] * size

    # set fixed ends (usually the start and end points are not changed)
    offspring1[0], offspring1[-1] = parent1[0], parent1[-1]
    offspring2[0], offspring2[-1] = parent2[0], parent2[-1]

    # copy segments between idx1 and idx2 from one parent to the other
    offspring1[idx1:idx2+1] = parent2[idx1:idx2+1]
    offspring2[idx1:idx2+1] = parent1[idx1:idx2+1]

    # create mapping based on copied segments to maintain relative ordering
    mapping1 = {parent2[i]: parent1[i] for i in range(idx1, idx2+1)}
    mapping2 = {parent1[i]: parent2[i] for i in range(idx1, idx2+1)}

    # function to apply mapping and fill None values in the offspring arrays
    def apply_mapping(offspring, mapping, parent):
        for i in range(1, size - 1):
            if offspring[i] is None:
                mapped_value = parent[i]
                # Resolve mapping conflicts until a unique value is found
                while mapped_value in mapping:
                    mapped_value = mapping[mapped_value]
                offspring[i] = mapped_value

    # apply mappings to complete the offspring sequences
    apply_mapping(offspring1, mapping1, parent1)
    apply_mapping(offspring2, mapping2, parent2)
    
    return offspring1, offspring2

def order_crossover(parent1: list, parent2: list) -> tuple:
    """
    Perform an ordered crossover between two parents to generate two offspring.

    The function selects a random subset from each parent and maintains the order of these elements in the respective offspring.
    It then fills the rest of each offspring's genome with genes from the other parent in the order they appear,
    skipping genes already included from the selected subset.

    Parameters:
        - parent1 (list): The first parent's genome.
        - parent2 (list): The second parent's genome.

    Returns:
        - tuple of lists: A tuple containing the genomes of the two offspring resulting from the crossover.

    Example Usage:
        parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        parent2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
        child1, child2 = order_crossover(parent1, parent2)
    """
    size = len(parent1)
    # generate two random crossover points
    start, end = sorted(random.sample(range(1, size - 1), 2))
    
    # initialize offspring with None placeholders
    offspring1 = [None] * size
    offspring2 = [None] * size
    
    # include the subset from each parent into the respective offspring
    offspring1[start:end+1] = parent2[start:end+1]
    offspring2[start:end+1] = parent1[start:end+1]
    
    # fill the remaining positions in offspring1 with the elements from parent1 in order
    fill_pos1 = (item for item in parent1 if item not in offspring1[start:end+1])
    index1 = 0
    for gene in fill_pos1:
        while offspring1[index1] is not None:
            index1 += 1
        if index1 < size:
            offspring1[index1] = gene
            index1 += 1
    
    # fill the remaining positions in offspring2 with the elements from parent2 in order
    fill_pos2 = (item for item in parent2 if item not in offspring2[start:end+1])
    index2 = 0
    for gene in fill_pos2:
        while offspring2[index2] is not None:
            index2 += 1
        if index2 < size:
            offspring2[index2] = gene
            index2 += 1
    
    return offspring1, offspring2

def fast_order_mapped_crossover(parent1: list, parent2: list) -> tuple:
    """
    Performs a Fast Ordered Mapped Crossover (FOMX) on two parent genomes.

    This function first selects two random cut points in the parent genomes. It then swaps the segments between these cut points 
    to create two offspring. The remaining areas in each offspring are filled with the areas from the other parent that are not already 
    in the offspring, preserving the order of appearance in the parent.

    Args:
        parent1 (list): The first parent genome.
        parent2 (list): The second parent genome.

    Returns:
        tuple: A tuple containing two genomes.
    
    Example Usage:
        parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        parent2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
        child1, child2 = fast_order_mapped_crossover(parent1, parent2) 

    Note:
        This function assumes that the parent genomes are lists of the same length and that they do not contain any None values.
    """
    size = len(parent1)
    
    # select two random cut points
    cutpoint1, cutpoint2 = sorted(random.sample(range(1, size-1), 2))
    
    # extract segments between the cut points from each parent
    segment1 = parent1[cutpoint1:cutpoint2+1]
    segment2 = parent2[cutpoint1:cutpoint2+1]
    
    # initialize offspring with None values
    offspring1 = [None] * size
    offspring2 = [None] * size
    
    # place the extracted segments into the corresponding positions in the offspring
    offspring1[cutpoint1:cutpoint2+1] = segment2
    offspring2[cutpoint1:cutpoint2+1] = segment1
    
    # create lists of remaining areas that are not part of the copied segments
    remaining_areas1 = [area for area in parent2 if area not in segment2]
    remaining_areas2 = [area for area in parent1 if area not in segment1]
    
    # fill in the remaining areas in the offspring, preserving the order from the other parent
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


def cycle_crossover(parent1: list, parent2: list) -> tuple:
    """
    Perform a cycle crossover on two parent lists to produce two offspring lists.

    Cycle crossover works by identifying a cycle of values between two parents and 
    then alternating the values between the parents to create two offspring. The cycle
    is identified by starting at a random position and following the mapping between the parents' values.

    Parameters:
    parent1 (list): The first parent permutation.
    parent2 (list): The second parent permutation.

    Returns:
    tuple: Two offspring permutations generated from the parents.

    Example Usage:
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    parent2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
    child1, child2 = cycle_crossover(parent1, parent2)
    
    """
    
    size = len(parent1)
    offspring1 = [0] * size
    offspring2 = [0] * size
    visited = [False] * size
    
    # randomly select the starting position for the cycle
    start_pos = random.randint(0, size - 1)
    cycle = []
    
    # identify the cycle starting from the randomly chosen position
    while True:
        cycle.append(start_pos)
        visited[start_pos] = True
        value = parent1[start_pos]
        next_pos = parent2.index(value)
        if visited[next_pos]:
            break
        else:
            start_pos = next_pos
    
    # copy the identified cycle to the offspring
    for pos in cycle:
        offspring1[pos] = parent1[pos]
        offspring2[pos] = parent2[pos]
    
    # fill in the remaining positions with the other parent's genes
    for i in range(size):
        if offspring1[i] == 0:
            offspring1[i] = parent2[i]
        if offspring2[i] == 0:
            offspring2[i] = parent1[i]
    
    return offspring1, offspring2


    
    