import random
def generate_individual():
    """
    Generate a valid game route starting and ending at 'Dirtmouth' ('D') based on provided areas.
    Applies route ordering rules included in the Project Description.
    
    Parameters:
    areas (list): List of area identifiers including 'D' for 'Dirtmouth'.
    
    Returns:
    list: A list representing a valid route starting and ending at 'Dirtmouth'.
    """
    # Define the areas in the game
    areas = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN', 'QS']

    # Initialize the route starting at 'Dirtmouth'
    route = ['D']
    
    # Exclude 'Dirtmouth' and 'Resting Grounds' for route generation
    possible_areas = [area for area in areas if area not in ['D', 'RG']]
    
    # Randomize area order
    random.shuffle(possible_areas)
    
    # Enforce 'DV' follows 'QS' immediately
    if 'QS' in possible_areas and 'DV' in possible_areas:
        qs_index = possible_areas.index('QS')
        dv_index = possible_areas.index('DV')
        if abs(qs_index - dv_index) > 1:
            possible_areas.remove('DV')
            possible_areas.insert(qs_index + 1, 'DV')
    
    # Prevent 'CS' from immediately following 'QG'
    if 'QG' in possible_areas and 'CS' in possible_areas:
        qg_index = possible_areas.index('QG')
        cs_index = possible_areas.index('CS')
        if abs(qg_index - cs_index) == 1:
            for i, area in enumerate(possible_areas):
                if area not in ['CS', 'QG'] and i != qg_index + 1:
                    possible_areas[i], possible_areas[cs_index] = possible_areas[cs_index], possible_areas[i]
                    break

    # Determine the halfway point to add 'RG'
    half_point = len(possible_areas) // 2
    possible_areas.insert(half_point, 'RG')
    
    # Finalize the route
    route.extend(possible_areas)
    route.append('D')  # End at 'Dirtmouth'
    
    return route


def population(n):
    """
    Generate a population of individual game routes, each represented as a list.

    Parameters:
    number (int): The number of individual routes to generate.

    Returns:
    list: A list of generated individual game routes.
    """
    # generate n individuals
    population = [generate_individual() for _ in range(n)]
    
    return population
