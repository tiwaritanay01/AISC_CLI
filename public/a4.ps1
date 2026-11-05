# LabX Remote: AISC Practical 04 (Implementation of Alpha-Beta Pruning Algorithm)
$filename = "alpha_beta_pruning.py"
$code = @'
def alpha_beta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or isinstance(node, int):
        return node

    if maximizing_player:
        value = float('-inf')
        for child in node:
            value = max(value, alpha_beta(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                print(f"  [Pruning] Branch pruned at Maximizer node: alpha ({alpha}) >= beta ({beta})")
                break
        return value
    else:
        value = float('inf')
        for child in node:
            value = min(value, alpha_beta(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                print(f"  [Pruning] Branch pruned at Minimizer node: alpha ({alpha}) >= beta ({beta})")
                break
        return value

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX: Alpha-Beta Pruning Game Tree Evaluator")
    print("=" * 55)
    
    # Game tree: 2 levels deep with 4 leaf pairs
    tree = [
        [3, 1],
        [6, 8],
        [1, 7],
        [0, -1]
    ]

    print(f"Game Tree Leaves: {tree}")
    result = alpha_beta(tree, 2, float('-inf'), float('inf'), True)
    print(f"\nOptimal Value at Root: {result}")
    print("=" * 55)

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
# Alpha-Beta Pruning is a search algorithm used to reduce the number of
# nodes to be evaluated in a minimax tree, it considers two values alpha and
# beta which represent the best possible score for the maximizing player and
# the minimizing player respectively. The algorithm works by maintaining a
# window of possible scores, if the score of a node is outside this window
# it can be pruned, reducing the number of nodes to be evaluated. The alpha
# value is the best possible score for the maximizing player, while the beta
# value is the best possible score for the minimizing player, the algorithm
# prunes nodes that are guaranteed to have a score outside the alpha-beta
# window.
# ============================================================================

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White

Write-Host "[OK] AISC Practical 04 ready!" -ForegroundColor White