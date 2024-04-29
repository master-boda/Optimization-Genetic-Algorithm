import random

def generate_individual(areas):
    # Always start and end at Dirtmouth
    route = ['D']
    
    # Possible areas to visit, excluding Dirtmouth and the final node is added later
    possible_areas = areas[:]
    possible_areas.remove('D')
    
    # Shuffle the list to create a random route
    random.shuffle(possible_areas)
    
    # Apply rule: KS can be omitted if DV follows QS immediately
    if 'QS' in possible_areas and 'DV' in possible_areas:
        qs_index = possible_areas.index('QS')
        dv_index = possible_areas.index('DV')
        if abs(qs_index - dv_index) > 1:  # If not immediate, shuffle DV next to QS
            possible_areas.remove('DV')
            possible_areas.insert(qs_index + 1, 'DV')
    
    # Apply rule: Do not visit CS right after QG
    if 'QG' in possible_areas and 'CS' in possible_areas:
        qg_index = possible_areas.index('QG')
        cs_index = possible_areas.index('CS')
        if abs(qg_index - cs_index) == 1:  # If CS is right after QG, swap CS with another area
            # Find a suitable swap candidate that is not immediately after QG
            for i, area in enumerate(possible_areas):
                if area not in ['CS', 'QG'] and i != qg_index + 1:
                    possible_areas[i], possible_areas[cs_index] = possible_areas[cs_index], possible_areas[i]
                    break
    
    # Construct the full route
    route.extend(possible_areas)
    route.append('D')  # End at Dirtmouth
    
    return route

# Define the areas available in the game
areas = ['D', 'G', 'FC', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN', 'QS']

# Generate a population of 10 random individuals
population = [generate_individual(areas) for _ in range(10)]
print(population)

import pandas as pd

# Carregar o dataset
geo_matrix_path = "./Geo_Matrix_Dataset.csv"
geo_matrix_df = pd.read_csv(geo_matrix_path)
geo_matrix_df.set_index("From/To", inplace=True)

# Definir a função de fitness que usa o dataset carregado
def fitness_function(route, geo_matrix):
    total_geo = 0
    
    # Iterar sobre a rota para calcular o ganho líquido de Geo
    for i in range(len(route) - 1):
        from_area = route[i]
        to_area = route[i + 1]
        # Adicionar o ganho de Geo entre duas áreas consecutivas
        total_geo += geo_matrix.loc[from_area, to_area]
    
    return total_geo

# Avaliar uma rota de exemplo usando a função de fitness
example_route = ['D', 'G', 'QS', 'DV', 'RG', 'SN', 'KS', 'QG', 'CS', 'FC', 'D']
route_fitness = fitness_function(example_route, geo_matrix_df)
print(route_fitness)
