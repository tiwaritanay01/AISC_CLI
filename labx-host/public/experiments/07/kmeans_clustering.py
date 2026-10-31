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
