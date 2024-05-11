import numpy as np
import pandas as pd

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
    for i in range(len(route) - 1):
        from_area = route[i]
        to_area = route[i + 1]
        total_geo += geo_matrix.loc[from_area, to_area]
    return total_geo


def geo_matrix(min_value=-500, max_value=500, original=False):
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

    # return the original matrix if original is True
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