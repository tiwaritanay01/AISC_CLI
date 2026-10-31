import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.1, epochs=20):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def activation(self, z):
        return 1 if z >= 0 else 0

    def fit(self, X, y):
        self.weights = np.zeros(X.shape[1])
        self.bias = 0.0

        for epoch in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                prediction = self.activation(np.dot(xi, self.weights) + self.bias)
                error = target - prediction
                self.weights += self.learning_rate * error * xi
                self.bias += self.learning_rate * error
                errors += abs(error)

            if errors == 0:
                print(f"Perceptron converged at epoch {epoch + 1}!")
                break

    def predict(self, X):
        return np.array([
            self.activation(np.dot(x, self.weights) + self.bias)
            for x in X
        ])

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX Exp 05: Single Layer Perceptron (AND Gate)")
    print("=" * 55)

    # Linearly separable binary patterns (AND Gate)
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    y = np.array([0, 0, 0, 1])

    model = Perceptron(learning_rate=0.1, epochs=20)
    model.fit(X, y)

    predictions = model.predict(X)
    print("Learned Weights :", model.weights)
    print("Learned Bias    :", model.bias)
    print("Target Outputs  :", y)
    print("Predicted Output:", predictions)
    print("Accuracy        :", f"{np.mean(predictions == y) * 100:.1f}%")
    print("=" * 55)
