import random

def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    # Exclude the first and the last index from sampling
    idx1, idx2 = sorted(random.sample(range(1, size-1), 2))
    child1, child2 = [None]*size, [None]*size

    # Preserve the first and last elements
    child1[0], child1[-1] = parent1[0], parent1[-1]
    child2[0], child2[-1] = parent2[0], parent2[-1]

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


def order_crossover(parent1, parent2):
    size = len(parent1)
    # Exclude the first and the last index from sampling
    idx1, idx2 = sorted(random.sample(range(1, size-1), 2))
    child = [None]*size

    # Copy the endpoints
    child[0], child[-1] = parent1[0], parent1[-1]

    # Copy a slice from first parent:
    child[idx1:idx2+1] = parent1[idx1:idx2+1]

    # Fill from second parent:
    p2idx = (idx2 + 1) % size
    cidx = (idx2 + 1) % size
    while None in child:
        if parent2[p2idx] not in child:
            child[cidx] = parent2[p2idx]
            cidx = (cidx + 1) % size
        p2idx = (p2idx + 1) % size

    return child


def cycle_crossover(parent1, parent2):
    size = len(parent1)
    child1, child2 = [None]*size, [None]*size
    cycle = 0
    
    # Start the cycles avoiding the first and last element
    while None in child1[1:-1]:  # Only consider inner elements for cycles
        if cycle % 2 == 0:  # Copy cycle from parent1 to child1, parent2 to child2
            start = next(i for i, x in enumerate(child1[1:-1], 1) if x is None)
            index = start
            while True:
                child1[index] = parent1[index]
                child2[index] = parent2[index]
                index = parent1.index(parent2[index])
                if index == start:
                    break
        cycle += 1

    # Ensure the first and last elements are copied directly
    child1[0], child1[-1] = parent1[0], parent1[-1]
    child2[0], child2[-1] = parent2[0], parent2[-1]

    return child1, child2

def simple_mutation(individual, config):
    # Check if mutation occurs based on the mutation rate
    if random.random() < config.mutation_rate:
        size = len(individual)
        
        # Generate two random indices between 1 and len(individual)-2
        # to exclude the first and last elements from swapping
        idx1, idx2 = random.sample(range(1, size-1), 2)
        
        # Perform the swap
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    
    return individual
