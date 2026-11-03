# LabX Remote: AISC Practical 03 (Uninformed Search - Depth First Iterative Deepening (DFID))
$filename = "dfid_search.py"
$code = @'
import sys
from collections import defaultdict

graph = defaultdict(list)

def dls(node, goal, depth, visited):
    if node == goal:
        print(node, end=" ")
        return True
    if depth <= 0:
        return False
    visited.add(node)
    print(node, end=" -> ")
    for neighbor in graph[node]:
        if neighbor not in visited:
            if dls(neighbor, goal, depth - 1, visited):
                return True
    return False

def iddfs(start, goal, max_depth):
    for depth in range(max_depth + 1):
        print(f"\nSearching at Depth Limit = {depth}: ", end="")
        visited = set()
        if dls(start, goal, depth, visited):
            print(f"\n[SUCCESS] Goal '{goal}' reached at depth {depth}!")
            return True
    print(f"\n[FAIL] Goal '{goal}' not found within depth {max_depth}.")
    return False

if __name__ == "__main__":
    # Graph edges definition
    edges = [
        ("A", "B"), ("A", "C"),
        ("B", "D"), ("B", "E"),
        ("C", "F"), ("C", "G"),
        ("E", "H"), ("F", "I")
    ]
    for u, v in edges:
        graph[u].append(v)

    start_node = "A"
    goal_node = "H"
    print("Graph Structure:")
    for k, v in graph.items():
        print(f"  {k} -> {v}")

    print(f"\nRunning DFID Search from '{start_node}' to '{goal_node}':")
    iddfs(start_node, goal_node, max_depth=4)

# --- Line 50: Execution & Theory Division ---

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# Depth First Iterative Deepening is a search strategy that combines the
# benefits of Breadth First Search and Depth First Search. It works by
# performing a series of depth-first searches with increasing depth limits,
# starting from a small limit and gradually increasing it until the goal is
# found. The algorithm uses a stack to keep track of nodes to visit and
# their depths, and it backtracks when it reaches a node that exceeds the
# current depth limit. This approach allows DFID to find the shortest path
# to the goal while avoiding the high memory usage of Breadth First Search.
# The time complexity of DFID is O(b^d) and the space complexity is O(d),
# where b is the branching factor and d is the depth of the goal node.
# ============================================================================

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White

Write-Host "[OK] AISC Practical 03 ready!" -ForegroundColor White