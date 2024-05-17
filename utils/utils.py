import numpy as np

def check_constraints(route):
    # length of the route ignoring Dirtmouth endpoints
    route_length = len(route) - 2
    
    # check for "RG" in the second half of the route
    rg_index = route.index('RG') if 'RG' in route else -1
    constraint1 = rg_index >= len(route) // 2

    # check if "CS" is not after "QG"
    constraint2 = not ('QG' in route and 'CS' in route and route.index('CS') > route.index('QG'))

    # check if route starts and ends with "D"
    constraint3 = route[0] == "D" and route[-1] == "D"

    return [constraint1, constraint2, constraint3]

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
    int: The total Geo accumulated along the route.
    """
    total_geo = 0
    total_geo_without_ks = 0
    skip_ks = False

    area_to_index = {'D': 0, 'G': 1, 'FC': 2, 'QG': 3, 'CS': 4, 'KS': 5, 'DV': 6, 'SN': 7, 'QS': 8, 'RG': 9}

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

            if route[i] == 'QS' and route[i + 1] == 'DV':
                skip_ks = True
                # Ensure there was a previous area in the route
                if i > 0:
                    previous_area = area_to_index[route[i-1]]
                    total_geo_without_ks += geo_matrix[previous_area][to_area]
            else:
                total_geo_without_ks += geo_matrix[from_area][to_area]

            total_geo += geo_matrix[from_area][to_area]

        return max(total_geo, total_geo_without_ks)
    else:
        return invalid_penalty





def geo_matrix_generator(min_value: int = -500, max_value: int = 500, size: int = 10, seed: int = None) -> list[list[int]]:
    """
    If original is True, returns the original Geo matrix given in the Project Description.
    Creates a matrix with biased random values representing Geo gains or losses.
    Diagonal elements are set to zero, indicating no gain/loss within the same area.
    Generate values with a 7% chance of being negative (maintaining the original matrix's ratio of negative values)
    Enforces the value of the edge from 'Greenpath' to 'Forgotten Crossroads' to be 3.2% less than the minimum positive value.

    Parameters:
        min_value (int): Minimum possible value for losses.
        max_value (int): Maximum possible value for gains.
        original (bool): Whether to return the original matrix.
        seed (int): Seed value for random number generation.

    Returns:
        list of lists: A matrix representing the Geo matrix.
    """

    if seed is not None:
        np.random.seed(seed)

    matrix = [[0]*size for _ in range(size)]

    index_G = 1
    index_FC = 2

    positive_values = []

    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i][j] = 0
            else:
                if i == index_G and j == index_FC:
                    continue
                if np.random.rand() < 0.07:
                    matrix[i][j] = np.random.randint(min_value, 0) if min_value < 0 else 0
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

def genotypic_diversity(population):
    """
    Calculates the genotypic diversity of a population by comparing the number of different positions between every pair of individuals.
    Parameters:
    population (list): A list of individuals in the population.
    Returns:
    float: The average number of different positions between individuals in the population.
    """
    num_individuals = len(population)
    num_positions = len(population[0])
    total_diff_positions = 0

    for i in range(num_individuals - 1):
        for j in range(i + 1, num_individuals):
            total_diff_positions += sum(population[i][k] != population[j][k] for k in range(num_positions))

    return total_diff_positions / (num_individuals * (num_individuals - 1) / 2)