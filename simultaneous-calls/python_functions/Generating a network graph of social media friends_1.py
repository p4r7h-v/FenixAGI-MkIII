import networkx as nx
import matplotlib.pyplot as plt

def generate_social_network_graph(friends_list):
    """
    Generates a network graph of social media friends.

    :param friends_list: List of tuples containing pairs of friends
    :type friends_list: list of tuples
    """

    # Create an empty graph
    G = nx.Graph()

    # Add edges to the graph
    for friend_pair in friends_list:
        G.add_edge(friend_pair[0], friend_pair[1])

    # Draw the graph
    nx.draw(G, with_labels=True, node_color="skyblue", font_weight="bold")
    plt.title("Social Media Network Graph")
    plt.show()