import numpy as np

def neural_network(X, y, hidden_size, learning_rate=0.01, epochs=10000):
    input_size = X.shape[1]
    output_size = y.shape[1]

    # Initialize the weights
    W1 = np.random.randn(input_size, hidden_size)
    b1 = np.zeros(hidden_size)
    W2 = np.random.randn(hidden_size, output_size)
    b2 = np.zeros(output_size)

    # Sigmoid activation function
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    # Derivative of sigmoid activation function
    def sigmoid_derivative(x):
        return sigmoid(x) * (1 - sigmoid(x))

    # Forward and Backward Propagation
    for i in range(epochs):
        # Forward Propagation
        Z1 = np.dot(X, W1) + b1
        A1 = sigmoid(Z1)
        Z2 = np.dot(A1, W2) + b2
        A2 = sigmoid(Z2)

        # Backward Propagation
        dZ2 = A2 - y
        dW2 = np.dot(A1.T, dZ2) / len(X)
        db2 = np.sum(dZ2, axis=0, keepdims=True) / len(X)
        dZ1 = np.dot(dZ2, W2.T) * sigmoid_derivative(Z1)
        dW1 = np.dot(X.T, dZ1) / len(X)
        db1 = np.sum(dZ1, axis=0, keepdims=True) / len(X)

        # Update the weights
        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1
        W2 -= learning_rate * dW2
        b2 -=learning_rate * db2

    return W1, b1, W2, b2

# Example usage
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

W1, b1, W2, b2 = neural_network(X, y, hidden_size=5, learning_rate=0.5, epochs=20000)

def predict(X):
    Z1 = np.dot(X, W1) + b1
    A1 = 1 / (1 + np.exp(-Z1))
    Z2 = np.dot(A1, W2) + b2
    A2 = 1 / (1 + np.exp(-Z2))
    return A2

print(predict(X))