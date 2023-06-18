import numpy as np
import noise

def generate_terrain(width, height, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
    """
    Generate a procedural terrain heightmap using Perlin noise.
    
    :param width: Width of the terrain
    :param height: Height of the terrain
    :param scale: Noise scale (larger value results in larger terrain features)
    :param octaves: Number of noise layers to combine
    :param persistence: Controls the amplitude of each octave (lower value results in smoother terrain)
    :param lacunarity: Controls the frequency of each octave (higher value results in more detailed terrain)
    :param seed: Optional random seed for generating the noise
    :return: 2D NumPy array containing terrain height values (0-1)
    """
    if seed is not None:
        np.random.seed(seed)
    base = np.random.randint(0, 10000)
    
    heightmap = np.zeros((height, width), dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            nx = (x + base) / scale
            ny = (y + base) / scale
            heightmap[y, x] = noise.pnoise2(nx, ny, octaves, persistence, lacunarity)

    # Normalize heightmap values to the range 0-1
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    
    return heightmap