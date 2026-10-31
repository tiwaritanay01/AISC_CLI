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
