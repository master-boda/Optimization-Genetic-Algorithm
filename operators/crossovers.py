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