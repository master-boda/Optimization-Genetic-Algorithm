import random

def correct_forbidden_sequences(child):
    size = len(child)
    forbidden_sequences = [("Q", "G"), ("C", "S"), ("Q", "S"), ("D", "V")]
    for i in range(size - 1):
        if (child[i], child[i+1]) in forbidden_sequences:
            # swap with a non-sequence forming element
            # ensures we do not with Dirtmouth
            if i > 0:  # swap with previous if not the first element
                child[i], child[i-1] = child[i-1], child[i]
            elif i < size - 2:  # swap with next if not near the last element
                child[i+1], child[i+2] = child[i+2], child[i+1]

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

    correct_forbidden_sequences(child1)
    correct_forbidden_sequences(child2)
    
    return child1, child2

# order and cycle crossover

def simple_mutation(individual, config):
    if random.random() < config.mutation_rate:
        size = len(individual)
        
        # prevents mutation of Dirtmouth
        idx1, idx2 = random.sample(range(1, size-1), 2)
        
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    
        correct_forbidden_sequences(individual)

    return individual
