import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def detect_credit_card_fraud(data: pd.DataFrame, test_data: pd.DataFrame):
    # Prepare the dataset
    X = data.drop('Class', axis=1)
    y = data['Class']

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    test_data = scaler.transform(test_data)

    # Build the logistic regression model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)

    # Validate the model
    y_val_pred = model.predict(X_val)
    print("Accuracy score:", accuracy_score(y_val, y_val_pred))
    print("Classification report:", classification_report(y_val, y_val_pred))

    # Predict frauds on the test dataset
    fraud_predictions = model.predict(test_data)
    return fraud_predictions