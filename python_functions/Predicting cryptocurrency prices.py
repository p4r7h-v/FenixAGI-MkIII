import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt


def predict_crypto_prices(crypto_data, days_to_predict=7, test_size=0.2):
    dataset = crypto_data.filter(['Close'])
    scaled_data = MinMaxScaler().fit_transform(dataset.values)

    prediction_days = days_to_predict
    x_train, y_train = [], []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days : x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)

    split = int(len(dataset) * (1 - test_size))
    test_data = dataset[split - prediction_days :].values
    test_data = MinMaxScaler().fit_transform(test_data)

    x_test = []
    for x in range(prediction_days, len(test_data)):
        x_test.append(test_data[x - prediction_days : x, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predictions = model.predict(x_test)
    predictions = MinMaxScaler().fit(dataset[split:].values).inverse_transform(predictions)

    plt.figure(figsize=(16, 8))
    plt.plot(dataset.index[:split], dataset[:split], label="Training data")
    plt.plot(dataset.index[split:], dataset[split:], label="Testing data")
    plt.plot(
        dataset.index[split + prediction_days:],
        predictions,
        label="Predicted price",
    )
    plt.legend()
    plt.title("Cryptocurrency Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()