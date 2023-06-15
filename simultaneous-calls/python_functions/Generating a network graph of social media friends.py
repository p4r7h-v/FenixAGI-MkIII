import networkx as nx
import matplotlib.pyplot as plt

def generate_social_network_graph(friend_pairs):
    # Initialize an empty graph
    G = nx.Graph()

    # Add nodes and edges to the graph
    for a, b in friend_pairs:
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')

    # Save the graph to an image file
    plt.savefig("social_network_graph.png")

    # Show the graph
    plt.show()

# Example usage
friend_pairs = [
    ("Alice", "Bob"),
    ("Bob", "Carol"),
    ("Carol", "Diana"),
    ("Diana", "Alice"),
    ("Emily", "Bob")
]

generate_social_network_graph(friend_pairs)