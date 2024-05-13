import numpy as np

def check_constraints(route):
    # length of the route ignoring Dirtmouth endpoints
    route_length = len(route) - 2
    
    # check for "RG" in the second half of the route
    rg_index = route.index('RG') if 'RG' in route else -1
    constraint1 = rg_index >= len(route) // 2

    # check for sequence "QS"-"DV" (KS will always be present in the route simultaneously :O)
    qs_dv_sequence = any(route[i] == 'QS' and route[i+1] == 'DV' for i in range(route_length))
    constraint2 = not qs_dv_sequence

    # check for sequence "QG"-"CS"
    qg_cs_sequence = any(route[i] == 'QG' and route[i+1] == 'CS' for i in range(route_length))
    constraint3 = not qg_cs_sequence

    return constraint1 and constraint2 and constraint3

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

    area_to_index = {'D': 0, 'G': 1, 'FC': 2, 'QG': 3, 'CS': 4, 'KS': 5, 'DV': 6, 'SN': 7, 'QS': 8}

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



def geo_matrix_generator(min_value=-500, max_value=500, original=False):
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

    Returns:
        list of lists: A matrix representing the Geo matrix.
    """
    # Simulated loading of the original matrix from the description.
    # This should be replaced with actual code to load the matrix if needed.
    labels = ['Dirtmouth', 'Greenpath', 'Forgotten Crossroads', 'Queen\'s Station', 
              'Queen\'s Gardens', 'City Storerooms', 'King\'s Station', 'Resting Grounds',
              'Distant Village', 'Stag Nest']
    
    if original:
        # Placeholder for actual original matrix load
        return [[0]*len(labels) for _ in labels]

    size = len(labels)
    matrix = [[0]*size for _ in range(size)]

    index_G = labels.index('Greenpath')
    index_FC = labels.index('Forgotten Crossroads')

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



print(geo_matrix_generator(-500, 500))