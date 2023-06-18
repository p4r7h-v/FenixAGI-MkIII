import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def run_logistic_regression(X, y, test_size=0.2, random_state=None):
    """
    Runs a logistic regression given input features X and output labels y.
    
    Parameters:
    X : {array-like, dataframe} of shape (n_samples, n_features)
        - Training data
    y : array-like of shape (n_samples,)
        - Target labels
    test_size : float, int or None, optional (default=0.2)
        - The proportion of the dataset to include in the test split.
    random_state : int, RandomState instance, default=None
        - Controls the shuffling applied to the data before applying the split.
    
    Returns:
    dict: A dictionary containing relevant model metrics
    """

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Create and train logistic regression model
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)

    # Make predictions
    y_pred = log_reg.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)

    # Return results
    return {
        'accuracy': accuracy,
        'confusion_matrix': conf_matrix,
        'classification_report': class_report,
        'model': log_reg,
    }