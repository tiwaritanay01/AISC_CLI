# LabX Remote: AISC Practical 06 (Supervised Learning using Multi-Layer Perceptron (MLP))
$clipCode = $null
$filename = "mlp_neural_network.py"
$code = @'
import numpy as np

class MLP:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=1.0):
        self.lr = learning_rate
        self.W1 = np.random.randn(input_size, hidden_size) * 0.5
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.5
        self.b2 = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x):
        return x * (1.0 - x)

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def train(self, X, y, epochs=10000):
        for ep in range(epochs):
            output = self.forward(X)
            error = y - output
            d_output = error * self.sigmoid_derivative(output)
            error_hidden = d_output.dot(self.W2.T)
            d_hidden = error_hidden * self.sigmoid_derivative(self.a1)

            self.W2 += self.a1.T.dot(d_output) * self.lr
            self.b2 += np.sum(d_output, axis=0, keepdims=True) * self.lr
            self.W1 += X.T.dot(d_hidden) * self.lr
            self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * self.lr

    def predict(self, X):
        return (self.forward(X) >= 0.5).astype(int)

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX Exp 06: Multi-Layer Perceptron (XOR Non-Linear)")
    print("=" * 55)

    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    y = np.array([
        [0],
        [1],
        [1],
        [0]
    ])

    mlp = MLP(input_size=2, hidden_size=4, output_size=1, learning_rate=1.0)
    print("Training MLP network with Backpropagation...")
    mlp.train(X, y, epochs=10000)

    preds = mlp.predict(X)
    print("Input Patterns:")
    for inp, target, pred in zip(X, y, preds):
        print(f"  {inp} -> Target: {target[0]}, Predicted: {pred[0]}")
    print("=" * 55)

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# Multi-layer perceptron (MLP) is a feed-forward neural network that maps
# input vectors to output vectors using layers of weighted neurons. Each
# neuron computes a weighted sum of its inputs, adds a bias, and applies a
# nonlinear activation function (e.g., ReLU, sigmoid). Training uses back-
# propagation to compute gradients of a loss function (e.g., cross-entropy)
# with respect to weights, and optimizers (SGD, Adam) update weights to
# minimize error. The network learns hierarchical feature representations,
# enabling classification or regression on complex data.
# ============================================================================

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White
if (-not $clipCode -or $filename.EndsWith(".py")) { $clipCode = $code }

if ($clipCode) {
    try {
        Set-Clipboard -Value $clipCode -ErrorAction Stop
        Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White
    } catch {
        try {
            $clipCode | clip.exe
            Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White
        } catch {}
    }
}
Write-Host "[OK] AISC Practical 06 ready!" -ForegroundColor White