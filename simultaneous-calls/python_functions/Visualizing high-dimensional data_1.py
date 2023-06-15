import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def visualize_high_dimensional_data(data, labels=None, perplexity=30, n_components=2, random_state=None):
    """
    Visualizes high-dimensional data using t-SNE algorithm for dimensionality reduction.

    :param data: numpy array, high-dimensional data with shape (n_samples, n_features)
    :param labels: Optional, numpy array, labels for each data point with shape (n_samples,)
    :param perplexity: int, optional (default=30), the perplexity parameter for t-SNE, which balances local and global aspects of the data
    :param n_components: int, optional (default=2), dimension of the embedded space (usually set to 2 or 3 for visualization purposes)
    :param random_state: int, optional, random_state parameter for reproducibility
    :return: None
    """
    # Apply t-SNE to the data
    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state)
    reduced_data = tsne.fit_transform(data)

    # Create a scatter plot of the reduced data
    plt.figure()
    if labels is None:
        plt.scatter(reduced_data[:, 0], reduced_data[:, 1])
    else:
        unique_labels = np.unique(labels)
        for label in unique_labels:
            plt.scatter(reduced_data[labels == label, 0], reduced_data[labels == label, 1], label=label)
        plt.legend()  # Show a legend if labels exist
    plt.xlabel("t-SNE 1")
    plt.ylabel("t-SNE 2")
    plt.title("Visualization of high-dimensional data using t-SNE")
    plt.show()