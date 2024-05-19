import numpy as np

def check_constraints(route):
    """
    Check if a given route satisfies certain constraints for the game.

    The constraints checked are:
        1. 'Resting Grounds' ('RG') must be in the second half of the route.
        2. 'City of Tears' ('CS') should not appear after 'Queen's Gardens' ('QG').
        3. The route must start and end with 'Dirtmouth' ('D').
        4. No repeated spots are allowed in the route.

    Parameters:
        route (list): The route to be checked, represented as a list of locations.

    Returns:
        list: A list of boolean values indicating whether each constraint is satisfied.

    Example usage:
        route = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']
        constraints = check_constraints(route)
        print(constraints)  # Output: [True, False, True, True]
    """
    # Length of the route ignoring Dirtmouth endpoints
    route_length = len(route) - 2
    
    # Check for 'RG' in the second half of the route
    rg_index = route.index('RG') if 'RG' in route else -1
    constraint1 = rg_index >= len(route) // 2

    # Check if 'CS' is not after 'QG'
    constraint2 = not ('QG' in route and 'CS' in route and route.index('CS') > route.index('QG'))

    # Check if route starts and ends with 'D'
    constraint3 = route[0] == "D" and route[-1] == "D"

    # Check for repeated spots except for 'D'
    constraint4 = len(set(route[1:-1])) == route_length

    return [constraint1, constraint2, constraint3, constraint4]


def fitness_function(route, geo_matrix):
    """
    Calculates the total accumulated Geo for a given route.
    Sums the Geo gains or losses when traveling from one area to another along the route.
    Geo values are obtained from a geo_matrix which is a list of lists.

    Parameters:
        route (list of str): The route taken, represented by area initials.
        geo_matrix (list of lists): A matrix where each list corresponds to an area and contains
                                the Geo changes to all other areas.

    Returns:
    tuple: (total Geo accumulated along the route, jumped_ks flag)
        int: The total Geo accumulated along the route.

    Example Usage:
        route = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']
        geo_matrix = [[0, 10, -20, 30, -40, 50, -60, 70, -80, 90],
                     [-10, 0, -15, 25, -35, 45, -55, 65, -75, 85],
                     [20, 15, 0, 35, -45, 55, -65, 75, -85, 95],
                     [-30, -25, -35, 0, 40, -50, 60, -70, 80, -90],
                     [40, 35, 45, -40, 0, -60, 70, -80, 90, -100],
                     [-50, -45, -55, 50, 60, 0, -70, 80, -90, 100],
                     [60, 55, 65, -60, -70, 70, 0, -90, 100, -110],
                     [-70, -65, -75, 70, 80, -80, 90, 0, -110, 120],
                     [80, 75, 85, -80, -90, 90, -100, 110, 0, -120],
                     [-90, -85, -95, 90, 100, -100, 110, -120, 120, 0]]
        fitness = fitness_function(route, geo_matrix)
        print(fitness)  # Output: 90
    """
    total_geo = 0
    total_geo_without_ks = 0
    skip_ks = False
    jumped_ks = False

    area_to_index = {'D': 0, 'G': 1, 'FC': 2, 'QG': 3, 'CS': 4, 'KS': 5, 'DV': 6, 'SN': 7, 'QS': 8, 'RG': 9}

    # Check route constraints
    constraints = check_constraints(route)
    num_constraints = len(constraints)
    invalid_penalty = -50 * num_constraints

    if all(constraints):
        for i in range(len(route) - 1):
            from_area = area_to_index[route[i]]
            to_area = area_to_index[route[i + 1]]

            if skip_ks:
                skip_ks = False
                continue

            # Handle special case for skipping 'KS' between 'QS' and 'DV'
            if route[i] == 'QS' and route[i + 1] == 'DV':
                skip_ks = True
                jumped_ks = True
                if i > 0:
                    previous_area = area_to_index[route[i-1]]
                    total_geo_without_ks += geo_matrix[previous_area][to_area]
            else:
                total_geo_without_ks += geo_matrix[from_area][to_area]

            total_geo += geo_matrix[from_area][to_area]

        return max(total_geo, total_geo_without_ks), jumped_ks
    else:
        return invalid_penalty, False



def genotypic_diversity(population):
    """
    Calculates the genotypic diversity of a population by comparing the number of different positions between every pair of individuals.
    
    Parameters:
        population (list): A list of individuals in the population.
    
    Returns:
        float: The average number of different positions between individuals in the population.

    Example Usage:
        population = [['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D'],
                     ['D', 'SN', 'QS', 'FC', 'CS', 'DV', 'RG', 'G', 'QG', 'KS', 'D'],
                     ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']]
        diversity = genotypic_diversity(population)
        print(diversity)  # Output: 0.8181818181818182
    """
    num_individuals = len(population)
    num_positions = len(population[0])
    total_diff_positions = 0

    # Compare each pair of individuals
    for i in range(num_individuals - 1):
        for j in range(i + 1, num_individuals):
            # Count differing positions
            total_diff_positions += sum(population[i][k] != population[j][k] for k in range(num_positions))

    # Calculate average number of different positions
    return total_diff_positions / (num_individuals * (num_individuals - 1) / 2)


def individual_genotypic_diversity(individual, population):
    """
    Calculates the genotypic diversity of a single individual by comparing the number of different positions 
    between the individual and every other individual in the population.

    Parameters:
        individual (list): The individual for which the genotypic diversity is to be calculated.
        population (list): A list of individuals in the population.

    Returns:
        float: The average number of different positions between the individual and the rest of the population.

    Example Usage:
        population = [['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D'],
                     ['D', 'SN', 'QS', 'FC', 'CS', 'DV', 'RG', 'G', 'QG', 'KS', 'D'],
                     ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']]
        individual = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']
        diversity = individual_genotypic_diversity(individual, population)
        print(diversity)  # Output: 0.8181818181818182
    """
    num_individuals = len(population)
    num_positions = len(individual)
    total_diff_positions = 0

    # Compare the individual with each other individual in the population
    for other_individual in population:
        # Count differing positions
        total_diff_positions += sum(individual[k] != other_individual[k] for k in range(num_positions))

    # Calculate average number of different positions
    return total_diff_positions / num_individuals

def fitness_shared(population, fitnesses, sigma_share=1.0):
    """
    Calculates the shared fitness of a population based on genotypic diversity.

    Parameters:
        population (list of list of str): The population of routes, where each route is a list of area initials.
        fitnesses (list of float): The fitness values of the population.
        sigma_share (float): The sharing threshold, which normalizes distances and controls the influence range.

    Returns:
        list of float: The shared fitness for each individual in the population.

    Example Usage:
        population = [['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D'],
                     ['D', 'SN', 'QS', 'FC', 'CS', 'DV', 'RG', 'G', 'QG', 'KS', 'D'],
                     ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']]
        fitnesses = [90, 85, 80]
        shared_fitnesses = fitness_shared(population, fitnesses, sigma_share=1.0)
        print(shared_fitnesses)  # Output: [90.0, 85.0, 80.0]
    """
    num_individuals = len(population)

    def linear_sharing_function(distance, sigma_share):
        """
        Linear sharing function that decreases the fitness contribution based on the normalized distance.

        Parameters:
            distance (float): The genotypic distance between two individuals.
            sigma_share (float): The sharing threshold.

        Returns:
            float: The sharing value, which is reduced as the distance increases.

        Example Usage:
            distance = 0.5
            sigma_share = 1.0
            sharing_value = linear_sharing_function(distance, sigma_share)
            print(sharing_value)
        """
        normalized_distance = distance / sigma_share
        if normalized_distance < 1:
            return 1 - normalized_distance
        else:
            return 0

    # Step 1: Calculate the genotypic diversity distances for each individual
    distances = np.zeros(num_individuals)
    for i in range(num_individuals):
        distances[i] = individual_genotypic_diversity(population[i], population)

    # Step 2: Normalize the distances by dividing by the maximum distance
    max_distance = np.max(distances)
    if max_distance > 0:
        distances /= max_distance

    # Step 3: Apply the linear sharing function to each individual's distance
    sharing_coefficients = np.zeros(num_individuals)
    for i in range(num_individuals):
        sharing_coefficients[i] = linear_sharing_function(distances[i], sigma_share)

    # Step 4: Redefine the fitness
    shared_fitnesses = []
    for i in range(num_individuals):
        if sharing_coefficients[i] == 0:
            shared_fitness = fitnesses[i]
        else:
            shared_fitness = fitnesses[i] / (1 + sharing_coefficients[i])
        shared_fitnesses.append(np.round(shared_fitness, 1))

    return shared_fitnesses

def geo_matrix_generator(min_value: int = -500, max_value: int = 500, size: int = 10, seed: int = None) -> list[list[int]]:
    """
    Creates a matrix with biased random values representing Geo gains or losses.
    Diagonal elements are set to zero, indicating no gain/loss within the same area.
    Generate values with a 7% chance of being negative (maintaining the original matrix's ratio of negative values).
    Enforces the value of the edge from 'Greenpath' to 'Forgotten Crossroads' to be 3.2% less than the minimum positive value.

    Parameters:
        min_value (int): Minimum possible value for losses.
        max_value (int): Maximum possible value for gains.
        size (int): Size of the square matrix.
        seed (int): Seed value for random number generation.

    Returns:
        list of lists: A matrix representing the Geo matrix.

    Example Usage:
        matrix = geo_matrix_generator(min_value=-100, max_value=100, size=10, seed=0)
        print(matrix)
    """
    
    if seed is not None:
        np.random.seed(seed)

    # Initialize the matrix with zero values
    matrix = [[0] * size for _ in range(size)]
    index_G = 1  # Index for Greenpath
    index_FC = 2  # Index for Forgotten Crossroads
    positive_values = []

    # Fill the matrix with random values
    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i][j] = 0  # No gain/loss within the same area
            else:
                if i == index_G and j == index_FC:
                    continue  # Skip special case to handle later
                if np.random.rand() < 0.07:
                    matrix[i][j] = np.random.randint(min_value, 0) if min_value < 0 else 0  # 7% chance for negative value
                else:
                    value = np.random.randint(1, max_value + 1)
                    matrix[i][j] = value
                    positive_values.append(value)

    # Enforce the special rule for Greenpath to Forgotten Crossroads
    if positive_values:
        min_positive = min(positive_values)
        geo_G_to_FC = int(min_positive * 0.968)
        matrix[index_G][index_FC] = geo_G_to_FC

    return matrix