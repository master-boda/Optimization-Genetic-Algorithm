import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the areas and their coordinates
areas = ["D", "FC", "G", "QS", "QG", "CS", "KS", "RG", "DV", "SN"]
coordinates = {
    "D": (0, 0),
    "FC": (1, 2),
    "G": (3, 3),
    "QS": (4, 1),
    "QG": (6, 2),
    "CS": (7, 4),
    "KS": (9, 0),
    "RG": (5, 6),
    "DV": (2, 7),
    "SN": (8, 5)
}

def plot_route(route, ax, title, color='skyblue'):
    """
    Plots a single route on the given axes with enhanced aesthetics.

    Parameters:
        - route (list of str): The route to be plotted, represented by area initials.
        - ax (matplotlib.axes._subplots.AxesSubplot): The matplotlib axes to plot on.
        - title (str): The title of the plot.
        - color (str): The color of the route line.

    Returns:
        - None: Displays the route on the provided axes.
    Example Usage:
        route = ['D', 'FC', 'G', 'QS', 'QG', 'CS', 'KS', 'RG', 'DV', 'SN']
        plot_route(route, ax, 'Best Route', color='limegreen')
    """
    x = [coordinates[area][0] for area in route]
    y = [coordinates[area][1] for area in route]
    ax.clear()
    ax.plot(x, y, marker='o', markersize=8, markerfacecolor='blue', markeredgewidth=2, markeredgecolor='black', color=color, linewidth=2)
    for area in route:
        ax.text(coordinates[area][0], coordinates[area][1], area, fontsize=12, ha='right', color='darkred', fontweight='bold')
    ax.set_xlabel('X Coordinate', fontsize=14)
    ax.set_ylabel('Y Coordinate', fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 8)

def visualize_routes(routes, best_route, interval=500):
    """
    Visualizes routes over generations with enhanced aesthetics using matplotlib animation.

    Parameters:
        - routes (list of list of str): A list of routes for each generation.
        - best_route (list of str): The best route found.
        - interval (int): The interval between frames in milliseconds.

    Returns:
        - None: Displays the animated visualization of routes over generations.

    Example Usage:
        visualize_routes(routes, best_route, interval=500)

    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    def update(num):
        """
        Updates the plots for each frame of the animation.

        Parameters:
            - num (int): The current frame number.

        Returns:
            - None: Updates the route plots for the current generation.

        Example Usage:
            update(1)      

        """
        plot_route(routes[num], ax1, f"Generation {num+1}")
        plot_route(best_route, ax2, "Best Route", color='limegreen')
    
    ani = animation.FuncAnimation(fig, update, frames=len(routes), interval=interval)
    plt.show()
