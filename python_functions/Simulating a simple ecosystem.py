import random

def simulate_ecosystem(plants, herbivores, carnivores, days):
    for day in range(days):
        # Plants grow
        plants += random.randint(1, 5)

        # Herbivores reproduce and eat plants
        herbivores += random.randint(0, herbivores)
        plants_to_eat = min(plants, int(herbivores * 0.5))
        herbivores -= max(0, int((plants_to_eat - herbivores) * 0.5))
        plants -= plants_to_eat

        # Carnivores reproduce and eat herbivores
        carnivores += random.randint(0, carnivores)
        herbivores_to_eat = min(herbivores, int(carnivores * 0.3))
        carnivores -= max(0, int((herbivores_to_eat - carnivores) * 0.3))
        herbivores -= herbivores_to_eat

        # Print the status of the ecosystem
        print(f"Day {day + 1}:")
        print(f"  Plants: {plants}")
        print(f"  Herbivores: {herbivores}")
        print(f"  Carnivores: {carnivores}")

# Example usage
simulate_ecosystem(plants=100, herbivores=5, carnivores=2, days=10)