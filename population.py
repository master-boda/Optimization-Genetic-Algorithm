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
    # define the areas in the game
    areas = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN', 'QS']

    # initialize the route starting at 'Dirtmouth'
    route = ['D']
    
    # exclude 'Dirtmouth' for route generation
    possible_areas = areas[:]
    possible_areas.remove('D')
    
    # randomize area order
    random.shuffle(possible_areas)
    
    # make sure 'DV' follows 'QS' immediately, if both are present
    if 'QS' in possible_areas and 'DV' in possible_areas:
        qs_index = possible_areas.index('QS')
        dv_index = possible_areas.index('DV')
        if abs(qs_index - dv_index) > 1:
            possible_areas.remove('DV')
            possible_areas.insert(qs_index + 1, 'DV')
    
    # make sure 'CS' does not immediately follow 'QG'
    if 'QG' in possible_areas and 'CS' in possible_areas:
        qg_index = possible_areas.index('QG')
        cs_index = possible_areas.index('CS')
        if abs(qg_index - cs_index) == 1:
            for i, area in enumerate(possible_areas):
                if area not in ['CS', 'QG'] and i != qg_index + 1:
                    possible_areas[i], possible_areas[cs_index] = possible_areas[cs_index], possible_areas[i]
                    break
    
    # finalize the route
    route.extend(possible_areas)
    route.append('D')  # end at 'Dirtmouth'
    
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
