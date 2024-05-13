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


