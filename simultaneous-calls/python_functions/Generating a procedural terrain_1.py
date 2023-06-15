import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2

def generate_procedural_terrain(width, height, scale=10, octaves=6, persistence=0.5, lacunarity=2.0, seed=42):
    """
    Generate a procedural terrain using Perlin noise.

    Args:
        width (int): Width of the terrain
        height (int): Height of the terrain
        scale (float): Scale factor for noise
        octaves (int): Number of octaves for noise
        persistence (float): Persistence for noise
        lacunarity (float): Lacunarity for noise
        seed (int): Seed for random number generation

    Returns:
        np.ndarray: A 2D numpy array representing the terrain
    """

    terrain = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            terrain[y][x] = snoise2(
                x * scale / width, y * scale / height,
                octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=seed
            )
    return terrain

terrain = generate_procedural_terrain(256, 256, scale=80)
plt.imshow(terrain, cmap='gray')
plt.show()