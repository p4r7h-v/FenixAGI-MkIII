import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def predict_flight_delays(file_path):
    # Load data
    data = pd.read_csv(file_path)

    # Preprocess data
    # This would include cleaning, handling missing values, datetime conversions, and
    # feature extraction. The code below assumes these steps are already done.

    # Split data into features and target
    X = data.drop('is_delayed', axis=1)  # is_delayed is assumed to be the target variable (1 for delayed, 0 for not)
    y = data['is_delayed']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Make predictions
    y_pred = clf.predict(X_test)

    # Evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    print("Classification report:")
    print(classification_report(y_test, y_pred))

    return clf