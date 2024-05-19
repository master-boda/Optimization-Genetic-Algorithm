# Genetic Algorithms for Optimizing In-Game Routing in Hollow Knight

This project explores and optimizes the use of Genetic Algorithms (GAs) for solving complex routing problems, specifically aiming to maximize in-game currency (Geo) earnings for a specified set of routes in the game Hollow Knight. The project involves implementing and testing various genetic operators, including different types of crossover and mutation functions, and executing a comprehensive grid search to determine the optimal configurations. The output includes the best route with the highest Geo earnings, a detailed analysis of phenotypic and genotypic diversity across generations, and a dynamic dashboard for visualizing the results. This project showcases the integration of theoretical knowledge, programming skills, and creative problem-solving in the field of optimization algorithms.

## Project Content

### Directories and Files

**Main Directory (`main`)**
- `__pycache__`
- `__init__.py`
- `genetic_algorithm.py`

**Operators Directory (`operators`)**
- `__pycache__`
- `__init__.py`
- `crossovers.py`
- `mutators.py`
- `optimizations.py`
- `selection_algorithms.py`

**Population Directory (`pop`)**
- `__pycache__`
- `__init__.py`
- `population.py`

**Tests Directory (`tests`)**
- `__pycache__`
- `__init__.py`
- `test_crossover.py`
- `test_mut.py`

**Utilities Directory (`utils`)**
- `__pycache__`
- `__init__.py`
- `utils.py`

**Visualizations Directory (`visualizations`)**
- `__pycache__`
- `dashboard.py`
- `visualization.py`

### Other Files
- `.gitattributes`
- `crossovers.md`
- `Geo_Matrix_Dataset.csv`
- `grid_search_results.csv`
- `gridsearch.py`
- `main.py`
- `ReadMe.md`
- `requirements.txt`

## Instructions

### Install Requirements
```bash
pip install -r requirements.txt
```

### Running the Algorithm

1. **Open `main.py`**
   ```python
   # Insert your matrix (list of lists) in matrix_to_use
   # If you want to use one of ours set it to 'None'
   ```

2. **Execute the Script**
   ```bash
   python main.py
   ```

3. **Output Explanation**
   ```
   ----------------------------------------
   Generation 49 best fitness : 3893
   ----------------------------------------
   Best individual: ['D', 'G', 'SN', 'FC', 'DV', 'KS', 'QS', 'CS', 'RG', 'QG', 'D']
   Phenotypic Diversity: 549.32
   Genotypic Diversity: 7.14
   ----------------------------------------
   ```

4. **Visualization**
   After running the script, a window with an animation of the routes will open.
   When you close it the Dashboard will initialize!

### Dashboard Initialization

1. **Run the Dashboard**
   ```bash
   # The dashboard will be running on http://127.0.0.1:8050
   ```

2. **Open the Browser**
   - Paste `http://127.0.0.1:8050` in your browser to explore the dashboard.

   ```
   127.0.0.1 - - [DD/MM/YYYY hh:mm:ss] "POST /_dash-update-component HTTP/1.1" 200 - outputs this everytime tou call the @app.callback
   ```

## Explore the Dashboard!
- Visualize the optimization process and results.
- Analyze phenotypic and genotypic diversity across generations.
- Interact with dynamic graphs and charts to gain insights into the algorithm's performance.

---

This project provides a comprehensive framework for optimizing routing problems using Genetic Algorithms, with a specific focus on maximizing in-game currency earnings in Hollow Knight. The integration of various genetic operators, extensive testing, and dynamic visualizations offers a robust and insightful approach to solving complex optimization problems.
```