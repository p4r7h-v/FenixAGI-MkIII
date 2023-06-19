import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def visualize_high_dimensional_data(data, n_components=2, perplexity=30, learning_rate=200, random_state=None, plot=True):
    """
    Visualize high-dimensional data using t-SNE.

    :param data: ndarray, shape (n_samples, n_features)
        The input data.
    :param n_components: int (default: 2)
        The number of dimensions to reduce the data to.
    :param perplexity: float (default: 30)
        The t-SNE perplexity parameter.
    :param learning_rate: float (default: 200)
        The t-SNE learning rate parameter.
    :param random_state: int or RandomState instance or None, optional (default: None)
        The random_state parameter for t-SNE.
    :param plot: bool (default: True)
        If True, the transformed data will be plotted in a scatter plot.
    :returns: ndarray, shape (n_samples, n_components)
        The reduced-dimension data.
    """
    tsne = TSNE(n_components=n_components, perplexity=perplexity, learning_rate=learning_rate, random_state=random_state)
    reduced_data = tsne.fit_transform(data)

    if plot:
        plt.scatter(reduced_data[:, 0], reduced_data[:, 1])
        plt.xlabel('t-SNE Component 1')
        plt.ylabel('t-SNE Component 2')
        plt.title('t-SNE visualization of high-dimensional data')
        plt.show()

    return reduced_data