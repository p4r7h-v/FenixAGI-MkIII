import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def predict_flight_delays(data, target):
    """
    Predict flight delays using Linear Regression.
    
    :param data: Feature data (X) for flights - an array or pandas DataFrame.
    :param target: Target data (Y) with actual delays - an array or pandas Series.
    :return: A tuple containing the trained Linear Regression model, mean squared error, and R2 score.
    """

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)

    # Create and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions using the test set
    y_pred = model.predict(X_test)

    # Calculate the mean squared error and R2 score
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return model, mse, r2