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
