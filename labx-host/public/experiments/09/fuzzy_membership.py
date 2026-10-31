import numpy as np

def triangular_membership(x, a, b, c):
    x = np.asarray(x, dtype=float)
    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0.0)

def trapezoidal_membership(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    return np.maximum(np.minimum(np.minimum((x - a) / (b - a), 1.0), (d - x) / (d - c)), 0.0)

if __name__ == "__main__":
    print("=" * 60)
    print(" LabX Exp 09: Fuzzy Membership Functions")
    print("=" * 60)

    test_values = [10, 20, 30, 50, 70, 80, 90]
    print(f"{'Input (x)':<12} | {'Triangular (20,50,80)':<22} | {'Trapezoidal (10,30,70,90)':<25}")
    print("-" * 65)

    for val in test_values:
        tri_deg = triangular_membership(val, 20, 50, 80)
        trap_deg = trapezoidal_membership(val, 10, 30, 70, 90)
        print(f"{val:<12} | {tri_deg:<22.3f} | {trap_deg:<25.3f}")

    print("=" * 60)
