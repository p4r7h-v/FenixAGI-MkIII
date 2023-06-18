import sys
from math import sqrt


def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def find_nearest_neighbor(p, unvisited):
    nearest_point = None
    min_distance = sys.maxsize

    for point in unvisited:
        if distance(p, point) < min_distance:
            nearest_point = point
            min_distance = distance(p, point)

    return nearest_point


def traveling_salesman(cities):
    starting_city = cities[0]
    route = [starting_city]
    unvisited = cities.copy()

    for _ in cities:
        current = route[-1]
        nearest_point = find_nearest_neighbor(current, unvisited)
        unvisited.remove(current)
        route.append(nearest_point)

    route.append(starting_city)

    return route


if __name__ == "__main__":
    cities = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 0)]
    solution = traveling_salesman(cities)
    print("The route using the nearest neighbor heuristic: ", solution)