import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def predict_house_prices(features, house_prices):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, house_prices, test_size=0.2, random_state=42)

    # Create and train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Return the test set predictions alongside their actual prices
    return list(zip(predictions, y_test))


# Example usage:
features = np.array([[2000, 3, 2], [2500, 4, 2.5], [1800, 3, 1.5], [1500, 2, 1], [3000, 5, 3]])
house_prices = np.array([500000, 600000, 400000, 300000, 800000])

predictions_and_actuals = predict_house_prices(features, house_prices)
print(predictions_and_actuals)