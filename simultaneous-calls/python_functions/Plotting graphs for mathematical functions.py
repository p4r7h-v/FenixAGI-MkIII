import matplotlib.pyplot as plt
import numpy as np

def plot_function(function, x_min=-10, x_max=10, num_points=1000):
    """
    Plots a mathematical function over a specified range.

    Parameters:
    - function: The mathematical function to plot. This should be a function that takes a single argument (x) and returns a value (y).
    - x_min: The minimum x value for the plot range.
    - x_max: The maximum x value for the plot range.
    - num_points: The number of points to sample the mathematical function over the specified range.

    Returns:
    None
    """
    x = np.linspace(x_min, x_max, num_points)
    y = function(x)

    plt.plot(x, y)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Plot of the mathematical function")
    plt.grid(True)
    plt.show()

# Example usage:
import math
plot_function(math.sin, x_min=0, x_max=2*math.pi)