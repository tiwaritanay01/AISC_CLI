"""Host builder script: generates public/ catalog, manifests, experiment sources, HTML, and ZIP archive
populated from AISC Laboratory Submissions (A_AISC_A_Submissions)."""

import os
import json
import html
import zipfile
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
HOST_DIR = BASE_DIR / "labx-host"
PUBLIC_DIR = HOST_DIR / "public"
EXP_DIR = PUBLIC_DIR / "experiments"
DL_DIR = PUBLIC_DIR / "downloads"

EXPERIMENTS = [
    {
        "id": 1,
        "slug": "ai-agents-peas-case-study",
        "title": "Case Study on AI Agents & PEAS Properties",
        "language": "python",
        "aliases": ["ai agents", "peas", "agent types", "case study ai", "peas properties"],
        "description": "Comprehensive study and simulation of AI Agent types (Simple Reflex, Model, Goal, Utility) and PEAS properties.",
        "aim": "To prepare a case study on AI Agents including type, environment, and PEAS properties.",
        "theory": (
            "AI Agents can be classified into four primary types: Simple Reflex, Model-Based, Goal-Based, and Utility-Based.\n"
            "The environment can be categorized across dimensions: fully vs. partially observable, deterministic vs. stochastic, "
            "static vs. dynamic, and episodic vs. sequential.\n"
            "The PEAS framework defines: Performance measure, Environment, Actuators, and Sensors, formalizing the agent's interaction loop."
        ),
        "algorithm": [
            "Define PEAS descriptor tuple: (P)erformance metric, (E)nvironment state, (A)ctuator commands, (S)ensor percepts.",
            "Classify environment properties (Observability, Determinism, Dynamism, Episodic nature).",
            "Select agent architecture: evaluate condition-action rules for reflex or internal state mapping for model-based agents.",
            "Simulate agent percept-reason-act cycle across discrete operational timesteps.",
            "Report performance score and environmental impact."
        ],
        "files": [
            {
                "path": "agent_case_study.py",
                "source": "agent_case_study.py",
                "role": "source",
                "content": '''"""Experiment 01: AI Agents and PEAS Framework Simulator."""

class AIAgent:
    def __init__(self, name: str, agent_type: str, peas: dict):
        self.name = name
        self.agent_type = agent_type
        self.peas = peas
        self.state = {}

    def display_peas(self):
        print(f"\\n{'='*55}")
        print(f" AGENT CASE STUDY: {self.name.upper()} ({self.agent_type})")
        print(f"{'='*55}")
        print(f"  - Performance Measure : {self.peas['Performance']}")
        print(f"  - Environment         : {self.peas['Environment']}")
        print(f"  - Actuators           : {self.peas['Actuators']}")
        print(f"  - Sensors             : {self.peas['Sensors']}")

    def act(self, percept: dict):
        # Condition-action rule reasoning
        status = percept.get("cleanliness", "dirty")
        location = percept.get("location", "Room_A")
        if status == "dirty":
            action = "SUCK_DIRT"
        else:
            action = "MOVE_TO_NEXT_ROOM"
        print(f"[Sensor Percept: {percept}] --> Reasoned Action: {action}")
        return action

def main():
    vacuum_peas = {
        "Performance": "Square area cleaned, low energy consumption, zero damage",
        "Environment": "Office floors, obstacles, furniture, doorways",
        "Actuators": "Drive wheels, vacuum suction motor, status indicator",
        "Sensors": "Cliff sensor, bump bumper, infrared distance, dirt detector"
    }
    car_peas = {
        "Performance": "Passenger safety, speed, legal adherence, comfort",
        "Environment": "Public roads, pedestrians, weather, traffic signs",
        "Actuators": "Steering assembly, accelerator, hydraulic brakes, horn",
        "Sensors": "LiDAR, RGB cameras, radar arrays, GPS, IMU sensors"
    }

    agent1 = AIAgent("Autonomous Vacuum Agent", "Simple Reflex / Model-Based", vacuum_peas)
    agent2 = AIAgent("Self-Driving Navigation Agent", "Goal & Utility-Based", car_peas)

    agent1.display_peas()
    agent1.act({"location": "Room_A", "cleanliness": "dirty"})
    agent1.act({"location": "Room_A", "cleanliness": "clean"})

    agent2.display_peas()
    print("\\n[PEAS Analysis Complete - Viva Cleared 3/3]")

if __name__ == "__main__":
    main()
'''
            },
            {
                "path": "CASE_STUDY.md",
                "source": "CASE_STUDY.md",
                "role": "docs",
                "content": """# AI Agents & PEAS Framework Case Study

## 1. Agent Classification
1. **Simple Reflex Agents**: Act strictly on current percept via condition-action rules.
2. **Model-Based Reflex Agents**: Maintain internal model state of unobserved environment.
3. **Goal-Based Agents**: Reason over future states required to achieve goals.
4. **Utility-Based Agents**: Maximize continuous utility / satisfaction functions.

## 2. PEAS Analysis
- **P** (Performance): Metric defining success.
- **E** (Environment): Context in which agent operates.
- **A** (Actuators): Tools agent uses to exert physical/virtual influence.
- **S** (Sensors): Inbound sensory mechanisms.
"""
            }
        ],
        "run": {
            "kind": "python",
            "entry": "agent_case_study.py"
        }
    },
    {
        "id": 2,
        "slug": "a-star-15-puzzle-problem",
        "title": "Informed Search - A* Algorithm for 15-Puzzle Problem",
        "language": "python",
        "aliases": ["a star", "15 puzzle", "a star algorithm", "informed search", "manhattan distance"],
        "description": "Heuristic A* search algorithm using Manhattan Distance to solve the 15-Puzzle problem.",
        "aim": "Informed Search - A* Algorithm for the 15-Puzzle Problem using Manhattan Distance heuristic.",
        "theory": (
            "The A* algorithm is an informed search strategy used to find the shortest path between nodes in a state-space graph.\n"
            "It evaluates nodes using f(n) = g(n) + h(n), where g(n) is the exact cost to reach node n from the start, "
            "and h(n) is an admissible heuristic estimating the cost from n to the goal.\n"
            "For the 15-puzzle problem, the sum of Manhattan distances of all tiles to their goal coordinates provides an admissible and consistent heuristic."
        ),
        "algorithm": [
            "Initialize priority queue with start state, g=0, and f=manhattan(start).",
            "Pop state with minimum f-value from priority queue.",
            "If current state matches GOAL, return reconstructed solution path.",
            "Generate valid neighbor states by sliding empty tile (0) in 4 directions.",
            "For each unvisited neighbor, compute g_new = g + 1, f_new = g_new + manhattan(neighbor).",
            "Push updated states into priority queue and repeat until goal is reached."
        ],
        "files": [
            {
                "path": "a_star_15_puzzle.py",
                "source": "a_star_15_puzzle.py",
                "role": "source",
                "content": '''import heapq

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
        print(f"\\nSolution found in {len(path) - 1} moves:")
        for step in path:
            for row in step:
                print(row)
            print()
    else:
        print("No solution found.")
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "a_star_15_puzzle.py"
        }
    },
    {
        "id": 3,
        "slug": "dfid-uninformed-search",
        "title": "Uninformed Search - Depth First Iterative Deepening (DFID)",
        "language": "python",
        "aliases": ["dfid", "iterative deepening", "iddfs", "uninformed search", "depth first"],
        "description": "Depth First Iterative Deepening (DFID/IDDFS) graph search combining space efficiency of DFS with optimality of BFS.",
        "aim": "Uninformed Search - Depth First Iterative Deepening (DFID) search implementation on state graphs.",
        "theory": (
            "DFID (Depth First Iterative Deepening), also known as IDDFS, is an uninformed search strategy that repeatedly executes "
            "depth-limited searches with incrementally increasing depth limits until the goal state is located.\n"
            "It combines the linear space complexity O(bd) of Depth-First Search with the completeness and optimality of Breadth-First Search."
        ),
        "algorithm": [
            "Set current depth limit L = 0.",
            "Execute recursive Depth-Limited Search (DLS) starting from root up to limit L.",
            "If goal node is encountered during traversal, terminate search and return path.",
            "If entire tree up to depth L is traversed without goal, increment L = L + 1.",
            "Repeat until goal is found or maximum search depth is exhausted."
        ],
        "files": [
            {
                "path": "dfid_search.py",
                "source": "dfid_search.py",
                "role": "source",
                "content": '''import sys
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
        print(f"\\nSearching at Depth Limit = {depth}: ", end="")
        visited = set()
        if dls(start, goal, depth, visited):
            print(f"\\n[SUCCESS] Goal '{goal}' reached at depth {depth}!")
            return True
    print(f"\\n[FAIL] Goal '{goal}' not found within depth {max_depth}.")
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

    print(f"\\nRunning DFID Search from '{start_node}' to '{goal_node}':")
    iddfs(start_node, goal_node, max_depth=4)
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "dfid_search.py"
        }
    },
    {
        "id": 4,
        "slug": "alpha-beta-pruning",
        "title": "Implementation of Alpha-Beta Pruning Algorithm",
        "language": "python",
        "aliases": ["alpha beta", "game search", "minimax", "alpha beta pruning", "adversarial search"],
        "description": "Adversarial search and branch pruning algorithm optimizing the minimax game-tree decision process.",
        "aim": "To implement Minimax Search with Alpha-Beta Pruning for two-player adversarial games.",
        "theory": (
            "Alpha-Beta pruning is an optimization technique for the minimax algorithm.\n"
            "It maintains two parameters: alpha (best value achieved by the maximizer so far) and beta (best value achieved by the minimizer so far).\n"
            "Whenever alpha >= beta, the current branch is pruned because the opponent would never permit that line of play."
        ),
        "algorithm": [
            "Initialize alpha = -infinity, beta = +infinity.",
            "For maximizing player: evaluate each child, update value = max(value, child_score), update alpha = max(alpha, value).",
            "If beta <= alpha, break loop (prune remaining siblings).",
            "For minimizing player: evaluate each child, update value = min(value, child_score), update beta = min(beta, value).",
            "If beta <= alpha, break loop (prune remaining siblings).",
            "Return optimal evaluated terminal score."
        ],
        "files": [
            {
                "path": "alpha_beta_pruning.py",
                "source": "alpha_beta_pruning.py",
                "role": "source",
                "content": '''def alpha_beta(node, depth, alpha, beta, maximizing_player):
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
    print(f"\\nOptimal Value at Root: {result}")
    print("=" * 55)
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "alpha_beta_pruning.py"
        }
    },
    {
        "id": 5,
        "slug": "single-layer-perceptron-slp",
        "title": "Single Layer Perceptron (SLP) for Binary Classification",
        "language": "python",
        "aliases": ["perceptron", "slp", "single layer perceptron", "perceptron learning rule", "binary classification"],
        "description": "Perceptron Learning Rule implementation to train a Single Layer Perceptron on linearly separable patterns.",
        "aim": "To implement a Single Layer Perceptron (SLP) neural network using the Perceptron Learning Rule to classify linearly separable binary patterns.",
        "theory": (
            "A Single Layer Perceptron is the fundamental unit of an artificial neural network.\n"
            "It computes a linear combination of inputs weighted by parameter vector W plus bias b, passed through a step activation function.\n"
            "The Perceptron Learning Rule updates weights iteratively: W = W + eta * (y - y_hat) * X, converging for linearly separable datasets."
        ),
        "algorithm": [
            "Initialize weights vector W with zeros and bias b = 0.",
            "For each training sample (x_i, target_i): compute linear output z = W . x_i + b.",
            "Apply hard step activation: output = 1 if z >= 0 else 0.",
            "Compute error = target - output.",
            "Update weights: W += learning_rate * error * x_i; bias += learning_rate * error.",
            "Repeat for specified epochs or until training error converges to zero."
        ],
        "files": [
            {
                "path": "perceptron_slp.py",
                "source": "perceptron_slp.py",
                "role": "source",
                "content": '''import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.1, epochs=20):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def activation(self, z):
        return 1 if z >= 0 else 0

    def fit(self, X, y):
        self.weights = np.zeros(X.shape[1])
        self.bias = 0.0

        for epoch in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                prediction = self.activation(np.dot(xi, self.weights) + self.bias)
                error = target - prediction
                self.weights += self.learning_rate * error * xi
                self.bias += self.learning_rate * error
                errors += abs(error)

            if errors == 0:
                print(f"Perceptron converged at epoch {epoch + 1}!")
                break

    def predict(self, X):
        return np.array([
            self.activation(np.dot(x, self.weights) + self.bias)
            for x in X
        ])

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX Exp 05: Single Layer Perceptron (AND Gate)")
    print("=" * 55)

    # Linearly separable binary patterns (AND Gate)
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    y = np.array([0, 0, 0, 1])

    model = Perceptron(learning_rate=0.1, epochs=20)
    model.fit(X, y)

    predictions = model.predict(X)
    print("Learned Weights :", model.weights)
    print("Learned Bias    :", model.bias)
    print("Target Outputs  :", y)
    print("Predicted Output:", predictions)
    print("Accuracy        :", f"{np.mean(predictions == y) * 100:.1f}%")
    print("=" * 55)
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "perceptron_slp.py"
        }
    },
    {
        "id": 6,
        "slug": "mlp-supervised-learning",
        "title": "Supervised Learning using Multi-Layer Perceptron (MLP)",
        "language": "python",
        "aliases": ["mlp", "multilayer perceptron", "backpropagation", "supervised learning", "neural network"],
        "description": "Multi-Layer Perceptron neural network with sigmoid activations and gradient descent backpropagation.",
        "aim": "To implement the Supervised Learning algorithm using Multi-Layer Perceptron (MLP) with Backpropagation to solve non-linear problems (XOR).",
        "theory": (
            "A Multi-Layer Perceptron (MLP) consists of an input layer, one or more hidden layers, and an output layer.\n"
            "Because of non-linear activation functions (such as Sigmoid), an MLP is capable of learning non-linearly separable decision boundaries (e.g. XOR gate).\n"
            "Training occurs via Backpropagation: forward pass computes loss, backward pass computes gradients using the chain rule and updates weights."
        ),
        "algorithm": [
            "Initialize network weights W1, W2 with small random values and biases b1, b2 with zeros.",
            "Forward Propagation: z1 = X . W1 + b1, a1 = sigmoid(z1), z2 = a1 . W2 + b2, output = sigmoid(z2).",
            "Compute error = target - output.",
            "Backward Propagation: calculate output delta = error * sigmoid_derivative(output).",
            "Propagate error to hidden layer: hidden delta = (output_delta . W2.T) * sigmoid_derivative(a1).",
            "Update weights and biases using gradient descent with learning rate lr.",
            "Iterate across training epochs."
        ],
        "files": [
            {
                "path": "mlp_neural_network.py",
                "source": "mlp_neural_network.py",
                "role": "source",
                "content": '''import numpy as np

class MLP:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=1.0):
        self.lr = learning_rate
        self.W1 = np.random.randn(input_size, hidden_size) * 0.5
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.5
        self.b2 = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x):
        return x * (1.0 - x)

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def train(self, X, y, epochs=10000):
        for ep in range(epochs):
            output = self.forward(X)
            error = y - output
            d_output = error * self.sigmoid_derivative(output)
            error_hidden = d_output.dot(self.W2.T)
            d_hidden = error_hidden * self.sigmoid_derivative(self.a1)

            self.W2 += self.a1.T.dot(d_output) * self.lr
            self.b2 += np.sum(d_output, axis=0, keepdims=True) * self.lr
            self.W1 += X.T.dot(d_hidden) * self.lr
            self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * self.lr

    def predict(self, X):
        return (self.forward(X) >= 0.5).astype(int)

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX Exp 06: Multi-Layer Perceptron (XOR Non-Linear)")
    print("=" * 55)

    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    y = np.array([
        [0],
        [1],
        [1],
        [0]
    ])

    mlp = MLP(input_size=2, hidden_size=4, output_size=1, learning_rate=1.0)
    print("Training MLP network with Backpropagation...")
    mlp.train(X, y, epochs=10000)

    preds = mlp.predict(X)
    print("Input Patterns:")
    for inp, target, pred in zip(X, y, preds):
        print(f"  {inp} -> Target: {target[0]}, Predicted: {pred[0]}")
    print("=" * 55)
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "mlp_neural_network.py"
        }
    },
    {
        "id": 7,
        "slug": "kmeans-unsupervised-clustering",
        "title": "Unsupervised Learning using K-Means Clustering",
        "language": "python",
        "aliases": ["kmeans", "k-means", "clustering", "unsupervised learning", "cluster centroids"],
        "description": "K-Means clustering algorithm partitioning unlabelled multidimensional data into optimal spatial clusters.",
        "aim": "To implement the Unsupervised Learning algorithm using K-Means Clustering to group unlabelled sample points.",
        "theory": (
            "K-Means is an unsupervised clustering algorithm that groups n observations into k clusters.\n"
            "Each observation belongs to the cluster with the nearest mean (cluster centroid), which serves as a prototype of the cluster.\n"
            "The objective is to minimize intra-cluster variance (Within-Cluster Sum of Squares, WCSS)."
        ),
        "algorithm": [
            "Select K centroid initial locations.",
            "Compute Euclidean distance from each sample point to all K centroids.",
            "Assign each sample point to the nearest cluster centroid.",
            "Recalculate cluster centroids as the arithmetic mean of all points assigned to that cluster.",
            "Repeat distance computation and reassignment until centroids stabilize and convergence is reached."
        ],
        "files": [
            {
                "path": "kmeans_clustering.py",
                "source": "kmeans_clustering.py",
                "role": "source",
                "content": '''import numpy as np

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

    print("\\nFinal Cluster Centroids:")
    for idx, c in enumerate(centroids):
        print(f"  Centroid {idx}: {c}")
    print("=" * 55)
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "kmeans_clustering.py"
        }
    },
    {
        "id": 8,
        "slug": "hopfield-associative-memory-network",
        "title": "Associative Memory Network (Hopfield Network)",
        "language": "python",
        "aliases": ["hopfield", "associative memory", "hebbian learning", "pattern recall", "hopfield network"],
        "description": "Discrete Hopfield Network using Hebbian learning for auto-associative memory and corrupted pattern restoration.",
        "aim": "To implement an Associative Memory Network (Hopfield Network) for pattern storage and associative recall.",
        "theory": (
            "A Hopfield Network is a recurrent artificial neural network that serves as a content-addressable associative memory system.\n"
            "Neurons have binary/bipolar threshold states (-1, +1) and symmetrical synaptic connections with zero self-feedback (w_ii = 0).\n"
            "Using Hebbian learning rules, patterns are stored as stable attractors (local energy minima). When presented with a noisy or incomplete input, the network iteratively converges to the stored prototype."
        ),
        "algorithm": [
            "Initialize zero weight matrix of size N x N.",
            "For each bipolar prototype pattern P: compute outer product P . P^T and add to weight matrix.",
            "Zero out diagonal entries (no self-loops: W_ii = 0) and normalize weights by 1/N.",
            "To recall: initialize network state with noisy probe pattern.",
            "Iteratively update neuron states: state_i = +1 if sum(W_ij * state_j) >= 0 else -1.",
            "Repeat until state stabilizes at the nearest stored memory attractor."
        ],
        "files": [
            {
                "path": "hopfield_network.py",
                "source": "hopfield_network.py",
                "role": "source",
                "content": '''import numpy as np

class HopfieldNetwork:
    def __init__(self, n_neurons):
        self.n_neurons = n_neurons
        self.weights = np.zeros((n_neurons, n_neurons))

    def train(self, patterns):
        self.weights = np.zeros((self.n_neurons, self.n_neurons))
        for pattern in patterns:
            p = np.array(pattern)
            self.weights += np.outer(p, p)
        np.fill_diagonal(self.weights, 0)
        self.weights /= self.n_neurons

    def recall(self, pattern, steps=10):
        state = np.array(pattern).copy()
        for _ in range(steps):
            for i in range(self.n_neurons):
                activation = np.dot(self.weights[i], state)
                state[i] = 1 if activation >= 0 else -1
        return state

if __name__ == "__main__":
    print("=" * 55)
    print(" LabX Exp 08: Hopfield Associative Memory Network")
    print("=" * 55)

    # 8-dimensional bipolar prototype memories (-1, +1)
    patterns = np.array([
        [1,  1,  1,  1, -1, -1, -1, -1],
        [1, -1,  1, -1,  1, -1,  1, -1]
    ])

    net = HopfieldNetwork(n_neurons=8)
    net.train(patterns)

    print("Stored Target Patterns:")
    print("  Pattern 1:", patterns[0])
    print("  Pattern 2:", patterns[1])

    # Probe with 2 corrupted bits
    noisy_probe = np.array([1, 1, -1, 1, -1, -1, 1, -1])
    print("\\nNoisy Input Pattern  :", noisy_probe)

    recovered = net.recall(noisy_probe)
    print("Associatively Recalled:", recovered)

    if np.array_equal(recovered, patterns[0]):
        print("-> Successfully restored to Stored Pattern 1!")
    else:
        print("-> Recalled nearest memory state.")
    print("=" * 55)
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "hopfield_network.py"
        }
    },
    {
        "id": 9,
        "slug": "fuzzy-membership-functions",
        "title": "Implementation of Fuzzy Membership Functions",
        "language": "python",
        "aliases": ["fuzzy membership", "fuzzy logic", "triangular membership", "trapezoidal membership", "soft computing"],
        "description": "Mathematical implementation and evaluation of Triangular and Trapezoidal fuzzy membership functions.",
        "aim": "To implement fuzzy membership functions (Triangular and Trapezoidal) and calculate degrees of membership for inputs.",
        "theory": (
            "Unlike classical binary sets where elements have strict membership (0 or 1), fuzzy sets assign elements a continuous degree of membership between [0, 1].\n"
            "Triangular Membership Function: defined by lower limit a, peak b, and upper limit c.\n"
            "Trapezoidal Membership Function: defined by lower limit a, plateau span [b, c], and upper limit d."
        ),
        "algorithm": [
            "Define triangular function: max(min((x - a)/(b - a), (c - x)/(c - b)), 0).",
            "Define trapezoidal function: max(min(min((x - a)/(b - a), 1), (d - x)/(d - c)), 0).",
            "Generate discrete input universe of discourse X.",
            "Compute membership degree for each input value.",
            "Display membership evaluation table across boundary and transition points."
        ],
        "files": [
            {
                "path": "fuzzy_membership.py",
                "source": "fuzzy_membership.py",
                "role": "source",
                "content": '''import numpy as np

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
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "fuzzy_membership.py"
        }
    },
    {
        "id": 10,
        "slug": "fuzzy-control-system-simulation",
        "title": "Fuzzy Control System Simulation (Fan Speed Controller)",
        "language": "python",
        "aliases": ["fuzzy control", "fuzzy controller", "mamdani", "temperature fan controller", "fuzzy simulation"],
        "description": "Simulation of a Mamdani fuzzy inference control system regulating fan speed based on room temperature.",
        "aim": "To write a program to simulate a fuzzy logic control system for temperature-dependent fan speed control.",
        "theory": (
            "A Fuzzy Logic Controller operates in four stages:\n"
            "1. Fuzzification: Translates crisp numeric sensor inputs into linguistic fuzzy variables (Cold, Warm, Hot).\n"
            "2. Rule Base: IF-THEN conditional rules defining system dynamics.\n"
            "3. Inference Engine: Evaluates active rules using fuzzy operators (e.g. Mamdani min/max).\n"
            "4. Defuzzification: Computes a crisp output value (e.g. Centroid / Center of Gravity method)."
        ),
        "algorithm": [
            "Define input linguistic variable (Temperature: Cold, Warm, Hot).",
            "Define output linguistic variable (Fan Speed: Slow, Medium, Fast).",
            "Define rule base: (Cold -> Slow), (Warm -> Medium), (Hot -> Fast).",
            "Obtain crisp input temperature value.",
            "Perform fuzzification, evaluate active rule firing strengths.",
            "Defuzzify aggregated fuzzy region using centroid calculation and output crisp speed."
        ],
        "files": [
            {
                "path": "fuzzy_control_system.py",
                "source": "fuzzy_control_system.py",
                "role": "source",
                "content": '''import sys
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
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "fuzzy_control_system.py"
        }
    },
    {
        "id": 11,
        "slug": "genetic-algorithm-simulated-annealing",
        "title": "Optimization using Genetic Algorithm & Simulated Annealing",
        "language": "python",
        "aliases": ["genetic algorithm", "simulated annealing", "optimization", "metaheuristic", "ga"],
        "description": "Population-based Genetic Algorithm and stochastic Simulated Annealing for non-linear function optimization.",
        "aim": "To implement Genetic Algorithm and Simulated Annealing metaheuristics for continuous optimization.",
        "theory": (
            "Genetic Algorithms (GA) mimic biological natural selection: candidate solutions (individuals) undergo selection, "
            "crossover (recombination), and mutation across successive generations to optimize a fitness objective.\n"
            "Simulated Annealing (SA) mimics the thermodynamic process of metallurgical annealing: a single candidate is perturbed, "
            "and uphill moves are conditionally accepted with probability exp(-delta_E / T) allowing escape from local optima."
        ),
        "algorithm": [
            "Initialize population of candidate solution individuals.",
            "Evaluate objective fitness for every individual.",
            "Select fittest individuals as parents for mating pool.",
            "Perform crossover to produce offspring candidates.",
            "Apply mutation with mutation probability.",
            "Replace low-fitness individuals and iterate until convergence."
        ],
        "files": [
            {
                "path": "genetic_algorithm.py",
                "source": "genetic_algorithm.py",
                "role": "source",
                "content": '''import random
import math

def fitness(x):
    # Sphere function: global minimum at x = 0
    return x ** 2

def run_genetic_algorithm(pop_size=20, generations=50, mutation_rate=0.1):
    population = [random.uniform(-10, 10) for _ in range(pop_size)]

    for gen in range(generations):
        population.sort(key=fitness)
        parents = population[:2]

        # Crossover
        child = (parents[0] + parents[1]) / 2.0

        # Mutation
        if random.random() < mutation_rate:
            child += random.uniform(-1.0, 1.0)
        child = max(-10.0, min(10.0, child))

        population[-1] = child

    best = min(population, key=fitness)
    return best, fitness(best)

def run_simulated_annealing(initial_temp=100.0, cooling_rate=0.95, iterations=100):
    current = random.uniform(-10, 10)
    current_cost = fitness(current)
    temp = initial_temp

    for _ in range(iterations):
        neighbor = current + random.uniform(-1.0, 1.0)
        neighbor_cost = fitness(neighbor)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-6)):
            current = neighbor
            current_cost = neighbor_cost

        temp *= cooling_rate

    return current, current_cost

if __name__ == "__main__":
    print("=" * 60)
    print(" LabX Exp 11: Genetic Algorithm & Simulated Annealing")
    print("=" * 60)

    ga_x, ga_fit = run_genetic_algorithm()
    print(f"Genetic Algorithm Result       : x = {ga_x:.6f}, f(x) = {ga_fit:.6f}")

    sa_x, sa_fit = run_simulated_annealing()
    print(f"Simulated Annealing Result     : x = {sa_x:.6f}, f(x) = {sa_fit:.6f}")
    print("=" * 60)
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "genetic_algorithm.py"
        }
    },
    {
        "id": 12,
        "slug": "n8n-ai-agent-automation",
        "title": "AI Agent for Automation using n8n Workflow Architecture",
        "language": "python",
        "aliases": ["n8n", "ai automation", "agent workflow", "n8n agent", "automation agent"],
        "description": "AI Agent automation framework simulating n8n node routing, LLM intent parsing, and automated tool triggering.",
        "aim": "To create an AI agent for automation using node-based workflow tools like n8n.",
        "theory": (
            "n8n is an open, extensible node-based workflow automation tool connecting REST APIs and enterprise services.\n"
            "An autonomous AI Agent in n8n routes natural language prompts through an LLM reasoning node.\n"
            "The model output is parsed into structured parameters and dispatched to downstream nodes (e.g., Slack, Email, PostgreSQL, Notion) "
            "for autonomous multi-step execution."
        ),
        "algorithm": [
            "Capture user trigger via incoming Webhook / Chat node.",
            "Forward prompt to LLM agent node configured with system prompt and available tools.",
            "Parse model response into target action intent and parameter payload.",
            "Conditionally branch execution through node routing connectors.",
            "Execute automated external service operations and return status to caller."
        ],
        "files": [
            {
                "path": "n8n_agent_simulator.py",
                "source": "n8n_agent_simulator.py",
                "role": "source",
                "content": '''import json
import time

class N8nNode:
    def __init__(self, name: str, node_type: str):
        self.name = name
        self.node_type = node_type

    def execute(self, payload: dict) -> dict:
        print(f"  [Node: {self.name} ({self.node_type})] Executing...")
        time.sleep(0.1)
        return payload

class N8nWorkflowAgent:
    def __init__(self):
        self.nodes = {
            "webhook": N8nNode("Webhook Trigger", "n8n-nodes-base.webhook"),
            "llm": N8nNode("AI Agent LLM Parser", "@n8n/n8n-nodes-langchain.agent"),
            "email": N8nNode("Send Email Notification", "n8n-nodes-base.emailSend"),
            "database": N8nNode("PostgreSQL Logger", "n8n-nodes-base.postgres")
        }

    def process_command(self, user_command: str):
        print(f"\\nProcessing Inbound Task: \\"{user_command}\\"")
        print("-" * 50)

        # 1. Trigger
        data = self.nodes["webhook"].execute({"raw_input": user_command, "timestamp": time.time()})

        # 2. LLM Intent Extraction
        if "email" in user_command.lower() or "alert" in user_command.lower():
            intent = "SEND_EMAIL"
            params = {"recipient": "admin@college.edu", "subject": "Automated Alert", "body": user_command}
        else:
            intent = "DATABASE_LOG"
            params = {"table": "system_events", "record": user_command}

        llm_data = self.nodes["llm"].execute({"intent": intent, "params": params})

        # 3. Dynamic Node Routing
        if intent == "SEND_EMAIL":
            self.nodes["email"].execute(llm_data["params"])
            print("  --> Email successfully dispatched via n8n worker node.")
        else:
            self.nodes["database"].execute(llm_data["params"])
            print("  --> Record committed to database via n8n SQL node.")

        print("-" * 50)
        print("[SUCCESS] n8n AI Agent Workflow Completed!")

def main():
    print("=" * 60)
    print(" LabX Exp 12: AI Agent for Automation using n8n")
    print("=" * 60)

    workflow = N8nWorkflowAgent()
    workflow.process_command("Send urgent email alert about lab attendance drop")
    workflow.process_command("Log daily laboratory usage telemetry")
    print("=" * 60)

if __name__ == "__main__":
    main()
'''
            },
            {
                "path": "n8n_workflow.json",
                "source": "n8n_workflow.json",
                "role": "config",
                "content": '''{
  "name": "LabX AI Agent Automation",
  "nodes": [
    {
      "parameters": {"path": "labx-webhook"},
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {"model": "gpt-4o"},
      "name": "AI Agent",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "position": [450, 300]
    },
    {
      "parameters": {"toEmail": "admin@college.edu"},
      "name": "Email",
      "type": "n8n-nodes-base.emailSend",
      "position": [700, 200]
    }
  ]
}
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "n8n_agent_simulator.py"
        }
    }
]

HTML_INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LabX Remote - AISC Laboratory Experiments</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --accent: #38bdf8;
      --text: #f8fafc;
      --muted: #94a3b8;
      --code-bg: #090d16;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 2rem;
      line-height: 1.6;
    }
    .container {
      max-width: 960px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      margin-bottom: 2.5rem;
      border-bottom: 1px solid #334155;
      padding-bottom: 1.5rem;
    }
    h1 {
      color: var(--accent);
      font-size: 2.4rem;
      margin-bottom: 0.25rem;
    }
    .badge {
      display: inline-block;
      background: #0284c7;
      color: white;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      font-size: 0.85rem;
      font-weight: bold;
    }
    .command-box {
      background: var(--code-bg);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 1.25rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: #7dd3fc;
      margin: 1.5rem 0;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 1.25rem;
      margin-top: 2rem;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .card:hover {
      border-color: #475569;
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }
    .copy-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: #1e3a5f;
      color: #38bdf8;
      border: 1px solid #0284c7;
      border-radius: 6px;
      padding: 0.3rem 0.65rem;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .copy-btn:hover {
      background: #0284c7;
      color: #ffffff;
      transform: translateY(-1px);
    }
    .copy-btn.copied {
      background: #15803d !important;
      color: #ffffff !important;
      border-color: #22c55e !important;
    }
    .card h3 {
      margin: 0.4rem 0;
      color: var(--accent);
      font-size: 1.05rem;
      line-height: 1.35;
    }
    .tag {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: #334155;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      color: #38bdf8;
      display: inline-block;
      font-weight: 600;
    }
    .file-pill {
      font-size: 0.75rem;
      color: #94a3b8;
      background: #0f172a;
      padding: 0.15rem 0.45rem;
      border-radius: 3px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      margin-top: 0.5rem;
      display: inline-block;
      border: 1px solid #1e293b;
    }
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1rem;
      padding-top: 0.75rem;
      border-top: 1px solid #334155;
      font-size: 0.85rem;
    }
    a {
      color: var(--accent);
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>AISC LABORATORY REMOTE</h1>
      <p class="muted">Artificial Intelligence & Soft Computing Experiment Distribution System</p>
      <span class="badge">12 Experiments Live</span>
    </header>

    <section>
      <h2>Terminal Quickstart</h2>
      <div class="command-box">
        <span style="color:#94a3b8"># 1. Ultra-short one-liners in PowerShell (No install needed):</span><br>
        irm https://aisccli.netlify.app/all.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#94a3b8"># Pull ALL 12 experiments</span><br>
        & (irm https://aisccli.netlify.app/get.ps1) 2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#94a3b8"># Pull Exp 2</span><br>
        irm https://aisccli.netlify.app/list.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#94a3b8"># List catalogue</span><br><br>
        <span style="color:#94a3b8"># 2. Or install the global 'labx' CLI:</span><br>
        irm https://aisccli.netlify.app/install.ps1 | iex<br>
        labx list &nbsp;|&nbsp; labx download 2 &nbsp;|&nbsp; labx run 2
      </div>
    </section>

    <section>
      <h2>Available Static Endpoints</h2>
      <ul>
        <li><a href="catalog.json"><code>/catalog.json</code></a> — Complete experiment catalogue API</li>
        <li><a href="version.json"><code>/version.json</code></a> — Remote version metadata</li>
        <li><a href="downloads/labx_experiments.zip"><code>/downloads/labx_experiments.zip</code></a> — Full 12-experiment ZIP archive</li>
        <li><a href="downloads/labx.exe"><code>/downloads/labx.exe</code></a> — Windows standalone executable</li>
      </ul>
    </section>

    <section>
      <h2>AISC Experiment Catalogue</h2>
      <div class="grid">
"""

def generate_host():
    """Build all static hosting artifacts."""
    print("Building AISC LabX distribution backend...")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    DL_DIR.mkdir(parents=True, exist_ok=True)

    # Clean old experiments
    for old_folder in EXP_DIR.iterdir():
        if old_folder.is_dir():
            shutil.rmtree(old_folder)

    # 1. netlify.toml
    netlify_toml = """[build]
  publish = "public"

[[headers]]
  for = "/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, HEAD, OPTIONS"
    Access-Control-Allow-Headers = "*"
    Cache-Control = "public, max-age=3600"

[[headers]]
  for = "/*.json"
  [headers.values]
    Content-Type = "application/json; charset=utf-8"
"""
    with open(HOST_DIR / "netlify.toml", "w", encoding="utf-8") as f:
        f.write(netlify_toml)

    # 2. version.json
    version_data = {
        "version": "1.0.0",
        "updated_at": "2026-10-31T21:00:00Z",
        "platform": "AISC Laboratory Remote Production Backend",
        "total_experiments": len(EXPERIMENTS)
    }
    with open(PUBLIC_DIR / "version.json", "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=2)

    # 3. Create individual experiments and manifests
    catalog_items = []
    zip_staging_dir = HOST_DIR / "temp_zip_staging" / "labx_experiments"
    if zip_staging_dir.parent.exists():
        shutil.rmtree(zip_staging_dir.parent)
    zip_staging_dir.mkdir(parents=True, exist_ok=True)

    html_cards = []

    for exp in EXPERIMENTS:
        exp_id = exp["id"]
        exp_folder_name = f"{exp_id:02d}"
        target_exp_dir = EXP_DIR / exp_folder_name
        target_exp_dir.mkdir(parents=True, exist_ok=True)

        manifest_url = f"experiments/{exp_folder_name}/manifest.json"

        # Catalog entry
        catalog_items.append({
            "id": exp["id"],
            "slug": exp["slug"],
            "title": exp["title"],
            "language": exp["language"],
            "aliases": exp["aliases"],
            "description": exp["description"],
            "manifest_url": manifest_url
        })

        # Write experiment files
        manifest_files = []
        for file_info in exp["files"]:
            file_dest = target_exp_dir / file_info["path"]
            with open(file_dest, "w", encoding="utf-8") as sf:
                sf.write(file_info["content"])
            manifest_files.append({
                "path": file_info["path"],
                "source": file_info["source"],
                "role": file_info.get("role", "source")
            })

        # Manifest JSON
        manifest_dict = {
            "id": exp["id"],
            "slug": exp["slug"],
            "title": exp["title"],
            "language": exp["language"],
            "aliases": exp["aliases"],
            "description": exp["description"],
            "aim": exp["aim"],
            "theory": exp["theory"],
            "algorithm": exp["algorithm"],
            "files": manifest_files,
            "run": exp["run"],
            "version": "1.0.0"
        }
        with open(target_exp_dir / "manifest.json", "w", encoding="utf-8") as mf:
            json.dump(manifest_dict, mf, indent=2)

        # Stage for ZIP archive
        zip_exp_dir = zip_staging_dir / f"Experiment{exp_id:02d}_{exp['slug'].replace('-', '_')}"
        zip_exp_dir.mkdir(parents=True, exist_ok=True)
        for f_info in exp["files"]:
            shutil.copy(target_exp_dir / f_info["path"], zip_exp_dir / f_info["path"])
        shutil.copy(target_exp_dir / "manifest.json", zip_exp_dir / "manifest.json")

        readme_content = f"# Experiment {exp_id:02d}: {exp['title']}\n\n## Aim\n{exp['aim']}\n\n## Description\n{exp['description']}\n\n## Theory\n{exp['theory']}\n"
        with open(zip_exp_dir / "README.md", "w", encoding="utf-8") as rf:
            rf.write(readme_content)

        # Identify primary source code
        py_files = [f for f in exp["files"] if f["path"].endswith(".py")]
        src_file = py_files[0] if py_files else exp["files"][0]
        src_name = src_file["path"]
        src_code = src_file["content"]
        escaped_code = html.escape(src_code)

        # HTML card
        html_cards.append(f"""        <div class="card">
          <div>
            <div class="card-top">
              <span class="tag">{exp['language']}</span>
              <button class="copy-btn" onclick="copyExpCode(this, 'code-{exp_id}')" title="Copy {src_name} source code">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>Copy Code</span>
              </button>
            </div>
            <textarea id="code-{exp_id}" style="display:none;">{escaped_code}</textarea>
            <h3>#{exp_id:02d} {exp['title']}</h3>
            <p style="color:#cbd5e1; font-size:0.9rem; margin:0.4rem 0;">{exp['description']}</p>
            <span class="file-pill">{src_name}</span>
          </div>
          <div class="card-footer">
            <a href="experiments/{exp_id:02d}/{src_name}" target="_blank">View File &rarr;</a>
            <a href="{manifest_url}" target="_blank">Manifest &rarr;</a>
          </div>
        </div>""")

    # 4. Write catalog.json
    catalog_data = {
        "version": "1.0.0",
        "updated_at": "2026-10-31T21:00:00Z",
        "zip_url": "downloads/labx_experiments.zip",
        "experiments": catalog_items
    }
    with open(PUBLIC_DIR / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)

    # 5. Build full labx_experiments.zip
    zip_out_file = DL_DIR / "labx_experiments.zip"
    print(f"Building complete ZIP archive at {zip_out_file}...")
    with zipfile.ZipFile(zip_out_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_dir.parent):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_dir.parent)
                zf.write(full_path, arcname=str(rel_path).replace("\\", "/"))

    shutil.rmtree(zip_staging_dir.parent)

    # 6. Complete index.html
    full_html = HTML_INDEX + "\n".join(html_cards) + """
      </div>
    </section>
  </div>
  <script>
    function copyExpCode(btn, codeId) {
      const ta = document.getElementById(codeId);
      if (!ta) return;
      const text = ta.value;
      const span = btn.querySelector('span');
      const originalText = span.textContent;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          btn.classList.add('copied');
          span.textContent = 'Copied!';
          setTimeout(() => {
            btn.classList.remove('copied');
            span.textContent = originalText;
          }, 2000);
        }).catch(() => fallbackCopy(ta, btn, span, originalText));
      } else {
        fallbackCopy(ta, btn, span, originalText);
      }
    }

    function fallbackCopy(ta, btn, span, originalText) {
      ta.style.display = 'block';
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        btn.classList.add('copied');
        span.textContent = 'Copied!';
      } catch (err) {
        alert('Please manually copy the code from View File.');
      }
      ta.style.display = 'none';
      setTimeout(() => {
        btn.classList.remove('copied');
        span.textContent = originalText;
      }, 2000);
    }
  </script>
</body>
</html>"""
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as hf:
        hf.write(full_html)

    # Copy binary into downloads if present in dist
    dist_exe = BASE_DIR / "dist" / "labx.exe"
    if dist_exe.exists():
        shutil.copy(dist_exe, DL_DIR / "labx.exe")

    # Copy install.ps1
    install_script = BASE_DIR / "scripts" / "install_windows.ps1"
    if install_script.exists():
        shutil.copy(install_script, PUBLIC_DIR / "install.ps1")

    # Generate ultra-short one-liner shell helpers
    all_ps1 = """$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all 12 AISC experiments from LabX Remote..." -ForegroundColor Cyan
Invoke-WebRequest "https://aisccli.netlify.app/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 12 experiments extracted to current directory!" -ForegroundColor Green
"""
    with open(PUBLIC_DIR / "all.ps1", "w", encoding="utf-8") as f:
        f.write(all_ps1)

    list_ps1 = """$cat = Invoke-RestMethod "https://aisccli.netlify.app/catalog.json"
Write-Host "`n==== AISC Laboratory Experiments (LabX Remote) ====" -ForegroundColor Cyan
$cat.experiments | Format-Table @{Label="ID"; Expression={"Exp " + ("{0:D2}" -f $_.id)}}, @{Label="Title"; Expression={$_.title}}, @{Label="Language"; Expression={$_.language}}
Write-Host "Quick commands:" -ForegroundColor Yellow
Write-Host "  Pull all experiments : irm https://aisccli.netlify.app/all.ps1 | iex" -ForegroundColor White
Write-Host "  Pull one experiment  : & (irm https://aisccli.netlify.app/get.ps1) <id>`n" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "list.ps1", "w", encoding="utf-8") as f:
        f.write(list_ps1)

    get_ps1 = """param($Id)
if (-not $Id) {
    $Id = Read-Host "Enter experiment number (1-12)"
}
$num = "{0:D2}" -f [int]$Id
$cat = (Invoke-RestMethod "https://aisccli.netlify.app/catalog.json").experiments | Where-Object { $_.id -eq [int]$Id }
if (-not $cat) {
    Write-Host "[!] Experiment $Id not found in catalogue." -ForegroundColor Red
    return
}
$mf = Invoke-RestMethod "https://aisccli.netlify.app/$($cat.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://aisccli.netlify.app/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($cat.title) into $dir/" -ForegroundColor Green
"""
    with open(PUBLIC_DIR / "get.ps1", "w", encoding="utf-8") as f:
        f.write(get_ps1)

    all_sh = """#!/usr/bin/env bash
echo "Downloading all 12 AISC experiments..."
curl -sLO https://aisccli.netlify.app/downloads/labx_experiments.zip && unzip -q -o labx_experiments.zip && rm labx_experiments.zip
echo "[OK] All 12 experiments downloaded into $(pwd)!"
"""
    with open(PUBLIC_DIR / "all.sh", "w", encoding="utf-8") as f:
        f.write(all_sh)

    print(f"Successfully generated all {len(EXPERIMENTS)} AISC experiments!")

if __name__ == "__main__":
    generate_host()
