import random
from population import generate_individual
from operators import *

def test_crossover(crossover):
    for i in range(50):
        parent1 = generate_individual()
        parent2 = generate_individual()
        child1, child2 = crossover(parent1, parent2)
        if len(child1) != len(parent1) or len(child2) != len(parent2):
            raise ValueError(f"Error in iteration {i+1}: The children should have the same length as the parents. Child1: {child1}, Child2: {child2}")
        for j in range(1, len(child1) - 1):
            if child1.count(child1[j]) > 1 or child2.count(child2[j]) > 1:
                raise ValueError(f"Error in iteration {i+1}: The children should not have duplicate values. Child1: {child1}, Child2: {child2} (index {j})")

# Call the test function
test_crossover(partially_mapped_crossover)
