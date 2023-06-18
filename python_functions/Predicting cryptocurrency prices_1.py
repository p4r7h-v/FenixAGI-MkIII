import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def predict_crypto_prices(ticker, start_date, end_date):
    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    
    # Calculate the number of days
    data['Days'] = (data['Date'] - data['Date'].min()).dt.days
    
    # Prepare data for training and testing
    X = data[['Days']]
    y = data['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Test the model
    score = model.score(X_test, y_test)
    print(f"Model accuracy: {score*100:.2f}%")
    
    # Predict future prices
    future_days = data['Days'].max() + 1
    future_date = data['Date'].min() + pd.to_timedelta(future_days, unit='D')
    future_price = model.predict([[future_days]])
    
    return {"Date": future_date, "Predicted Price": future_price[0]}

# Example usage
predicted_price = predict_crypto_prices(ticker='BTC-USD', start_date='2020-01-01', end_date='2021-01-01')
print(predicted_price)