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

import numpy as np

def cycle_crossover(parent1, parent2):
    """
    Perform cycle crossover (CX) between two parent permutations.
    
    :param parent1: List of elements representing the first parent.
    :param parent2: List of elements representing the second parent.
    :return: Two children resulting from the crossover.
    """
    size = len(parent1)
    child1 = [None] * size
    child2 = [None] * size

    # Create a mask for tracking visited indices
    visited = [False] * size
    
    def get_cycle(start):
        cycle = []
        current = start
        while True:
            cycle.append(current)
            visited[current] = True
            current = parent1.index(parent2[current])
            if current == start:
                break
        return cycle
    
    # Perform the cycle crossover
    for i in range(size):
        if not visited[i]:
            cycle = get_cycle(i)
            for index in cycle:
                child1[index] = parent1[index]
                child2[index] = parent2[index]

    # Fill in the rest from the other parent
    for i in range(size):
        if child1[i] is None:
            child1[i] = parent2[i]
        if child2[i] is None:
            child2[i] = parent1[i]

    return child1, child2

# Example usage
parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
parent2 = [4, 1, 2, 3, 6, 5, 8, 7]

child1, child2 = cycle_crossover(parent1, parent2)
print("Parent 1:  ", parent1)
print("Parent 2:  ", parent2)
print("Child 1:   ", child1)
print("Child 2:   ", child2)
    