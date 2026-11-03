# LabX Remote: AISC Practical 07 (Unsupervised Learning using K-Means Clustering)
$filename = "kmeans_clustering.py"
$code = @'
import numpy as np

def kmeans(X, k=2, max_iters=100):
    np.random.seed(42)
    # Randomly initialize centroids from sample points
    initial_indices = np.random.choice(len(X), k, replace=False)
    centroids = X[initial_indices].copy()

    for _ in range(max_iters):
        # Compute euclidean distance from all points to centroids
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        # Recompute centroids
        new_centroids = np.array([X[labels == i].mean(axis=0) if len(X[labels == i]) > 0 else centroids[i] for i in range(k)])

        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids

    return labels, centroids

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX Exp 07: Unsupervised K-Means Clustering")
    print("=" * 55)

    X = np.array([
        [1.0, 2.0], [1.0, 4.0], [1.0, 0.0],
        [10.0, 2.0], [10.0, 4.0], [10.0, 0.0]
    ])

    labels, centroids = kmeans(X, k=2)

    print("Data Points:")
    for pt, lbl in zip(X, labels):
        print(f"  Point {pt} -> Cluster {lbl}")

    print("\nFinal Cluster Centroids:")
    for idx, c in enumerate(centroids):
        print(f"  Centroid {idx}: {c}")
    print("=" * 55)

# --- Line 44: Execution & Theory Division ---
# --- Line 45: Execution & Theory Division ---
# --- Line 46: Execution & Theory Division ---
# --- Line 47: Execution & Theory Division ---
# --- Line 48: Execution & Theory Division ---
# --- Line 49: Execution & Theory Division ---
# --- Line 50: Execution & Theory Division ---

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# Unsupervised learning finds structure in data without labels, using
# methods like clustering to group similar items and dimensionality
# reduction to uncover latent factors. Techniques such as k-means, DBSCAN,
# hierarchical clustering, PCA, t-SNE, and autoencoders help reveal
# patterns, anomalies, or low-dimensional representations. The goal is to
# extract insights, compress data, or prepare features for downstream tasks.
# ============================================================================

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White

Write-Host "[OK] AISC Practical 07 ready!" -ForegroundColor White