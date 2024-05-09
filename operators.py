import random

def order_crossover(parent1, parent2):
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(size), 2))
    child = [None]*size

    # Copy a slice from first parent:
    child[idx1:idx2+1] = parent1[idx1:idx2+1]

    # Fill from second parent:
    p2idx = (idx2 + 1) % size  # Start right after the slice in parent2
    cidx = (idx2 + 1) % size   # Start right after the slice in child
    while None in child:
        if parent2[p2idx] not in child:
            child[cidx] = parent2[p2idx]
            cidx = (cidx + 1) % size
        p2idx = (p2idx + 1) % size

    return child

def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(size), 2))
    child = [None]*size
    
    # Initialize children with None
    child1, child2 = [None]*size, [None]*size

    # Copy the crossover segments
    child1[idx1:idx2+1] = parent2[idx1:idx2+1]
    child2[idx1:idx2+1] = parent1[idx1:idx2+1]

    # Create mapping from segment swaps
    mapping1 = {parent2[i]: parent1[i] for i in range(idx1, idx2+1)}
    mapping2 = {parent1[i]: parent2[i] for i in range(idx1, idx2+1)}

    # Function to apply mapping
    def apply_mapping(child, mapping):
        for i in range(size):
            if i < idx1 or i > idx2:
                while child[i] in mapping:
                    child[i] = mapping[child[i]]
    
    # Fill in the remaining slots in children
    for i in range(size):
        if child1[i] is None:
            child1[i] = parent1[i] if parent1[i] not in child1 else mapping1[parent1[i]]
        if child2[i] is None:
            child2[i] = parent2[i] if parent2[i] not in child2 else mapping2[parent2[i]]

    apply_mapping(child1, mapping1)
    apply_mapping(child2, mapping2)
    
    return child1, child2

def cycle_crossover(parent1, parent2):
    size = len(parent1)
    child1, child2 = [None]*size, [None]*size
    cycle = 0
    used_indices = set()
    
    while None in child1:
        if cycle % 2 == 0:  # Copy cycle from parent1 to child1, parent2 to child2
            start = child1.index(None)
            index = start
            while True:
                child1[index] = parent1[index]
                child2[index] = parent2[index]
                used_indices.add(index)
                index = parent1.index(parent2[index])
                if index == start:
                    break
        cycle += 1

    return child1, child2
