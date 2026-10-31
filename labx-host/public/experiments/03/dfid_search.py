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
