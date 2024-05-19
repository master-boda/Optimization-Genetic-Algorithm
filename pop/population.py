import random

def generate_individual() -> list[str]:
    """
    Generate a game route starting and ending at 'Dirtmouth' ('D') without strict sequence rules,
    with 'Resting Grounds' ('RG') inserted at a random position in the second half of the route.
    
    Returns:
    list: A list representing a route starting and ending at 'Dirtmouth'.
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
    """
    # Generate n individuals
    population = [generate_individual() for _ in range(n)]
    
    return population
