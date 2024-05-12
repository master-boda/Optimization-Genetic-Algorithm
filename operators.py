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
    # Select two random crossover points
    cut_point1 = random.randint(1, len(parent1) - 2)
    cut_point2 = random.randint(cut_point1 + 1, len(parent1) - 1)

    # Initialize offspring with null values
    offspring1 = [None] * len(parent1)
    offspring2 = [None] * len(parent2)

    # Copy the segments between cut points from each parent to the other offspring
    for i in range(cut_point1, cut_point2 + 1):
        offspring1[i] = parent2[i]
        offspring2[i] = parent1[i]

    # Initialize mapping dictionaries to track duplications
    map1 = {}
    map2 = {}

    # Populate mapping from parent segments
    for i in range(cut_point1, cut_point2 + 1):
        map1[parent2[i]] = parent1[i]
        map2[parent1[i]] = parent2[i]

    # Fill in the rest of the offspring
    def FillOffspring(offspring, parent, mapping):
        j = 0
        for gene in parent:
            if cut_point1 <= j < cut_point2:
                j += 1
                continue
            while gene in mapping and j < len(offspring):
                gene = mapping[gene]
            if j < len(offspring):
                offspring[j] = gene
                j += 1

    # Fill both offspring using the mapping function
    FillOffspring(offspring1, parent1, map2)
    FillOffspring(offspring2, parent2, map1)

    return offspring1, offspring2
