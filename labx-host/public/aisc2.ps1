# LabX Remote: AISC Practical 02 (Informed Search - A* Algorithm for 15-Puzzle Problem)
$clipCode = $null
$filename = "a_star_15_puzzle.py"
$code = @'
import heapq

GOAL = (
    (1, 2, 3, 4),
    (5, 6, 7, 8),
    (9, 10, 11, 12),
    (13, 14, 15, 0)
)
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan(state):
    distance = 0
    for i in range(4):
        for j in range(4):
            value = state[i][j]
            if value != 0:
                goal_x = (value - 1) // 4
                goal_y = (value - 1) % 4
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def get_neighbors(state):
    state_list = [list(row) for row in state]
    x, y = 0, 0
    for i in range(4):
        for j in range(4):
            if state_list[i][j] == 0:
                x, y = i, j
    neighbors = []
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 4 and 0 <= ny < 4:
            new_state = [row[:] for row in state_list]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(tuple(tuple(row) for row in new_state))
    return neighbors

def a_star(start):
    pq = []
    heapq.heappush(pq, (manhattan(start), 0, start, []))
    visited = set()
    while pq:
        f, g, current, path = heapq.heappop(pq)
        if current == GOAL:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + manhattan(neighbor)
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [current]))
    return None

if __name__ == "__main__":
    start = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    )
    print("Initial State:")
    for r in start:
        print(r)
    path = a_star(start)
    if path:
        print(f"\nSolution found in {len(path) - 1} moves:")
        for step in path:
            for row in step:
                print(row)
            print()
    else:
        print("No solution found.")

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# The A* algorithm is an informed search strategy used to find the shortest
# path between two nodes in a weighted graph. It uses a best-first search
# approach, where the node with the lowest estimated total cost is chosen
# next. The algorithm consists of a priority queue to hold nodes to be
# evaluated, a set of visited nodes, and a heuristic function to estimate
# the distance from a node to the goal. The heuristic function guides the
# search towards the goal, making it more efficient than uninformed search
# algorithms. The algorithm terminates when the goal node is reached or the
# queue is empty.
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
Write-Host "[OK] AISC Practical 02 ready!" -ForegroundColor White