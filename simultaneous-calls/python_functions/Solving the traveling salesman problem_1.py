import math
import itertools

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def nearest_neighbor_algorithm(cities):
    unvisited_cities = set(cities)
    start_city = unvisited_cities.pop()
    tour = [start_city]

    while unvisited_cities:
        current_city = tour[-1]
        nearest_city = min(unvisited_cities, key=lambda city: distance(current_city, city))
        tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)

    return tour