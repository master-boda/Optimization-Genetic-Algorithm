import random

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