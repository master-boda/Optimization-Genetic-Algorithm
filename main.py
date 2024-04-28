from config import GAConfig
from optimization_problem import OptimizationProblem
from genetic_algorithm import GeneticAlgorithm

def objective_function(solution):
    return sum(solution)  # Uma função objetivo simples para exemplo

def main():
    config = GAConfig()
    problem = OptimizationProblem(objective_function)
    ga = GeneticAlgorithm(config, problem)
    best_solution = ga.run()
    print("Melhor solução encontrada:", best_solution)

if __name__ == "__main__":
    main()
