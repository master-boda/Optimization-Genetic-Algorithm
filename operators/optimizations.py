from utils.utils import fitness_function

def two_opt(route, geo_matrix, max_iterations=25):
    best_route = route[:]
    improved = False
    iteration = 0

    while not improved and iteration < max_iterations:
        improved = False
        best_fit = fitness_function(best_route, geo_matrix)
        # keep endpoints fixed
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1:
                    continue  # dont need to swap adjacent elements
                new_route = best_route[:]
                # reverse the segment between i and j+1
                new_route[i:j + 1] = reversed(new_route[i:j + 1])
                new_fit = fitness_function(new_route, geo_matrix)
                if new_fit > best_fit:
                    best_route = new_route
                    best_fit = new_fit
                    improved = True
                    break
            if improved:
                break
        iteration += 1

    return best_route