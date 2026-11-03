# LabX Remote: AISC Practical 08 (Associative Memory Network (Hopfield Network))
$filename = "hopfield_network.py"
$code = @'
import numpy as np

class HopfieldNetwork:
    def __init__(self, n_neurons):
        self.n_neurons = n_neurons
        self.weights = np.zeros((n_neurons, n_neurons))

    def train(self, patterns):
        self.weights = np.zeros((self.n_neurons, self.n_neurons))
        for pattern in patterns:
            p = np.array(pattern)
            self.weights += np.outer(p, p)
        np.fill_diagonal(self.weights, 0)
        self.weights /= self.n_neurons

    def recall(self, pattern, steps=10):
        state = np.array(pattern).copy()
        for _ in range(steps):
            for i in range(self.n_neurons):
                activation = np.dot(self.weights[i], state)
                state[i] = 1 if activation >= 0 else -1
        return state

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX Exp 08: Hopfield Associative Memory Network")
    print("=" * 55)

    # 8-dimensional bipolar prototype memories (-1, +1)
    patterns = np.array([
        [1,  1,  1,  1, -1, -1, -1, -1],
        [1, -1,  1, -1,  1, -1,  1, -1]
    ])

    net = HopfieldNetwork(n_neurons=8)
    net.train(patterns)

    print("Stored Target Patterns:")
    print("  Pattern 1:", patterns[0])
    print("  Pattern 2:", patterns[1])

    # Probe with 2 corrupted bits
    noisy_probe = np.array([1, 1, -1, 1, -1, -1, 1, -1])
    print("\nNoisy Input Pattern  :", noisy_probe)

    recovered = net.recall(noisy_probe)
    print("Associatively Recalled:", recovered)

    if np.array_equal(recovered, patterns[0]):
        print("-> Successfully restored to Stored Pattern 1!")
    else:
        print("-> Recalled nearest memory state.")
    print("=" * 55)

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# Associative memory stores patterns as high-dimensional vectors and
# retrieves them by similarity. The classic Hopfield network uses a
# symmetric weight matrix built from outer products of stored patterns, and
# updates neurons asynchronously until convergence. Retrieval works by
# presenting a noisy or incomplete pattern, then iteratively applying the
# sign of the weighted sum until the state stabilizes to the nearest stored
# pattern. TODO: compute weight matrix W = Σ_i p_i p_iᵀ - N·I, then iterate
# v ← sign(Wv) until convergence.
# ============================================================================

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White

Write-Host "[OK] AISC Practical 08 ready!" -ForegroundColor White