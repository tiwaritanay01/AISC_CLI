# LabX Remote: AISC Practical 10 (Fuzzy Control System Simulation (Fan Speed Controller))
$filename = "fuzzy_control_system.py"
$code = @'
import sys
import numpy as np

def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)

def simulate_fan_controller(temp: float) -> float:
    # 1. Fuzzification
    u_cold = triangular(temp, 0, 0, 20) if temp <= 20 else 0.0
    u_warm = triangular(temp, 10, 20, 30)
    u_hot = triangular(temp, 20, 40, 40) if temp >= 20 else 0.0

    print(f"Fuzzified Degrees: Cold={u_cold:.2f}, Warm={u_warm:.2f}, Hot={u_hot:.2f}")

    # 2. Rule evaluation (Mamdani minimum implication)
    w_slow = u_cold
    w_medium = u_warm
    w_fast = u_hot

    # 3. Defuzzification via Weighted Average Centroid
    slow_center = 25.0
    medium_center = 50.0
    fast_center = 85.0

    numerator = (w_slow * slow_center) + (w_medium * medium_center) + (w_fast * fast_center)
    denominator = w_slow + w_medium + w_fast

    if denominator == 0:
        return 0.0
    return numerator / denominator

if __name__ == "__main__":
    print("=" * 60)
    print(" LabX Exp 10: Fuzzy Control System (Fan Speed Controller)")
    print("=" * 60)

    # Allow custom CLI argument or interactive input
    if len(sys.argv) > 1:
        try:
            temp = float(sys.argv[1])
        except ValueError:
            temp = 28.0
    else:
        temp = 28.0

    print(f"Input Room Temperature: {temp:.1f} deg C")
    fan_speed = simulate_fan_controller(temp)
    print(f"Computed Fan Speed    : {fan_speed:.2f} %")
    print("=" * 60)

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# Fuzzy control systems use linguistic variables and membership functions to
# map crisp inputs to fuzzy sets. Rules are expressed in IF-THEN form,
# combining antecedents with AND/OR operators to produce fuzzy outputs.
# Defuzzification (e.g., centroid) converts the aggregated fuzzy output back
# to a crisp control action. The system handles uncertainty by allowing
# partial membership, enabling smoother transitions than binary logic.
# ============================================================================

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White

Write-Host "[OK] AISC Practical 10 ready!" -ForegroundColor White