import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def predict_readmissions(data, target, model=None, test_size=0.25, random_state=42):
    """
    Predict patient readmissions using a given dataset and a machine learning model.
    
    :param data: pandas DataFrame containing features for the dataset
    :param target: pandas Series containing target variable - readmission status
    :param model: scikit-learn model to be used for prediction (default: RandomForestClassifier)
    :param test_size: float ranging from 0 to 1, representing the proportion of the dataset to be used for testing (default: 0.25)
    :param random_state: int, controls randomization for train/test split (default: 42)
    
    :return: tuple (model, accuracy_score), the trained model and its accuracy score on the test set
    """
    # Set default model if not provided
    if model is None:
        model = RandomForestClassifier(random_state=random_state)

    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=test_size, random_state=random_state)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate the accuracy score
    score = accuracy_score(y_test, y_pred)

    return model, score

# Example usage:
if __name__ == "__main__":
    # Load your dataset here (for demonstration purposes, using a dummy dataset)
    # Replace this with the actual dataset containing patient features and readmission status
    data = pd.DataFrame(np.random.rand(100, 5), columns=["feature1", "feature2", "feature3", "feature4", "feature5"])
    target = pd.Series(np.random.randint(0, 2, 100), name="readmission")
    
    model, accuracy = predict_readmissions(data, target)
    print(f"Model: {model}")
    print(f"Accuracy: {accuracy}")