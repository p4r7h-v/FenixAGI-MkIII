import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

def predict_patient_readmissions(data_path):
    # Load historical patient data
    data = pd.read_csv(data_path)

    # Clean and preprocess the data to be used in the model (assumes proper column names are in the CSV file)
    # You'll need to modify the feature and target column names based on your specific dataset
    features = data.drop(columns=["readmission"])
    target = data["readmission"]

    # Split the data into training and testing datasets (70% train, 30% test)
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

    # Create logistic regression model
    log_reg_model = LogisticRegression()

    # Train the model
    log_reg_model.fit(x_train, y_train)

    # Make predictions using the test dataset
    y_pred = log_reg_model.predict(x_test)

    # Evaluate the model
    print("Accuracy score: ", accuracy_score(y_test, y_pred))
    print("Classification report: \n", classification_report(y_test, y_pred))

    # Return the trained model
    return log_reg_model

# Example usage:
trained_model = predict_patient_readmissions("path/to/your/historical_patient_data.csv")