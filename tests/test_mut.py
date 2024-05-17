import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from operators.mutators import *
from pop.population import generate_individual

test_buddy = generate_individual()


print(test_buddy)
print(inversion_mutation(test_buddy, 1))