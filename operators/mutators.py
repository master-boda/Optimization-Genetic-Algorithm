import random

def swap_mutation(individual: list, rate: float) -> list:
    """
    Apply a simple swap mutation to an individual within a genetic algorithm based on a given mutation rate.

    This mutation selects two random positions within the individual (excluding the first and last elements,
    which are assumed to be 'D' for Dirtmouth) and swaps their values. This simple change can help the genetic
    algorithm escape local optima by introducing variability into the population without making drastic changes.

    Parameters:
    individual (list): The individual to mutate, represented as a list of locations, where the
                       first and last elements are 'D', representing Dirtmouth.
    rate (float): The probability that the mutation will be applied to the individual.

    Returns:
    list: The mutated individual, which may be unchanged if the mutation was not applied.

    Example Usage:
        individual = ['D', 'A', 'B', 'C', 'D']
        swap_mutation(individual, 0.5)
        # Output: ['D', 'A', 'C', 'B', 'D']
    """
    # Check if mutation should be applied based on the mutation rate
    if random.random() < rate:
        size = len(individual)
        
        # Select two random positions, excluding the first and last elements (Dirtmouth)
        idx1, idx2 = random.sample(range(1, size - 1), 2)
        
        # Swap the chosen positions
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

    return individual


def inversion_mutation(individual: list, rate: float) -> list:
    """
    Perform an inversion mutation on a genetic algorithm individual with a given probability.

    This mutation randomly selects a contiguous segment of the individual (excluding the 
    first and last elements, which are fixed as 'D') and reverses the order of the elements 
    within this segment. This introduces variability while maintaining the start and end points.
    
    Parameters:
        individual (list): The individual to mutate. It must start and end with 'D'.
        rate (float): The probability of the mutation being applied to the individual.

    Returns:
        list: The mutated individual, which may be unchanged if the mutation did not occur.

    Example Usage:
        individual = ['D', 'A', 'B', 'C', 'D']
        inversion_mutation(individual, 0.5)
        # Output: ['D', 'C', 'B', 'A', 'D']
    """
    # check if mutation should be applied based on the mutation rate
    if random.random() < rate:
        size = len(individual)
        
        # choose the start and end indices of the segment to invert, ensuring they are within bounds
        point1, point2 = sorted(random.sample(range(1, size - 1), 2))
        
        # perform the inversion on the selected segment
        individual = individual[:point1] + individual[point1:point2+1][::-1] + individual[point2+1:]

    return individual


def displacement_mutation(individual: list, rate: float) -> list:
    """
    Apply a displacement mutation to an individual within a genetic algorithm based on a given mutation rate.

    This mutation selects a contiguous segment from the individual (excluding the fixed start and end at 'D'),
    removes it, and reinserts it at a different position. This mutation is more disruptive than a simple swap
    or scramble as it can significantly alter the structure of the route while still preserving the sequence
    of the displaced segment.

    Parameters:
        individual (list): The individual to mutate, represented as a list of locations, where the
                           first and last elements are 'D', representing Dirtmouth.
        rate (float): The probability that the mutation will be applied to the individual.

    Returns:
        list: The mutated individual, which may be unchanged if the mutation was not applied.

    Example Usage:
        individual = ['D', 'A', 'B', 'C', 'D']
        displacement_mutation(individual, 0.5)
        # Output: ['D', 'B', 'C', 'A', 'D']
    """
    # check if mutation should be applied based on the mutation rate
    if random.random() < rate:
        size = len(individual)
        
        # choose start and end indices for the segment to be displaced, avoiding the first and last positions
        start, end = sorted(random.sample(range(1, size - 1), 2))
        
        # extract the segment
        segment = individual[start:end + 1]
        
        # remove the segment from the original position
        remaining_individual = individual[:start] + individual[end + 1:]
        
        # choose a new insertion position, avoiding the start and end of the list
        insert_position = random.choice(range(1, len(remaining_individual)))
        
        # reinsert the segment at the new position
        individual = remaining_individual[:insert_position] + segment + remaining_individual[insert_position:]

    return individual