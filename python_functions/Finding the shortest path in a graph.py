import heapq

def find_shortest_path(graph, start, end):
    """
    Finds the shortest path between the start and end nodes in a graph using Dijkstra's Algorithm.

    :param graph: Graph represented as a dictionary of nodes and their corresponding adjacent nodes and weights.
                  For example: {'A': {'B': 1, 'C': 4}, 'B': {'A': 1, 'C': 2, 'D': 5}, 'C': {'A': 4, 'B': 2, 'D': 1}, 'D': {'B': 5, 'C': 1}}
    :param start: The starting node in the graph.
    :param end: The ending node in the graph.
    :return: A tuple containing the shortest distance and the shortest path as a list of nodes.
    """

    # Initialize distance dictionary with infinite values for all nodes except the start node
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    # Initialize priority queue with the starting node
    priority_queue = [(0, start)]

    # Initialize dictionary to store the shortest path
    shortest_path = {}

    while priority_queue:
        # Get the node with the minimum distance from the priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        # If the current distance is greater than the recorded distance, skip this node
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            # Calculate the distance from the current node to the neighboring node
            distance = current_distance + weight

            # Update the distances dictionary if the calculated distance is less than the recorded distance
            if distance < distances[neighbor]:
                # Update the distance in the distances dictionary
                distances[neighbor] = distance
                # Update the shortest path from the start node to the neighbor
                shortest_path[neighbor] = current_node
                # Add the neighbor and its distance to the priority queue
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct the shortest path from start to end
    path = [end]
    while path[-1] != start:
        path.append(shortest_path[path[-1]])
    path.reverse()

    return distances[end], path