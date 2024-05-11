import random
from population import generate_individual

def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(1, size-1), 2))
    child1, child2 = [None]*size, [None]*size

    child1[0], child1[-1] = parent1[0], parent1[-1]
    child2[0], child2[-1] = parent2[0], parent2[-1]

    child1[idx1:idx2+1] = parent2[idx1:idx2+1]
    child2[idx1:idx2+1] = parent1[idx1:idx2+1]

    print(f"Selected Indices: {idx1}, {idx2}")
    print(f"Initial child1: {child1}")
    print(f"Initial child2: {child2}")

    mapping1 = {parent2[i]: parent1[i] for i in range(idx1, idx2+1)}
    mapping2 = {parent1[i]: parent2[i] for i in range(idx1, idx2+1)}

    print(f"Mapping from parent2 to parent1: {mapping1}")
    print(f"Mapping from parent1 to parent2: {mapping2}")

    def apply_mapping(child, mapping):
        for i in range(1, size - 1):
            if child[i] is None:
                original = parent2[i] if child == child1 else parent1[i]
                child[i] = mapping.get(original, original)
        print(f"Final {('child1' if child == child1 else 'child2')}: {child}")

    apply_mapping(child1, mapping1)
    apply_mapping(child2, mapping2)

    return child1, child2

# Test function
def test_partially_mapped_crossover():
    parent1 = generate_individual()
    parent2 = generate_individual()
    child1, child2 = partially_mapped_crossover(parent1, parent2)

# Call the test function
test_partially_mapped_crossover()
