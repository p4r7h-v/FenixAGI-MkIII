import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def run_logistic_regression(X, y, test_size=0.2, random_state=None):
    """
    Run logistic regression on the given dataset.

    Parameters:
    X (array-like): Feature data for the samples.
    y (array-like): Target values for the samples.
    test_size (float, optional): Proportion of the dataset to include in the test split. Default is 0.2 (20%).
    random_state (int, optional): Random seed used to shuffle the data. Default is None (no seed).

    Returns:
    dict: Dictionary containing the LogisticRegression model, training and testing data, and evaluation metrics.
    """

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Create a Logistic Regression model and fit it to the training data
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predict the target values for the testing data
    y_pred = model.predict(X_test)

    # Calculate accuracy and classification report
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return {
        "model": model,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "y_pred": y_pred,
        "accuracy": accuracy,
        "classification_report": report,
    }