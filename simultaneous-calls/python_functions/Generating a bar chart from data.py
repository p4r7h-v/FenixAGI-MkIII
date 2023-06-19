import matplotlib.pyplot as plt

def generate_bar_chart(data, labels, title='Bar Chart', xlabel='Categories', ylabel='Values', display_values=False):
    """
    Generates a bar chart from the given data and labels.

    Args:
    data: list of numeric values.
    labels: list of strings, with the same length as data, representing categories.
    title: string, chart title (default: 'Bar Chart')
    xlabel: string, x-axis label (default: 'Categories')
    ylabel: string, y-axis label (default: 'Values')
    display_values: bool, if True, displays values on top of bars (default: False)

    Returns:
    None
    """

    if len(data) != len(labels):
        print("Error: data and labels should have the same length.")
        return

    fig, ax = plt.subplots()
    bar_width = 0.5
    index = range(len(data))
    bars = ax.bar(index, data, bar_width)

    if display_values:
        for bar in bars:
            x, y = bar.get_xy()
            height = bar.get_height()
            ax.text(x + bar_width/2, height, f'{height}', ha='center', va='bottom')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(index)
    ax.set_xticklabels(labels)

    plt.show()