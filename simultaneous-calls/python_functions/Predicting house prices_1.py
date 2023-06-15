import numpy as np
from sklearn.linear_model import LinearRegression

def predict_house_price(bedrooms, square_footage, age):
    # Sample dataset
    # Features: [number of bedrooms, square footage, age]
    X = np.array([
        [2, 1200, 30],
        [3, 1700, 20],
        [3, 1500, 25],
        [4, 2000, 15],
        [4, 2300, 10],
    ])

    # Target: house prices in thousands of dollars
    y = np.array([150, 250, 225, 350, 400])

    # Create and fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the house price based on the input features
    predicted_price = model.predict([[bedrooms, square_footage, age]])[0]

    return predicted_price

# Example usage:
bedrooms = 3
square_footage = 1600
age = 25
price_prediction = predict_house_price(bedrooms, square_footage, age)
print(f"The predicted price for a {bedrooms} bedroom, {square_footage} sqft, and {age} years old house is: ${price_prediction * 1000}")