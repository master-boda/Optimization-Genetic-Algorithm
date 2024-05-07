import numpy as np
import pandas as pd

def fitness_function(route, geo_matrix):
    """
    Calculate the total Geo (in-game currency) accumulated based on a given route.

    This function computes the total Geo accumulated as the player moves from one area to another
    along a specified route. The Geo values between areas are retrieved from a matrix that defines
    the Geo gain or loss when traveling from one area to another.

    Parameters:
    route (list of str): A list of area identifiers representing the route taken.
    geo_matrix (DataFrame): A pandas DataFrame where indices and columns are area identifiers,
                            and values are the Geo gained or lost when moving from index (from_area)
                            to column (to_area).

    Returns:
    int: The total Geo accumulated over the given route.
    """
    total_geo = 0
    for i in range(len(route) - 1):
        from_area = route[i]
        to_area = route[i + 1]
        total_geo += geo_matrix.loc[from_area, to_area]
    return total_geo


areas = ["D", "FC", "G", "QS", "QG", "CS", "KS", "RG", "DV", "SN"]


def geo_matrix(labels, min_value=-500, max_value=500):
    """
    Creates a matrix with biased random values representing Geo gains or losses.
    Diagonal elements are set to zero, indicating no gain/loss within the same area.
    The probability of a negative value is 7%, because in the matrix given in the project instructions 
    there was 7 negative values in a total of 100 values. 

    Parameters:
        labels (list): List of labels representing the areas.
        min_value (int): Minimum possible value for losses.
        max_value (int): Maximum possible value for gains.

    Returns:
        pd.DataFrame: A pandas DataFrame representing the Geo matrix with labels.
    """
    size = len(labels)
    matrix = np.zeros((size, size), dtype=int)


    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i, j] = 0
            else:
                matrix[i, j] = np.random.randint(min_value, 0) if np.random.rand() < 0.07 else np.random.randint(1, max_value + 1) #sets up the 7% odd of being a negative number

    return pd.DataFrame(matrix, index=labels, columns=labels)

