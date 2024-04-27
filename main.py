#e o main file, o q temos de entregar, so meter codigo final

from genetic_algorithm import GeneticAlgorithm
from config import GAConfig
from visualization import plot_results

def main():
    config = GAConfig()
    
    ga = GeneticAlgorithm(config)
    results = ga.run()
    
    plot_results(results)

if __name__ == "__main__":
    main()
