import random
def generate_individual(areas):
    """
    Generate a valid game route starting and ending at 'Dirtmouth' ('D') based on provided areas.
    Applies specific game rules to order areas optimally for the route.
    
    Parameters:
    areas (list): List of area identifiers including 'D' for 'Dirtmouth'.
    
    Returns:
    list: A list representing a valid route starting and ending at 'Dirtmouth'.
    """
    # Initialize the route starting at 'Dirtmouth'
    route = ['D']
    
    # Exclude 'Dirtmouth' for route generation
    possible_areas = areas[:]
    possible_areas.remove('D')
    
    # Randomize area order
    random.shuffle(possible_areas)
    
    # Ensure 'DV' follows 'QS' immediately, if both are present
    if 'QS' in possible_areas and 'DV' in possible_areas:
        qs_index = possible_areas.index('QS')
        dv_index = possible_areas.index('DV')
        if abs(qs_index - dv_index) > 1:
            possible_areas.remove('DV')
            possible_areas.insert(qs_index + 1, 'DV')
    
    # Ensure 'CS' does not immediately follow 'QG'
    if 'QG' in possible_areas and 'CS' in possible_areas:
        qg_index = possible_areas.index('QG')
        cs_index = possible_areas.index('CS')
        if abs(qg_index - cs_index) == 1:
            for i, area in enumerate(possible_areas):
                if area not in ['CS', 'QG'] and i != qg_index + 1:
                    possible_areas[i], possible_areas[cs_index] = possible_areas[cs_index], possible_areas[i]
                    break
    
    # Finalize the route
    route.extend(possible_areas)
    route.append('D')  # End at 'Dirtmouth'
    
    return route

# Define the areas available in the game
areas = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN', 'QS']

def population(number):
    """
    Generate a population of individual game routes, each represented as a list.

    Parameters:
    number (int): The number of individual routes to generate.

    Returns:
    list: A list of generated individual game routes.
    """
    # Generate 'number' of individuals using list comprehension
    population = [generate_individual(areas) for _ in range(number)]
    
    return population
