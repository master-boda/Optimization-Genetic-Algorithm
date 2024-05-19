import random

def generate_individual() -> list[str]:
    """
    Generate a game route starting and ending at 'Dirtmouth' ('D') without strict sequence rules.
        
    Returns:
    list: A list representing a route starting and ending at 'Dirtmouth'.

    Example Usage:
    generate_individual()
    # Output: ['D', 'FC', 'G', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']
    """
    # define the areas in the game
    areas = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG']

    # initialize the route starting at 'Dirtmouth'
    route = ['D']
    
    # exclude 'Dirtmouth' for route generation
    possible_areas = [area for area in areas if area != 'D']
    
    random.shuffle(possible_areas)

    route.extend(possible_areas)
    route.append('D') # end at 'Dirtmouth'
    
    return route

def population(n: int) -> list[list[str]]:
    """
    Generate a population of individual game routes, each represented as a list.

    Parameters:
    number (int): The number of individual routes to generate.

    Returns:
    list: A list of generated individual game routes.

    Example Usage:
    population(5)
    # Output: [['D', 'FC', 'G', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']
    #          ['D', 'SN', 'QS', 'FC', 'CS', 'DV', 'RG', 'G', 'QG', 'KS', 'D']
    #          ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']
    #          ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']
    #          ['D', 'FC', 'G', 'QG', 'CS', 'KS', 'DV', 'SN', 'QS', 'RG', 'D']]
    """
    # Generate n individuals
    population = [generate_individual() for _ in range(n)]
    
    return population
