import numpy as np
import pandas as pd

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
    Geo values are obtained from a Geo matrix.

    Parameters:
    route (list of str): The route taken, represented by letters representing areas in the game.
    geo_matrix (DataFrame): A DataFrame where indices and columns represent areas, and values indicate Geo changes between areas.

    Returns:
    int: The total Geo accumulated along the route.
    """

    total_geo = 0
    total_geo_without_ks = 0
    skip_ks = False

    for i in range(len(route) - 1):
        from_area = route[i]
        to_area = route[i + 1]

        if skip_ks:
            skip_ks = False
            continue

        if from_area == "QS" and to_area == "DV":
            skip_ks = True
            total_geo_without_ks += geo_matrix.loc[route[i-1], to_area]
        else:
            total_geo_without_ks += geo_matrix.loc[from_area, to_area]

        total_geo += geo_matrix.loc[from_area, to_area]

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
        pd.DataFrame: A pandas DataFrame representing the Geo matrix.
    """
    # import the original Geo matrix from the Project Description
    df_original = pd.read_csv('Geo_Matrix_Dataset.csv', index_col='From/To')
    # extract area labels
    labels = df_original.index.tolist()

    if original:
        return df_original
    
    size = len(labels)
    matrix = np.zeros((size, size), dtype=int)

    index_G = labels.index('G')
    index_FC = labels.index('FC')

    positive_values = []

    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i, j] = 0
            else:
                # exclude G to FC initially
                if i == index_G and j == index_FC:
                    continue

                # generate values with a 7% chance of being negative (maintaining the original ratio of negative values)
                if np.random.rand() < 0.07:
                    matrix[i, j] = np.random.randint(min_value, 0) if min_value < 0 else 0
                else:
                    value = np.random.randint(1, max_value + 1)
                    matrix[i, j] = value
                    positive_values.append(value)

    # minimum positive value
    min_positive = min(positive_values)

    # calculate G to FC as 3.2% less than the minimum positive value
    geo_G_to_FC = int(min_positive * 0.968)

    matrix[index_G, index_FC] = geo_G_to_FC

    return pd.DataFrame(matrix, index=labels, columns=labels)