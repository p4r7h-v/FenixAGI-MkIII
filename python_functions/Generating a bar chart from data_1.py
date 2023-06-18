import matplotlib.pyplot as plt

def generate_bar_chart(data, labels, title='Bar Chart', xlabel='X-axis', ylabel='Y-axis', color='blue'):
    """
    Generates a bar chart from the given data.

    :param data: A list of numerical values representing the height of each bar
    :param labels: A list of string values representing the labels for each bar
    :param title: The title of the bar chart (optional)
    :param xlabel: The label for the x-axis (optional)
    :param ylabel: The label for the y-axis (optional)
    :param color: The color of the bars (optional)
    """
    if len(data) != len(labels):
        raise ValueError("Data and labels lists must have the same length")

    # Create the bar chart
    plt.bar(labels, data, color=color)

    # Customize the chart
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # Display the chart
    plt.show()

# Example usage:
data = [10, 20, 30, 40, 50]
labels = ['A', 'B', 'C', 'D', 'E']
generate_bar_chart(data, labels, title='Sample Bar Chart', xlabel='Categories', ylabel='Values', color='green')