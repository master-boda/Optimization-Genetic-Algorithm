import random
import numpy as np
def partially_mapped_crossover(parent1: list, parent2: list) -> tuple:
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(1, size-1), 2))
    offspring1, offspring2 = [None]*size, [None]*size

    # set fixed ends
    offspring1[0], offspring1[-1] = parent1[0], parent1[-1]
    offspring2[0], offspring2[-1] = parent2[0], parent2[-1]

    # copy segments between idx1 and idx2 from one parent to the other
    offspring1[idx1:idx2+1] = parent2[idx1:idx2+1]
    offspring2[idx1:idx2+1] = parent1[idx1:idx2+1]

    # create mapping based on copied segments
    mapping1 = {parent2[i]: parent1[i] for i in range(idx1, idx2+1)}
    mapping2 = {parent1[i]: parent2[i] for i in range(idx1, idx2+1)}

    # apply mappings to fill None values in the offspring arrays
    def apply_mapping(offspring, mapping, parent):
        for i in range(1, size - 1):
            if offspring[i] is None:
                mapped_value = parent[i]
                while mapped_value in mapping:
                    mapped_value = mapping[mapped_value]
                offspring[i] = mapped_value

    apply_mapping(offspring1, mapping1, parent1)
    apply_mapping(offspring2, mapping2, parent2)
    
    return offspring1, offspring2

def fast_ordered_mapped_crossover(parent1: list, parent2: list) -> tuple:
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



def ordered_crossover(parent1: list, parent2: list) -> tuple:
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
    """
    size = len(parent1)
    # Generate two random crossover points
    start, end = sorted(random.sample(range(1, size - 1), 2))
    
    # Initialize offspring with None placeholders
    offspring1 = [None] * size
    offspring2 = [None] * size
    
    # Include the subset from each parent into the respective offspring
    offspring1[start:end+1] = parent2[start:end+1]
    offspring2[start:end+1] = parent1[start:end+1]
    
    # Fill the remaining positions in offspring1 with the elements from parent1 in order
    fill_pos1 = (item for item in parent1 if item not in offspring1[start:end+1])
    index1 = 0
    for gene in fill_pos1:
        while offspring1[index1] is not None:
            index1 += 1
        if index1 < size:
            offspring1[index1] = gene
            index1 += 1
    
    # Fill the remaining positions in offspring2 with the elements from parent2 in order
    fill_pos2 = (item for item in parent2 if item not in offspring2[start:end+1])
    index2 = 0
    for gene in fill_pos2:
        while offspring2[index2] is not None:
            index2 += 1
        if index2 < size:
            offspring2[index2] = gene
            index2 += 1
    
    return offspring1, offspring2


def cycle_crossover(parent1: list, parent2: list) -> tuple:
    size = len(parent1)
    offspring1, offspring2 = [None]*size, [None]*size

    visited = [False] * size

    # Randomly select a starting position for the cycle
    #start_pos = random.randint(0, size - 1)
    start_pos = 0
    cycle = []

    # Create the cycle
    current_pos = start_pos
    while not visited[current_pos]:
        cycle.append(current_pos)
        visited[current_pos] = True
        value = parent1[current_pos]
        current_pos = parent2.index(value)

    # Assign cycle values to offspring
    for pos in cycle:
        offspring1[pos] = parent1[pos]
        offspring2[pos] = parent2[pos]

    # Fill in the remaining positions with values from the other parent
    for i in range(size):
        if offspring1[i] is None:
            offspring1[i] = parent2[i]
        if offspring2[i] is None:
            offspring2[i] = parent1[i]

    return offspring1, offspring2

  def sequential_constructive_crossover(parent1, parent2):
    
    def select_city(parent, index, used):
        city = parent[index]
        while city in used:
            index = (index + 1) % len(parent)
            city = parent[index]
        return city

    size = len(parent1)
    offspring1 = []
    offspring2 = []
    
    used1 = set()
    used2 = set()
    
    index1_1 = 0
    index1_2 = 0
    index2_1 = 0
    index2_2 = 0
    
    while len(offspring1) < size and len(offspring2) < size:
        # Alternate for offspring1
        if len(offspring1) < size:
            if len(offspring1) % 2 == 0:
                city = select_city(parent1, index1_1, used1)
                index1_1 = (index1_1 + 1) % size
            else:
                city = select_city(parent2, index2_1, used1)
                index2_1 = (index2_1 + 1) % size
            offspring1.append(city)
            used1.add(city)
        
        # Alternate for offspring2
        if len(offspring2) < size:
            if len(offspring2) % 2 == 0:
                city = select_city(parent2, index1_2, used2)
                index1_2 = (index1_2 + 1) % size
            else:
                city = select_city(parent1, index2_2, used2)
                index2_2 = (index2_2 + 1) % size
            offspring2.append(city)
            used2.add(city)
    
    return offspring1, offspring2
    

    
    