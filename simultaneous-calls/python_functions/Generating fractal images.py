import numpy as np
from PIL import Image

def mandelbrot_image(width, height, max_iterations=1000, x_range=(-2, 1), y_range=(-1, 1)):
    # Initialize an empty image with the desired width and height.
    image = Image.new("RGB", (width, height), "white")
    pixels = image.load()

    # Calculate the scaling factors based on the desired width, height, and range.
    x_scale = float(x_range[1] - x_range[0]) / width
    y_scale = float(y_range[1] - y_range[0]) / height
    
    for x in range(width):
        real = x_scale * x + x_range[0]
        for y in range(height):
            imag = y_scale * y + y_range[0]

            # Initialize the complex number for the Mandelbrot set calculation.
            z = complex(real, imag)
            c = z

            # Iteratively perform the Mandelbrot set calculation.
            for iteration in range(max_iterations):
                if abs(z) > 2:
                    break
                z = z*z + c

            # Set the pixel color based on the number of iterations.
            color = (iteration % 8 * 32, iteration % 16 * 16, iteration % 32 * 8)
            pixels[x, y] = color

    # Show the generated fractal image.
    image.show()

# Example usage:
mandelbrot_image(800, 800)