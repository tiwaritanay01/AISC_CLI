# LabX Remote: AISC Practical 09 (Implementation of Fuzzy Membership Functions)
$clipCode = $null
$filename = "fuzzy_membership.py"
$code = @'
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

# --- Line 27: Execution & Theory Division ---
# --- Line 28: Execution & Theory Division ---
# --- Line 29: Execution & Theory Division ---
# --- Line 30: Execution & Theory Division ---
# --- Line 31: Execution & Theory Division ---
# --- Line 32: Execution & Theory Division ---
# --- Line 33: Execution & Theory Division ---
# --- Line 34: Execution & Theory Division ---
# --- Line 35: Execution & Theory Division ---
# --- Line 36: Execution & Theory Division ---
# --- Line 37: Execution & Theory Division ---
# --- Line 38: Execution & Theory Division ---
# --- Line 39: Execution & Theory Division ---
# --- Line 40: Execution & Theory Division ---
# --- Line 41: Execution & Theory Division ---
# --- Line 42: Execution & Theory Division ---
# --- Line 43: Execution & Theory Division ---
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
# Fuzzy membership functions map crisp inputs to degrees of belonging
# between 0 and 1, enabling reasoning with imprecise data. Common shapes
# include triangular, trapezoidal, Gaussian, and sigmoid, each defined by a
# few parameters that control the width and center of the fuzzy set. The
# choice of shape affects smoothness, computational cost, and
# interpretability. Membership values are combined via fuzzy operators (AND,
# OR) and aggregated to produce fuzzy outputs, which are then defuzzified to
# crisp decisions. Proper tuning of parameters is essential for accurate
# modeling of real-world phenomena.
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
Write-Host "[OK] AISC Practical 09 ready!" -ForegroundColor White