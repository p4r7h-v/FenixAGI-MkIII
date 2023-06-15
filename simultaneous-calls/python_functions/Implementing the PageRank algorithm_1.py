import numpy as np

def pagerank(links, alpha=0.85, convergence=1e-6, max_iter=100):
    """
    Simplified version of the PageRank algorithm.

    Parameters:
    -----------
    links: List[Tuple[int, int]]
        A list of tuples representing directed links between nodes, where each tuple is (from_node, to_node).
    alpha: float, optional (default=0.85)
        The damping factor.
    convergence: float, optional  (default=1e-6)
        The convergence threshold.
    max_iter: int, optional (default=100)
        The maximum number of iterations.

    Returns:
    --------
    ranks: numpy array
        The PageRank values of each node.
    """
    # Find unique node IDs and their counts
    nodes, outlinks_count = np.unique(np.array(links), return_counts=True)

    # Number of nodes
    N = len(nodes)

    # Initialize the PageRank vector
    ranks = np.ones(N) / N

    # Initialize the transition matrix
    P = np.zeros((N, N))

    # Populate the transition matrix
    for from_node, to_node in links:
        P[to_node, from_node] = 1.0 / outlinks_count[from_node]

    # Iterate until convergence or max iterations reached
    for _ in range(max_iter):
        new_ranks = alpha * P.dot(ranks) + (1 - alpha) / N
        if np.linalg.norm(new_ranks - ranks) < convergence:
            break
        ranks = new_ranks

    return ranks