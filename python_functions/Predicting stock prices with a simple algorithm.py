import pandas as pd
import numpy as np

def predict_stock_prices(prices, window_size=3, num_predictions=5):
    """
    Predicts stock prices using a simple moving average algorithm.

    :param prices: A list or Pandas Series of historical stock prices.
    :param window_size: The number of days to consider for the moving average.
    :param num_predictions: The number of future predictions to make.
    :return: A list of predicted stock prices.
    """
    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)

    predictions = []
    for _ in range(num_predictions):
        moving_average = prices[-window_size:].mean()
        predictions.append(moving_average)
        prices = prices.append(pd.Series(moving_average), ignore_index=True)

    return predictions