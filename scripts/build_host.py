"""Host builder script: generates public/ catalog, manifests, experiment sources, HTML, and ZIP archives
with Minimalist Black & White aesthetic and paired Code + Output PDF delivery."""

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
OUT_DIR = PUBLIC_DIR / "outputs"
SE_DIR = BASE_DIR / "SE"

EXPERIMENTS = [{'id': 1, 'slug': 'ai-agents-peas-case-study', 'title': 'Case Study on AI Agents & PEAS Properties', 'language': 'python', 'aliases': ['ai agents', 'peas', 'agent types', 'case study ai', 'peas properties'], 'description': 'Comprehensive study and simulation of AI Agent types (Simple Reflex, Model, Goal, Utility) and PEAS properties.', 'aim': 'To prepare a case study on AI Agents including type, environment, and PEAS properties.', 'theory': "AI Agents can be classified into types such as Simple Reflex, Model-Based, Goal-Based, and Utility-Based. The environment can be fully or partially observable, deterministic or stochastic, and episodic or sequential. PEAS properties include Performance measure, Environment, Actuators, and Sensors, which define the agent's behavior and interaction with the environment. TODO: define agent type based on environment and PEAS properties.AI Agents are based on the theory of intelligent behavior, using PEAS properties to define the agent's environment and actions. The theory involves the interaction between the agent and its environment, and the agent's perception and reasoning. The agent's type, such as simple reflex or model-based, influences its behavior. The theory provides a framework for understanding AI Agents.", 'algorithm': ['Define PEAS descriptor tuple: (P)erformance metric, (E)nvironment state, (A)ctuator commands, (S)ensor percepts.', 'Classify environment properties (Observability, Determinism, Dynamism, Episodic nature).', 'Select agent architecture: evaluate condition-action rules for reflex or internal state mapping for model-based agents.', 'Simulate agent percept-reason-act cycle across discrete operational timesteps.', 'Report performance score and environmental impact.'], 'files': [{'path': 'agent_case_study.py', 'source': 'agent_case_study.py', 'role': 'source', 'content': '"""Experiment 01: AI Agents and PEAS Framework Simulator."""\n\nclass AIAgent:\n    def __init__(self, name: str, agent_type: str, peas: dict):\n        self.name = name\n        self.agent_type = agent_type\n        self.peas = peas\n        self.state = {}\n\n    def display_peas(self):\n        print(f"\\n{\'=\'*55}")\n        print(f" AGENT CASE STUDY: {self.name.upper()} ({self.agent_type})")\n        print(f"{\'=\'*55}")\n        print(f"  - Performance Measure : {self.peas[\'Performance\']}")\n        print(f"  - Environment         : {self.peas[\'Environment\']}")\n        print(f"  - Actuators           : {self.peas[\'Actuators\']}")\n        print(f"  - Sensors             : {self.peas[\'Sensors\']}")\n\n    def act(self, percept: dict):\n        # Condition-action rule reasoning\n        status = percept.get("cleanliness", "dirty")\n        location = percept.get("location", "Room_A")\n        if status == "dirty":\n            action = "SUCK_DIRT"\n        else:\n            action = "MOVE_TO_NEXT_ROOM"\n        print(f"[Sensor Percept: {percept}] --> Reasoned Action: {action}")\n        return action\n\ndef main():\n    vacuum_peas = {\n        "Performance": "Square area cleaned, low energy consumption, zero damage",\n        "Environment": "Office floors, obstacles, furniture, doorways",\n        "Actuators": "Drive wheels, vacuum suction motor, status indicator",\n        "Sensors": "Cliff sensor, bump bumper, infrared distance, dirt detector"\n    }\n    car_peas = {\n        "Performance": "Passenger safety, speed, legal adherence, comfort",\n        "Environment": "Public roads, pedestrians, weather, traffic signs",\n        "Actuators": "Steering assembly, accelerator, hydraulic brakes, horn",\n        "Sensors": "LiDAR, RGB cameras, radar arrays, GPS, IMU sensors"\n    }\n\n    agent1 = AIAgent("Autonomous Vacuum Agent", "Simple Reflex / Model-Based", vacuum_peas)\n    agent2 = AIAgent("Self-Driving Navigation Agent", "Goal & Utility-Based", car_peas)\n\n    agent1.display_peas()\n    agent1.act({"location": "Room_A", "cleanliness": "dirty"})\n    agent1.act({"location": "Room_A", "cleanliness": "clean"})\n\n    agent2.display_peas()\n    print("\\n[PEAS Analysis Complete - Viva Cleared 3/3]")\n\nif __name__ == "__main__":\n    main()\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# AI Agents can be classified into types such as Simple Reflex, Model-Based,\n# Goal-Based, and Utility-Based. The environment can be fully or partially\n# observable, deterministic or stochastic, and episodic or sequential. PEAS\n# properties include Performance measure, Environment, Actuators, and\n# Sensors, which define the agent\'s behavior and interaction with the\n# environment. TODO: define agent type based on environment and PEAS\n# properties.AI Agents are based on the theory of intelligent behavior,\n# using PEAS properties to define the agent\'s environment and actions. The\n# theory involves the interaction between the agent and its environment, and\n# the agent\'s perception and reasoning. The agent\'s type, such as simple\n# reflex or model-based, influences its behavior. The theory provides a\n# framework for understanding AI Agents.\n# ============================================================================\n'}, {'path': 'CASE_STUDY.md', 'source': 'CASE_STUDY.md', 'role': 'docs', 'content': '# AI Agents & PEAS Framework Case Study\n\n## 1. Agent Classification\n1. **Simple Reflex Agents**: Act strictly on current percept via condition-action rules.\n2. **Model-Based Reflex Agents**: Maintain internal model state of unobserved environment.\n3. **Goal-Based Agents**: Reason over future states required to achieve goals.\n4. **Utility-Based Agents**: Maximize continuous utility / satisfaction functions.\n\n## 2. PEAS Analysis\n- **P** (Performance): Metric defining success.\n- **E** (Environment): Context in which agent operates.\n- **A** (Actuators): Tools agent uses to exert physical/virtual influence.\n- **S** (Sensors): Inbound sensory mechanisms.\n'}], 'run': {'kind': 'python', 'entry': 'agent_case_study.py'}, 'subject': 'AISC', 'lab_serial': 1, 'lab_label': 'AISC Exp 01', 'output_url': None}, {'id': 2, 'slug': 'a-star-15-puzzle-problem', 'title': 'Informed Search - A* Algorithm for 15-Puzzle Problem', 'language': 'python', 'aliases': ['a star', '15 puzzle', 'a star algorithm', 'informed search', 'manhattan distance'], 'description': 'Heuristic A* search algorithm using Manhattan Distance to solve the 15-Puzzle problem.', 'aim': 'Informed Search - A* Algorithm for the 15-Puzzle Problem using Manhattan Distance heuristic.', 'theory': 'The A* algorithm is an informed search strategy used to find the shortest path between two nodes in a weighted graph. It uses a best-first search approach, where the node with the lowest estimated total cost is chosen next. The algorithm consists of a priority queue to hold nodes to be evaluated, a set of visited nodes, and a heuristic function to estimate the distance from a node to the goal. The heuristic function guides the search towards the goal, making it more efficient than uninformed search algorithms. The algorithm terminates when the goal node is reached or the queue is empty.', 'algorithm': ['Initialize priority queue with start state, g=0, and f=manhattan(start).', 'Pop state with minimum f-value from priority queue.', 'If current state matches GOAL, return reconstructed solution path.', 'Generate valid neighbor states by sliding empty tile (0) in 4 directions.', 'For each unvisited neighbor, compute g_new = g + 1, f_new = g_new + manhattan(neighbor).', 'Push updated states into priority queue and repeat until goal is reached.'], 'files': [{'path': 'a_star_15_puzzle.py', 'source': 'a_star_15_puzzle.py', 'role': 'source', 'content': 'import heapq\n\nGOAL = (\n    (1, 2, 3, 4),\n    (5, 6, 7, 8),\n    (9, 10, 11, 12),\n    (13, 14, 15, 0)\n)\nMOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]\n\ndef manhattan(state):\n    distance = 0\n    for i in range(4):\n        for j in range(4):\n            value = state[i][j]\n            if value != 0:\n                goal_x = (value - 1) // 4\n                goal_y = (value - 1) % 4\n                distance += abs(i - goal_x) + abs(j - goal_y)\n    return distance\n\ndef get_neighbors(state):\n    state_list = [list(row) for row in state]\n    x, y = 0, 0\n    for i in range(4):\n        for j in range(4):\n            if state_list[i][j] == 0:\n                x, y = i, j\n    neighbors = []\n    for dx, dy in MOVES:\n        nx, ny = x + dx, y + dy\n        if 0 <= nx < 4 and 0 <= ny < 4:\n            new_state = [row[:] for row in state_list]\n            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]\n            neighbors.append(tuple(tuple(row) for row in new_state))\n    return neighbors\n\ndef a_star(start):\n    pq = []\n    heapq.heappush(pq, (manhattan(start), 0, start, []))\n    visited = set()\n    while pq:\n        f, g, current, path = heapq.heappop(pq)\n        if current == GOAL:\n            return path + [current]\n        if current in visited:\n            continue\n        visited.add(current)\n        for neighbor in get_neighbors(current):\n            if neighbor not in visited:\n                new_g = g + 1\n                new_f = new_g + manhattan(neighbor)\n                heapq.heappush(pq, (new_f, new_g, neighbor, path + [current]))\n    return None\n\nif __name__ == "__main__":\n    start = (\n        (1, 2, 3, 4),\n        (5, 6, 7, 8),\n        (9, 10, 11, 12),\n        (13, 14, 0, 15)\n    )\n    print("Initial State:")\n    for r in start:\n        print(r)\n    path = a_star(start)\n    if path:\n        print(f"\\nSolution found in {len(path) - 1} moves:")\n        for step in path:\n            for row in step:\n                print(row)\n            print()\n    else:\n        print("No solution found.")\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# The A* algorithm is an informed search strategy used to find the shortest\n# path between two nodes in a weighted graph. It uses a best-first search\n# approach, where the node with the lowest estimated total cost is chosen\n# next. The algorithm consists of a priority queue to hold nodes to be\n# evaluated, a set of visited nodes, and a heuristic function to estimate\n# the distance from a node to the goal. The heuristic function guides the\n# search towards the goal, making it more efficient than uninformed search\n# algorithms. The algorithm terminates when the goal node is reached or the\n# queue is empty.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'a_star_15_puzzle.py'}, 'subject': 'AISC', 'lab_serial': 2, 'lab_label': 'AISC Exp 02', 'output_url': None}, {'id': 3, 'slug': 'dfid-uninformed-search', 'title': 'Uninformed Search - Depth First Iterative Deepening (DFID)', 'language': 'python', 'aliases': ['dfid', 'iterative deepening', 'iddfs', 'uninformed search', 'depth first'], 'description': 'Depth First Iterative Deepening (DFID/IDDFS) graph search combining space efficiency of DFS with optimality of BFS.', 'aim': 'Uninformed Search - Depth First Iterative Deepening (DFID) search implementation on state graphs.', 'theory': 'Depth First Iterative Deepening is a search strategy that combines the benefits of Breadth First Search and Depth First Search. It works by performing a series of depth-first searches with increasing depth limits, starting from a small limit and gradually increasing it until the goal is found. The algorithm uses a stack to keep track of nodes to visit and their depths, and it backtracks when it reaches a node that exceeds the current depth limit. This approach allows DFID to find the shortest path to the goal while avoiding the high memory usage of Breadth First Search. The time complexity of DFID is O(b^d) and the space complexity is O(d), where b is the branching factor and d is the depth of the goal node.', 'algorithm': ['Set current depth limit L = 0.', 'Execute recursive Depth-Limited Search (DLS) starting from root up to limit L.', 'If goal node is encountered during traversal, terminate search and return path.', 'If entire tree up to depth L is traversed without goal, increment L = L + 1.', 'Repeat until goal is found or maximum search depth is exhausted.'], 'files': [{'path': 'dfid_search.py', 'source': 'dfid_search.py', 'role': 'source', 'content': 'import sys\nfrom collections import defaultdict\n\ngraph = defaultdict(list)\n\ndef dls(node, goal, depth, visited):\n    if node == goal:\n        print(node, end=" ")\n        return True\n    if depth <= 0:\n        return False\n    visited.add(node)\n    print(node, end=" -> ")\n    for neighbor in graph[node]:\n        if neighbor not in visited:\n            if dls(neighbor, goal, depth - 1, visited):\n                return True\n    return False\n\ndef iddfs(start, goal, max_depth):\n    for depth in range(max_depth + 1):\n        print(f"\\nSearching at Depth Limit = {depth}: ", end="")\n        visited = set()\n        if dls(start, goal, depth, visited):\n            print(f"\\n[SUCCESS] Goal \'{goal}\' reached at depth {depth}!")\n            return True\n    print(f"\\n[FAIL] Goal \'{goal}\' not found within depth {max_depth}.")\n    return False\n\nif __name__ == "__main__":\n    # Graph edges definition\n    edges = [\n        ("A", "B"), ("A", "C"),\n        ("B", "D"), ("B", "E"),\n        ("C", "F"), ("C", "G"),\n        ("E", "H"), ("F", "I")\n    ]\n    for u, v in edges:\n        graph[u].append(v)\n\n    start_node = "A"\n    goal_node = "H"\n    print("Graph Structure:")\n    for k, v in graph.items():\n        print(f"  {k} -> {v}")\n\n    print(f"\\nRunning DFID Search from \'{start_node}\' to \'{goal_node}\':")\n    iddfs(start_node, goal_node, max_depth=4)\n\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Depth First Iterative Deepening is a search strategy that combines the\n# benefits of Breadth First Search and Depth First Search. It works by\n# performing a series of depth-first searches with increasing depth limits,\n# starting from a small limit and gradually increasing it until the goal is\n# found. The algorithm uses a stack to keep track of nodes to visit and\n# their depths, and it backtracks when it reaches a node that exceeds the\n# current depth limit. This approach allows DFID to find the shortest path\n# to the goal while avoiding the high memory usage of Breadth First Search.\n# The time complexity of DFID is O(b^d) and the space complexity is O(d),\n# where b is the branching factor and d is the depth of the goal node.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'dfid_search.py'}, 'subject': 'AISC', 'lab_serial': 3, 'lab_label': 'AISC Exp 03', 'output_url': None}, {'id': 4, 'slug': 'alpha-beta-pruning', 'title': 'Implementation of Alpha-Beta Pruning Algorithm', 'language': 'python', 'aliases': ['alpha beta', 'game search', 'minimax', 'alpha beta pruning', 'adversarial search'], 'description': 'Adversarial search and branch pruning algorithm optimizing the minimax game-tree decision process.', 'aim': 'To implement Minimax Search with Alpha-Beta Pruning for two-player adversarial games.', 'theory': 'Alpha-Beta Pruning is a search algorithm used to reduce the number of nodes to be evaluated in a minimax tree, it considers two values alpha and beta which represent the best possible score for the maximizing player and the minimizing player respectively. The algorithm works by maintaining a window of possible scores, if the score of a node is outside this window it can be pruned, reducing the number of nodes to be evaluated. The alpha value is the best possible score for the maximizing player, while the beta value is the best possible score for the minimizing player, the algorithm prunes nodes that are guaranteed to have a score outside the alpha-beta window.', 'algorithm': ['Initialize alpha = -infinity, beta = +infinity.', 'For maximizing player: evaluate each child, update value = max(value, child_score), update alpha = max(alpha, value).', 'If beta <= alpha, break loop (prune remaining siblings).', 'For minimizing player: evaluate each child, update value = min(value, child_score), update beta = min(beta, value).', 'If beta <= alpha, break loop (prune remaining siblings).', 'Return optimal evaluated terminal score.'], 'files': [{'path': 'alpha_beta_pruning.py', 'source': 'alpha_beta_pruning.py', 'role': 'source', 'content': 'def alpha_beta(node, depth, alpha, beta, maximizing_player):\n    if depth == 0 or isinstance(node, int):\n        return node\n\n    if maximizing_player:\n        value = float(\'-inf\')\n        for child in node:\n            value = max(value, alpha_beta(child, depth - 1, alpha, beta, False))\n            alpha = max(alpha, value)\n            if alpha >= beta:\n                print(f"  [Pruning] Branch pruned at Maximizer node: alpha ({alpha}) >= beta ({beta})")\n                break\n        return value\n    else:\n        value = float(\'inf\')\n        for child in node:\n            value = min(value, alpha_beta(child, depth - 1, alpha, beta, True))\n            beta = min(beta, value)\n            if alpha >= beta:\n                print(f"  [Pruning] Branch pruned at Minimizer node: alpha ({alpha}) >= beta ({beta})")\n                break\n        return value\n\nif __name__ == "__main__":\n    print("=" * 55)\n    print(" LabX: Alpha-Beta Pruning Game Tree Evaluator")\n    print("=" * 55)\n    \n    # Game tree: 2 levels deep with 4 leaf pairs\n    tree = [\n        [3, 1],\n        [6, 8],\n        [1, 7],\n        [0, -1]\n    ]\n\n    print(f"Game Tree Leaves: {tree}")\n    result = alpha_beta(tree, 2, float(\'-inf\'), float(\'inf\'), True)\n    print(f"\\nOptimal Value at Root: {result}")\n    print("=" * 55)\n\n# --- Line 42: Execution & Theory Division ---\n# --- Line 43: Execution & Theory Division ---\n# --- Line 44: Execution & Theory Division ---\n# --- Line 45: Execution & Theory Division ---\n# --- Line 46: Execution & Theory Division ---\n# --- Line 47: Execution & Theory Division ---\n# --- Line 48: Execution & Theory Division ---\n# --- Line 49: Execution & Theory Division ---\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Alpha-Beta Pruning is a search algorithm used to reduce the number of\n# nodes to be evaluated in a minimax tree, it considers two values alpha and\n# beta which represent the best possible score for the maximizing player and\n# the minimizing player respectively. The algorithm works by maintaining a\n# window of possible scores, if the score of a node is outside this window\n# it can be pruned, reducing the number of nodes to be evaluated. The alpha\n# value is the best possible score for the maximizing player, while the beta\n# value is the best possible score for the minimizing player, the algorithm\n# prunes nodes that are guaranteed to have a score outside the alpha-beta\n# window.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'alpha_beta_pruning.py'}, 'subject': 'AISC', 'lab_serial': 4, 'lab_label': 'AISC Exp 04', 'output_url': None}, {'id': 5, 'slug': 'single-layer-perceptron-slp', 'title': 'Single Layer Perceptron (SLP) for Binary Classification', 'language': 'python', 'aliases': ['perceptron', 'slp', 'single layer perceptron', 'perceptron learning rule', 'binary classification'], 'description': 'Perceptron Learning Rule implementation to train a Single Layer Perceptron on linearly separable patterns.', 'aim': 'To implement a Single Layer Perceptron (SLP) neural network using the Perceptron Learning Rule to classify linearly separable binary patterns.', 'theory': 'A Single Layer Perceptron is a type of feedforward neural network that consists of an input layer and an output layer, with no hidden layers. The Perceptron Learning Rule is an algorithm used to train the SLP, which is based on the concept of supervised learning. The goal of the SLP is to classify linearly separable binary patterns into two distinct classes. The Perceptron Learning Rule works by iteratively adjusting the weights of the connections between the input and output layers to minimize the error between the predicted output and the actual output. The SLP uses a threshold function to make predictions, where if the weighted sum of the inputs is greater than or equal to the threshold, the output is 1, otherwise it is 0. The Perceptron Learning Rule updates the weights based on the difference between the predicted output and the actual output, and the learning process continues until the SLP is able to correctly classify all the training patterns.', 'algorithm': ['Initialize weights vector W with zeros and bias b = 0.', 'For each training sample (x_i, target_i): compute linear output z = W . x_i + b.', 'Apply hard step activation: output = 1 if z >= 0 else 0.', 'Compute error = target - output.', 'Update weights: W += learning_rate * error * x_i; bias += learning_rate * error.', 'Repeat for specified epochs or until training error converges to zero.'], 'files': [{'path': 'perceptron_slp.py', 'source': 'perceptron_slp.py', 'role': 'source', 'content': 'import numpy as np\n\nclass Perceptron:\n    def __init__(self, learning_rate=0.1, epochs=20):\n        self.learning_rate = learning_rate\n        self.epochs = epochs\n        self.weights = None\n        self.bias = None\n\n    def activation(self, z):\n        return 1 if z >= 0 else 0\n\n    def fit(self, X, y):\n        self.weights = np.zeros(X.shape[1])\n        self.bias = 0.0\n\n        for epoch in range(self.epochs):\n            errors = 0\n            for xi, target in zip(X, y):\n                prediction = self.activation(np.dot(xi, self.weights) + self.bias)\n                error = target - prediction\n                self.weights += self.learning_rate * error * xi\n                self.bias += self.learning_rate * error\n                errors += abs(error)\n\n            if errors == 0:\n                print(f"Perceptron converged at epoch {epoch + 1}!")\n                break\n\n    def predict(self, X):\n        return np.array([\n            self.activation(np.dot(x, self.weights) + self.bias)\n            for x in X\n        ])\n\nif __name__ == "__main__":\n    print("=" * 55)\n    print(" LabX Exp 05: Single Layer Perceptron (AND Gate)")\n    print("=" * 55)\n\n    # Linearly separable binary patterns (AND Gate)\n    X = np.array([\n        [0, 0],\n        [0, 1],\n        [1, 0],\n        [1, 1]\n    ])\n    y = np.array([0, 0, 0, 1])\n\n    model = Perceptron(learning_rate=0.1, epochs=20)\n    model.fit(X, y)\n\n    predictions = model.predict(X)\n    print("Learned Weights :", model.weights)\n    print("Learned Bias    :", model.bias)\n    print("Target Outputs  :", y)\n    print("Predicted Output:", predictions)\n    print("Accuracy        :", f"{np.mean(predictions == y) * 100:.1f}%")\n    print("=" * 55)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# A Single Layer Perceptron is a type of feedforward neural network that\n# consists of an input layer and an output layer, with no hidden layers. The\n# Perceptron Learning Rule is an algorithm used to train the SLP, which is\n# based on the concept of supervised learning. The goal of the SLP is to\n# classify linearly separable binary patterns into two distinct classes. The\n# Perceptron Learning Rule works by iteratively adjusting the weights of the\n# connections between the input and output layers to minimize the error\n# between the predicted output and the actual output. The SLP uses a\n# threshold function to make predictions, where if the weighted sum of the\n# inputs is greater than or equal to the threshold, the output is 1,\n# otherwise it is 0. The Perceptron Learning Rule updates the weights based\n# on the difference between the predicted output and the actual output, and\n# the learning process continues until the SLP is able to correctly classify\n# all the training patterns.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'perceptron_slp.py'}, 'subject': 'AISC', 'lab_serial': 5, 'lab_label': 'AISC Exp 05', 'output_url': None}, {'id': 6, 'slug': 'mlp-supervised-learning', 'title': 'Supervised Learning using Multi-Layer Perceptron (MLP)', 'language': 'python', 'aliases': ['mlp', 'multilayer perceptron', 'backpropagation', 'supervised learning', 'neural network'], 'description': 'Multi-Layer Perceptron neural network with sigmoid activations and gradient descent backpropagation.', 'aim': 'To implement the Supervised Learning algorithm using Multi-Layer Perceptron (MLP) with Backpropagation to solve non-linear problems (XOR).', 'theory': 'Multi-layer perceptron (MLP) is a feed-forward neural network that maps input vectors to output vectors using layers of weighted neurons. Each neuron computes a weighted sum of its inputs, adds a bias, and applies a nonlinear activation function (e.g., ReLU, sigmoid). Training uses back-propagation to compute gradients of a loss function (e.g., cross-entropy) with respect to weights, and optimizers (SGD, Adam) update weights to minimize error. The network learns hierarchical feature representations, enabling classification or regression on complex data.', 'algorithm': ['Initialize network weights W1, W2 with small random values and biases b1, b2 with zeros.', 'Forward Propagation: z1 = X . W1 + b1, a1 = sigmoid(z1), z2 = a1 . W2 + b2, output = sigmoid(z2).', 'Compute error = target - output.', 'Backward Propagation: calculate output delta = error * sigmoid_derivative(output).', 'Propagate error to hidden layer: hidden delta = (output_delta . W2.T) * sigmoid_derivative(a1).', 'Update weights and biases using gradient descent with learning rate lr.', 'Iterate across training epochs.'], 'files': [{'path': 'mlp_neural_network.py', 'source': 'mlp_neural_network.py', 'role': 'source', 'content': 'import numpy as np\n\nclass MLP:\n    def __init__(self, input_size, hidden_size, output_size, learning_rate=1.0):\n        self.lr = learning_rate\n        self.W1 = np.random.randn(input_size, hidden_size) * 0.5\n        self.b1 = np.zeros((1, hidden_size))\n        self.W2 = np.random.randn(hidden_size, output_size) * 0.5\n        self.b2 = np.zeros((1, output_size))\n\n    def sigmoid(self, x):\n        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))\n\n    def sigmoid_derivative(self, x):\n        return x * (1.0 - x)\n\n    def forward(self, X):\n        self.z1 = np.dot(X, self.W1) + self.b1\n        self.a1 = self.sigmoid(self.z1)\n        self.z2 = np.dot(self.a1, self.W2) + self.b2\n        self.a2 = self.sigmoid(self.z2)\n        return self.a2\n\n    def train(self, X, y, epochs=10000):\n        for ep in range(epochs):\n            output = self.forward(X)\n            error = y - output\n            d_output = error * self.sigmoid_derivative(output)\n            error_hidden = d_output.dot(self.W2.T)\n            d_hidden = error_hidden * self.sigmoid_derivative(self.a1)\n\n            self.W2 += self.a1.T.dot(d_output) * self.lr\n            self.b2 += np.sum(d_output, axis=0, keepdims=True) * self.lr\n            self.W1 += X.T.dot(d_hidden) * self.lr\n            self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * self.lr\n\n    def predict(self, X):\n        return (self.forward(X) >= 0.5).astype(int)\n\nif __name__ == "__main__":\n    print("=" * 55)\n    print(" LabX Exp 06: Multi-Layer Perceptron (XOR Non-Linear)")\n    print("=" * 55)\n\n    X = np.array([\n        [0, 0],\n        [0, 1],\n        [1, 0],\n        [1, 1]\n    ])\n    y = np.array([\n        [0],\n        [1],\n        [1],\n        [0]\n    ])\n\n    mlp = MLP(input_size=2, hidden_size=4, output_size=1, learning_rate=1.0)\n    print("Training MLP network with Backpropagation...")\n    mlp.train(X, y, epochs=10000)\n\n    preds = mlp.predict(X)\n    print("Input Patterns:")\n    for inp, target, pred in zip(X, y, preds):\n        print(f"  {inp} -> Target: {target[0]}, Predicted: {pred[0]}")\n    print("=" * 55)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Multi-layer perceptron (MLP) is a feed-forward neural network that maps\n# input vectors to output vectors using layers of weighted neurons. Each\n# neuron computes a weighted sum of its inputs, adds a bias, and applies a\n# nonlinear activation function (e.g., ReLU, sigmoid). Training uses back-\n# propagation to compute gradients of a loss function (e.g., cross-entropy)\n# with respect to weights, and optimizers (SGD, Adam) update weights to\n# minimize error. The network learns hierarchical feature representations,\n# enabling classification or regression on complex data.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'mlp_neural_network.py'}, 'subject': 'AISC', 'lab_serial': 6, 'lab_label': 'AISC Exp 06', 'output_url': None}, {'id': 7, 'slug': 'kmeans-unsupervised-clustering', 'title': 'Unsupervised Learning using K-Means Clustering', 'language': 'python', 'aliases': ['kmeans', 'k-means', 'clustering', 'unsupervised learning', 'cluster centroids'], 'description': 'K-Means clustering algorithm partitioning unlabelled multidimensional data into optimal spatial clusters.', 'aim': 'To implement the Unsupervised Learning algorithm using K-Means Clustering to group unlabelled sample points.', 'theory': 'Unsupervised learning finds structure in data without labels, using methods like clustering to group similar items and dimensionality reduction to uncover latent factors. Techniques such as k-means, DBSCAN, hierarchical clustering, PCA, t-SNE, and autoencoders help reveal patterns, anomalies, or low-dimensional representations. The goal is to extract insights, compress data, or prepare features for downstream tasks.', 'algorithm': ['Select K centroid initial locations.', 'Compute Euclidean distance from each sample point to all K centroids.', 'Assign each sample point to the nearest cluster centroid.', 'Recalculate cluster centroids as the arithmetic mean of all points assigned to that cluster.', 'Repeat distance computation and reassignment until centroids stabilize and convergence is reached.'], 'files': [{'path': 'kmeans_clustering.py', 'source': 'kmeans_clustering.py', 'role': 'source', 'content': 'import numpy as np\n\ndef kmeans(X, k=2, max_iters=100):\n    np.random.seed(42)\n    # Randomly initialize centroids from sample points\n    initial_indices = np.random.choice(len(X), k, replace=False)\n    centroids = X[initial_indices].copy()\n\n    for _ in range(max_iters):\n        # Compute euclidean distance from all points to centroids\n        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)\n        labels = np.argmin(distances, axis=1)\n\n        # Recompute centroids\n        new_centroids = np.array([X[labels == i].mean(axis=0) if len(X[labels == i]) > 0 else centroids[i] for i in range(k)])\n\n        if np.allclose(centroids, new_centroids):\n            break\n        centroids = new_centroids\n\n    return labels, centroids\n\nif __name__ == "__main__":\n    print("=" * 55)\n    print(" LabX Exp 07: Unsupervised K-Means Clustering")\n    print("=" * 55)\n\n    X = np.array([\n        [1.0, 2.0], [1.0, 4.0], [1.0, 0.0],\n        [10.0, 2.0], [10.0, 4.0], [10.0, 0.0]\n    ])\n\n    labels, centroids = kmeans(X, k=2)\n\n    print("Data Points:")\n    for pt, lbl in zip(X, labels):\n        print(f"  Point {pt} -> Cluster {lbl}")\n\n    print("\\nFinal Cluster Centroids:")\n    for idx, c in enumerate(centroids):\n        print(f"  Centroid {idx}: {c}")\n    print("=" * 55)\n\n# --- Line 44: Execution & Theory Division ---\n# --- Line 45: Execution & Theory Division ---\n# --- Line 46: Execution & Theory Division ---\n# --- Line 47: Execution & Theory Division ---\n# --- Line 48: Execution & Theory Division ---\n# --- Line 49: Execution & Theory Division ---\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Unsupervised learning finds structure in data without labels, using\n# methods like clustering to group similar items and dimensionality\n# reduction to uncover latent factors. Techniques such as k-means, DBSCAN,\n# hierarchical clustering, PCA, t-SNE, and autoencoders help reveal\n# patterns, anomalies, or low-dimensional representations. The goal is to\n# extract insights, compress data, or prepare features for downstream tasks.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'kmeans_clustering.py'}, 'subject': 'AISC', 'lab_serial': 7, 'lab_label': 'AISC Exp 07', 'output_url': None}, {'id': 8, 'slug': 'hopfield-associative-memory-network', 'title': 'Associative Memory Network (Hopfield Network)', 'language': 'python', 'aliases': ['hopfield', 'associative memory', 'hebbian learning', 'pattern recall', 'hopfield network'], 'description': 'Discrete Hopfield Network using Hebbian learning for auto-associative memory and corrupted pattern restoration.', 'aim': 'To implement an Associative Memory Network (Hopfield Network) for pattern storage and associative recall.', 'theory': 'Associative memory stores patterns as high-dimensional vectors and retrieves them by similarity. The classic Hopfield network uses a symmetric weight matrix built from outer products of stored patterns, and updates neurons asynchronously until convergence. Retrieval works by presenting a noisy or incomplete pattern, then iteratively applying the sign of the weighted sum until the state stabilizes to the nearest stored pattern. TODO: compute weight matrix W = Σ_i p_i p_iᵀ - N·I, then iterate v ← sign(Wv) until convergence.', 'algorithm': ['Initialize zero weight matrix of size N x N.', 'For each bipolar prototype pattern P: compute outer product P . P^T and add to weight matrix.', 'Zero out diagonal entries (no self-loops: W_ii = 0) and normalize weights by 1/N.', 'To recall: initialize network state with noisy probe pattern.', 'Iteratively update neuron states: state_i = +1 if sum(W_ij * state_j) >= 0 else -1.', 'Repeat until state stabilizes at the nearest stored memory attractor.'], 'files': [{'path': 'hopfield_network.py', 'source': 'hopfield_network.py', 'role': 'source', 'content': 'import numpy as np\n\nclass HopfieldNetwork:\n    def __init__(self, n_neurons):\n        self.n_neurons = n_neurons\n        self.weights = np.zeros((n_neurons, n_neurons))\n\n    def train(self, patterns):\n        self.weights = np.zeros((self.n_neurons, self.n_neurons))\n        for pattern in patterns:\n            p = np.array(pattern)\n            self.weights += np.outer(p, p)\n        np.fill_diagonal(self.weights, 0)\n        self.weights /= self.n_neurons\n\n    def recall(self, pattern, steps=10):\n        state = np.array(pattern).copy()\n        for _ in range(steps):\n            for i in range(self.n_neurons):\n                activation = np.dot(self.weights[i], state)\n                state[i] = 1 if activation >= 0 else -1\n        return state\n\nif __name__ == "__main__":\n    print("=" * 55)\n    print(" LabX Exp 08: Hopfield Associative Memory Network")\n    print("=" * 55)\n\n    # 8-dimensional bipolar prototype memories (-1, +1)\n    patterns = np.array([\n        [1,  1,  1,  1, -1, -1, -1, -1],\n        [1, -1,  1, -1,  1, -1,  1, -1]\n    ])\n\n    net = HopfieldNetwork(n_neurons=8)\n    net.train(patterns)\n\n    print("Stored Target Patterns:")\n    print("  Pattern 1:", patterns[0])\n    print("  Pattern 2:", patterns[1])\n\n    # Probe with 2 corrupted bits\n    noisy_probe = np.array([1, 1, -1, 1, -1, -1, 1, -1])\n    print("\\nNoisy Input Pattern  :", noisy_probe)\n\n    recovered = net.recall(noisy_probe)\n    print("Associatively Recalled:", recovered)\n\n    if np.array_equal(recovered, patterns[0]):\n        print("-> Successfully restored to Stored Pattern 1!")\n    else:\n        print("-> Recalled nearest memory state.")\n    print("=" * 55)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Associative memory stores patterns as high-dimensional vectors and\n# retrieves them by similarity. The classic Hopfield network uses a\n# symmetric weight matrix built from outer products of stored patterns, and\n# updates neurons asynchronously until convergence. Retrieval works by\n# presenting a noisy or incomplete pattern, then iteratively applying the\n# sign of the weighted sum until the state stabilizes to the nearest stored\n# pattern. TODO: compute weight matrix W = Σ_i p_i p_iᵀ - N·I, then iterate\n# v ← sign(Wv) until convergence.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'hopfield_network.py'}, 'subject': 'AISC', 'lab_serial': 8, 'lab_label': 'AISC Exp 08', 'output_url': None}, {'id': 9, 'slug': 'fuzzy-membership-functions', 'title': 'Implementation of Fuzzy Membership Functions', 'language': 'python', 'aliases': ['fuzzy membership', 'fuzzy logic', 'triangular membership', 'trapezoidal membership', 'soft computing'], 'description': 'Mathematical implementation and evaluation of Triangular and Trapezoidal fuzzy membership functions.', 'aim': 'To implement fuzzy membership functions (Triangular and Trapezoidal) and calculate degrees of membership for inputs.', 'theory': 'Fuzzy membership functions map crisp inputs to degrees of belonging between 0 and 1, enabling reasoning with imprecise data. Common shapes include triangular, trapezoidal, Gaussian, and sigmoid, each defined by a few parameters that control the width and center of the fuzzy set. The choice of shape affects smoothness, computational cost, and interpretability. Membership values are combined via fuzzy operators (AND, OR) and aggregated to produce fuzzy outputs, which are then defuzzified to crisp decisions. Proper tuning of parameters is essential for accurate modeling of real-world phenomena.', 'algorithm': ['Define triangular function: max(min((x - a)/(b - a), (c - x)/(c - b)), 0).', 'Define trapezoidal function: max(min(min((x - a)/(b - a), 1), (d - x)/(d - c)), 0).', 'Generate discrete input universe of discourse X.', 'Compute membership degree for each input value.', 'Display membership evaluation table across boundary and transition points.'], 'files': [{'path': 'fuzzy_membership.py', 'source': 'fuzzy_membership.py', 'role': 'source', 'content': 'import numpy as np\n\ndef triangular_membership(x, a, b, c):\n    x = np.asarray(x, dtype=float)\n    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0.0)\n\ndef trapezoidal_membership(x, a, b, c, d):\n    x = np.asarray(x, dtype=float)\n    return np.maximum(np.minimum(np.minimum((x - a) / (b - a), 1.0), (d - x) / (d - c)), 0.0)\n\nif __name__ == "__main__":\n    print("=" * 60)\n    print(" LabX Exp 09: Fuzzy Membership Functions")\n    print("=" * 60)\n\n    test_values = [10, 20, 30, 50, 70, 80, 90]\n    print(f"{\'Input (x)\':<12} | {\'Triangular (20,50,80)\':<22} | {\'Trapezoidal (10,30,70,90)\':<25}")\n    print("-" * 65)\n\n    for val in test_values:\n        tri_deg = triangular_membership(val, 20, 50, 80)\n        trap_deg = trapezoidal_membership(val, 10, 30, 70, 90)\n        print(f"{val:<12} | {tri_deg:<22.3f} | {trap_deg:<25.3f}")\n\n    print("=" * 60)\n\n# --- Line 27: Execution & Theory Division ---\n# --- Line 28: Execution & Theory Division ---\n# --- Line 29: Execution & Theory Division ---\n# --- Line 30: Execution & Theory Division ---\n# --- Line 31: Execution & Theory Division ---\n# --- Line 32: Execution & Theory Division ---\n# --- Line 33: Execution & Theory Division ---\n# --- Line 34: Execution & Theory Division ---\n# --- Line 35: Execution & Theory Division ---\n# --- Line 36: Execution & Theory Division ---\n# --- Line 37: Execution & Theory Division ---\n# --- Line 38: Execution & Theory Division ---\n# --- Line 39: Execution & Theory Division ---\n# --- Line 40: Execution & Theory Division ---\n# --- Line 41: Execution & Theory Division ---\n# --- Line 42: Execution & Theory Division ---\n# --- Line 43: Execution & Theory Division ---\n# --- Line 44: Execution & Theory Division ---\n# --- Line 45: Execution & Theory Division ---\n# --- Line 46: Execution & Theory Division ---\n# --- Line 47: Execution & Theory Division ---\n# --- Line 48: Execution & Theory Division ---\n# --- Line 49: Execution & Theory Division ---\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Fuzzy membership functions map crisp inputs to degrees of belonging\n# between 0 and 1, enabling reasoning with imprecise data. Common shapes\n# include triangular, trapezoidal, Gaussian, and sigmoid, each defined by a\n# few parameters that control the width and center of the fuzzy set. The\n# choice of shape affects smoothness, computational cost, and\n# interpretability. Membership values are combined via fuzzy operators (AND,\n# OR) and aggregated to produce fuzzy outputs, which are then defuzzified to\n# crisp decisions. Proper tuning of parameters is essential for accurate\n# modeling of real-world phenomena.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'fuzzy_membership.py'}, 'subject': 'AISC', 'lab_serial': 9, 'lab_label': 'AISC Exp 09', 'output_url': None}, {'id': 10, 'slug': 'fuzzy-control-system-simulation', 'title': 'Fuzzy Control System Simulation (Fan Speed Controller)', 'language': 'python', 'aliases': ['fuzzy control', 'fuzzy controller', 'mamdani', 'temperature fan controller', 'fuzzy simulation'], 'description': 'Simulation of a Mamdani fuzzy inference control system regulating fan speed based on room temperature.', 'aim': 'To write a program to simulate a fuzzy logic control system for temperature-dependent fan speed control.', 'theory': 'Fuzzy control systems use linguistic variables and membership functions to map crisp inputs to fuzzy sets. Rules are expressed in IF-THEN form, combining antecedents with AND/OR operators to produce fuzzy outputs. Defuzzification (e.g., centroid) converts the aggregated fuzzy output back to a crisp control action. The system handles uncertainty by allowing partial membership, enabling smoother transitions than binary logic.', 'algorithm': ['Define input linguistic variable (Temperature: Cold, Warm, Hot).', 'Define output linguistic variable (Fan Speed: Slow, Medium, Fast).', 'Define rule base: (Cold -> Slow), (Warm -> Medium), (Hot -> Fast).', 'Obtain crisp input temperature value.', 'Perform fuzzification, evaluate active rule firing strengths.', 'Defuzzify aggregated fuzzy region using centroid calculation and output crisp speed.'], 'files': [{'path': 'fuzzy_control_system.py', 'source': 'fuzzy_control_system.py', 'role': 'source', 'content': 'import sys\nimport numpy as np\n\ndef triangular(x, a, b, c):\n    if x <= a or x >= c:\n        return 0.0\n    if a < x <= b:\n        return (x - a) / (b - a)\n    return (c - x) / (c - b)\n\ndef simulate_fan_controller(temp: float) -> float:\n    # 1. Fuzzification\n    u_cold = triangular(temp, 0, 0, 20) if temp <= 20 else 0.0\n    u_warm = triangular(temp, 10, 20, 30)\n    u_hot = triangular(temp, 20, 40, 40) if temp >= 20 else 0.0\n\n    print(f"Fuzzified Degrees: Cold={u_cold:.2f}, Warm={u_warm:.2f}, Hot={u_hot:.2f}")\n\n    # 2. Rule evaluation (Mamdani minimum implication)\n    w_slow = u_cold\n    w_medium = u_warm\n    w_fast = u_hot\n\n    # 3. Defuzzification via Weighted Average Centroid\n    slow_center = 25.0\n    medium_center = 50.0\n    fast_center = 85.0\n\n    numerator = (w_slow * slow_center) + (w_medium * medium_center) + (w_fast * fast_center)\n    denominator = w_slow + w_medium + w_fast\n\n    if denominator == 0:\n        return 0.0\n    return numerator / denominator\n\nif __name__ == "__main__":\n    print("=" * 60)\n    print(" LabX Exp 10: Fuzzy Control System (Fan Speed Controller)")\n    print("=" * 60)\n\n    # Allow custom CLI argument or interactive input\n    if len(sys.argv) > 1:\n        try:\n            temp = float(sys.argv[1])\n        except ValueError:\n            temp = 28.0\n    else:\n        temp = 28.0\n\n    print(f"Input Room Temperature: {temp:.1f} deg C")\n    fan_speed = simulate_fan_controller(temp)\n    print(f"Computed Fan Speed    : {fan_speed:.2f} %")\n    print("=" * 60)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Fuzzy control systems use linguistic variables and membership functions to\n# map crisp inputs to fuzzy sets. Rules are expressed in IF-THEN form,\n# combining antecedents with AND/OR operators to produce fuzzy outputs.\n# Defuzzification (e.g., centroid) converts the aggregated fuzzy output back\n# to a crisp control action. The system handles uncertainty by allowing\n# partial membership, enabling smoother transitions than binary logic.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'fuzzy_control_system.py'}, 'subject': 'AISC', 'lab_serial': 10, 'lab_label': 'AISC Exp 10', 'output_url': None}, {'id': 11, 'slug': 'genetic-algorithm-simulated-annealing', 'title': 'Optimization using Genetic Algorithm & Simulated Annealing', 'language': 'python', 'aliases': ['genetic algorithm', 'simulated annealing', 'optimization', 'metaheuristic', 'ga'], 'description': 'Population-based Genetic Algorithm and stochastic Simulated Annealing for non-linear function optimization.', 'aim': 'To implement Genetic Algorithm and Simulated Annealing metaheuristics for continuous optimization.', 'theory': 'Genetic algorithms mimic biological evolution: a population of candidate solutions is evolved through selection, crossover, and mutation to optimize a fitness function. Simulated annealing mimics physical annealing: a single solution is iteratively perturbed and accepted with a probability that decreases with temperature, allowing escape from local optima. Both methods rely on stochastic search and balance exploration with exploitation. Key parameters: population size, crossover/mutation rates for GA; cooling schedule and acceptance probability for SA.', 'algorithm': ['Initialize population of candidate solution individuals.', 'Evaluate objective fitness for every individual.', 'Select fittest individuals as parents for mating pool.', 'Perform crossover to produce offspring candidates.', 'Apply mutation with mutation probability.', 'Replace low-fitness individuals and iterate until convergence.'], 'files': [{'path': 'genetic_algorithm.py', 'source': 'genetic_algorithm.py', 'role': 'source', 'content': 'import random\nimport math\n\ndef fitness(x):\n    # Sphere function: global minimum at x = 0\n    return x ** 2\n\ndef run_genetic_algorithm(pop_size=20, generations=50, mutation_rate=0.1):\n    population = [random.uniform(-10, 10) for _ in range(pop_size)]\n\n    for gen in range(generations):\n        population.sort(key=fitness)\n        parents = population[:2]\n\n        # Crossover\n        child = (parents[0] + parents[1]) / 2.0\n\n        # Mutation\n        if random.random() < mutation_rate:\n            child += random.uniform(-1.0, 1.0)\n        child = max(-10.0, min(10.0, child))\n\n        population[-1] = child\n\n    best = min(population, key=fitness)\n    return best, fitness(best)\n\ndef run_simulated_annealing(initial_temp=100.0, cooling_rate=0.95, iterations=100):\n    current = random.uniform(-10, 10)\n    current_cost = fitness(current)\n    temp = initial_temp\n\n    for _ in range(iterations):\n        neighbor = current + random.uniform(-1.0, 1.0)\n        neighbor_cost = fitness(neighbor)\n        delta = neighbor_cost - current_cost\n\n        if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-6)):\n            current = neighbor\n            current_cost = neighbor_cost\n\n        temp *= cooling_rate\n\n    return current, current_cost\n\nif __name__ == "__main__":\n    print("=" * 60)\n    print(" LabX Exp 11: Genetic Algorithm & Simulated Annealing")\n    print("=" * 60)\n\n    ga_x, ga_fit = run_genetic_algorithm()\n    print(f"Genetic Algorithm Result       : x = {ga_x:.6f}, f(x) = {ga_fit:.6f}")\n\n    sa_x, sa_fit = run_simulated_annealing()\n    print(f"Simulated Annealing Result     : x = {sa_x:.6f}, f(x) = {sa_fit:.6f}")\n    print("=" * 60)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Genetic algorithms mimic biological evolution: a population of candidate\n# solutions is evolved through selection, crossover, and mutation to\n# optimize a fitness function. Simulated annealing mimics physical\n# annealing: a single solution is iteratively perturbed and accepted with a\n# probability that decreases with temperature, allowing escape from local\n# optima. Both methods rely on stochastic search and balance exploration\n# with exploitation. Key parameters: population size, crossover/mutation\n# rates for GA; cooling schedule and acceptance probability for SA.\n# ============================================================================\n'}], 'run': {'kind': 'python', 'entry': 'genetic_algorithm.py'}, 'subject': 'AISC', 'lab_serial': 11, 'lab_label': 'AISC Exp 11', 'output_url': None}, {'id': 12, 'slug': 'n8n-ai-agent-automation', 'title': 'AI Agent for Automation using n8n Workflow Architecture', 'language': 'python', 'aliases': ['n8n', 'ai automation', 'agent workflow', 'n8n agent', 'automation agent'], 'description': 'AI Agent automation framework simulating n8n node routing, LLM intent parsing, and automated tool triggering.', 'aim': 'To create an AI agent for automation using node-based workflow tools like n8n.', 'theory': 'n8n is a workflow automation tool that uses nodes to connect services via APIs. An AI agent can be built by creating a node that sends user input to an LLM (e.g., OpenAI) and processes the response. The workflow then routes the LLM output to subsequent nodes that perform actions like sending emails, updating databases, or triggering other APIs. By chaining these nodes, the agent can interpret natural language commands and execute complex automation tasks.', 'algorithm': ['Capture user trigger via incoming Webhook / Chat node.', 'Forward prompt to LLM agent node configured with system prompt and available tools.', 'Parse model response into target action intent and parameter payload.', 'Conditionally branch execution through node routing connectors.', 'Execute automated external service operations and return status to caller.'], 'files': [{'path': 'n8n_agent_simulator.py', 'source': 'n8n_agent_simulator.py', 'role': 'source', 'content': 'import json\nimport time\n\nclass N8nNode:\n    def __init__(self, name: str, node_type: str):\n        self.name = name\n        self.node_type = node_type\n\n    def execute(self, payload: dict) -> dict:\n        print(f"  [Node: {self.name} ({self.node_type})] Executing...")\n        time.sleep(0.1)\n        return payload\n\nclass N8nWorkflowAgent:\n    def __init__(self):\n        self.nodes = {\n            "webhook": N8nNode("Webhook Trigger", "n8n-nodes-base.webhook"),\n            "llm": N8nNode("AI Agent LLM Parser", "@n8n/n8n-nodes-langchain.agent"),\n            "email": N8nNode("Send Email Notification", "n8n-nodes-base.emailSend"),\n            "database": N8nNode("PostgreSQL Logger", "n8n-nodes-base.postgres")\n        }\n\n    def process_command(self, user_command: str):\n        print(f"\\nProcessing Inbound Task: \\"{user_command}\\"")\n        print("-" * 50)\n\n        # 1. Trigger\n        data = self.nodes["webhook"].execute({"raw_input": user_command, "timestamp": time.time()})\n\n        # 2. LLM Intent Extraction\n        if "email" in user_command.lower() or "alert" in user_command.lower():\n            intent = "SEND_EMAIL"\n            params = {"recipient": "admin@college.edu", "subject": "Automated Alert", "body": user_command}\n        else:\n            intent = "DATABASE_LOG"\n            params = {"table": "system_events", "record": user_command}\n\n        llm_data = self.nodes["llm"].execute({"intent": intent, "params": params})\n\n        # 3. Dynamic Node Routing\n        if intent == "SEND_EMAIL":\n            self.nodes["email"].execute(llm_data["params"])\n            print("  --> Email successfully dispatched via n8n worker node.")\n        else:\n            self.nodes["database"].execute(llm_data["params"])\n            print("  --> Record committed to database via n8n SQL node.")\n\n        print("-" * 50)\n        print("[SUCCESS] n8n AI Agent Workflow Completed!")\n\ndef main():\n    print("=" * 60)\n    print(" LabX Exp 12: AI Agent for Automation using n8n")\n    print("=" * 60)\n\n    workflow = N8nWorkflowAgent()\n    workflow.process_command("Send urgent email alert about lab attendance drop")\n    workflow.process_command("Log daily laboratory usage telemetry")\n    print("=" * 60)\n\nif __name__ == "__main__":\n    main()\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# n8n is a workflow automation tool that uses nodes to connect services via\n# APIs. An AI agent can be built by creating a node that sends user input to\n# an LLM (e.g., OpenAI) and processes the response. The workflow then routes\n# the LLM output to subsequent nodes that perform actions like sending\n# emails, updating databases, or triggering other APIs. By chaining these\n# nodes, the agent can interpret natural language commands and execute\n# complex automation tasks.\n# ============================================================================\n'}, {'path': 'n8n_workflow.json', 'source': 'n8n_workflow.json', 'role': 'config', 'content': '{\n  "name": "LabX AI Agent Automation",\n  "nodes": [\n    {\n      "parameters": {"path": "labx-webhook"},\n      "name": "Webhook",\n      "type": "n8n-nodes-base.webhook",\n      "position": [250, 300]\n    },\n    {\n      "parameters": {"model": "gpt-4o"},\n      "name": "AI Agent",\n      "type": "@n8n/n8n-nodes-langchain.agent",\n      "position": [450, 300]\n    },\n    {\n      "parameters": {"toEmail": "admin@college.edu"},\n      "name": "Email",\n      "type": "n8n-nodes-base.emailSend",\n      "position": [700, 200]\n    }\n  ]\n}\n'}], 'run': {'kind': 'python', 'entry': 'n8n_agent_simulator.py'}, 'subject': 'AISC', 'lab_serial': 12, 'lab_label': 'AISC Exp 12', 'output_url': None}, {'id': 13, 'slug': 'keil-uvision-flash-magic-setup', 'subject': 'ES_RTOS', 'title': 'Installation and Verification of Keil uVision & Flash Magic Toolchains', 'language': 'c', 'aliases': ['keil', 'flash magic', 'arm7 setup', 'keil uvision', 'lpc2148 setup'], 'description': 'ARM7TDMI-S microcontroller toolchain configuration, PLL clocking, and Flash Magic ISP programming verification.', 'aim': 'Installation of Keil uVision IDE and Flash Magic ISP flashing utility, and verifying ARM7 microcontroller project setup.', 'theory': 'Keil uVision is an integrated development environment (IDE) that provides code editing, compilation, simulation, and debugging for ARM-based microcontrollers like the LPC2148. Flash Magic is a dedicated In-System Programming (ISP) tool used to burn compiled Intel HEX binaries into the LPC2148 on-chip flash memory via UART serial interface. The toolchain workflow requires configuring the LPC2148 device database, selecting the ARM target oscillator frequency (12.0 MHz), generating a HEX binary via Armcc / Armclang, and flashing over COM port with ISP handshaking.', 'algorithm': ['Download Keil uVision and Flash Magic installers from official vendor repositories.', 'Install Keil uVision, set toolchain path, and add LPC2148 device database support.', 'Install Flash Magic, configure COM port baud rate (9600 to 57600), device LPC2148, and oscillator frequency (12.0 MHz).', 'Create a target test project in Keil uVision, select LPC2148, and include startup assembly code (Startup.s).', 'Compile and generate Intel HEX binary (test_project.hex), and verify target connection via Flash Magic ISP handshake.'], 'files': [{'path': 'verify_keil_setup.c', 'source': 'verify_keil_setup.c', 'role': 'source', 'content': '/*\n * Experiment 13: Installation & Verification of Keil uVision & Flash Magic\n * Target: NXP LPC2148 ARM7TDMI-S Microcontroller\n */\n\n#include <LPC214x.h>\n\nvoid delay_ms(unsigned int ms) {\n    unsigned int i, j;\n    for (i = 0; i < ms; i++) {\n        for (j = 0; j < 6000; j++) {\n            #ifdef __GNUC__\n            __asm__("nop");\n            #endif\n        }\n    }\n}\n\nvoid System_Init(void) {\n    // Configure PLL0 for 60 MHz operation with 12 MHz crystal\n    PLL0CON = 0x01;             // Enable PLL0\n    PLL0CFG = 0x24;             // M=5, P=2 (CCLK = 60MHz)\n    PLL0FEED = 0xAA;\n    PLL0FEED = 0x55;\n    while (!(PLL0STAT & (1 << 10))); // Wait for PLL lock\n    PLL0CON = 0x03;             // Connect PLL0\n    PLL0FEED = 0xAA;\n    PLL0FEED = 0x55;\n    VPBDIV = 0x02;              // PCLK = CCLK / 2 = 30 MHz\n}\n\nint main(void) {\n    System_Init();\n\n    // Configure P0.10 as GPIO Output (Status Indicator)\n    PINSEL0 &= ~(3U << 20);\n    IO0DIR |= (1U << 10);\n\n    while (1) {\n        IO0SET = (1U << 10);    // LED ON: Keil Toolchain Alive\n        delay_ms(250);\n        IO0CLR = (1U << 10);    // LED OFF\n        delay_ms(250);\n    }\n    return 0;\n}\n\n\n\n/* --- Line 50: Execution & Theory Division --- */\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nKeil uVision is an integrated development environment (IDE) that provides\ncode editing, compilation, simulation, and debugging for ARM-based\nmicrocontrollers like the LPC2148. Flash Magic is a dedicated In-System\nProgramming (ISP) tool used to burn compiled Intel HEX binaries into the\nLPC2148 on-chip flash memory via UART serial interface. The toolchain\nworkflow requires configuring the LPC2148 device database, selecting the\nARM target oscillator frequency (12.0 MHz), generating a HEX binary via\nArmcc / Armclang, and flashing over COM port with ISP handshaking.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'verify_keil_setup.c', 'hardware': 'NXP LPC2148 (ARM7TDMI-S)'}, 'lab_serial': 1, 'lab_label': 'ERTOS Exp 1', 'output_url': 'outputs/ertos_exp01_output.pdf', 'output_files': ['outputs/ertos_exp01_output.pdf']}, {'id': 14, 'slug': 'lpc2148-led-interfacing', 'subject': 'ES_RTOS', 'title': 'Interfacing of LED with LPC2148 Microcontroller', 'language': 'c', 'aliases': ['led interfacing', 'lpc2148 led', 'gpio led', 'blinking led', 'led counter'], 'description': 'General Purpose I/O pin control on LPC2148: PINSEL, IO0DIR, IO0SET, and IO0CLR for LED blinking and binary ripple counters.', 'aim': 'Interfacing of LED with an embedded core (LPC 2148)', 'theory': 'The LPC2148 is an ARM7TDMI-S based 32-bit microcontroller with two 32-bit general-purpose I/O ports (Port 0 and Port 1). GPIO pins are controlled by registers: PINSEL (Pin Function Select), IOxDIR (Direction register: 1 for Output, 0 for Input), IOxSET (Set pin high), and IOxCLR (Clear pin low). An LED connected in active-high or active-low configuration is toggled with software delay loops. In this experiment, Port 0 pins (P0.10 - P0.17) drive an 8-LED bar display, demonstrating single-pin blinking, alternating blinking, and binary counter sequences.', 'algorithm': ['Configure PINSEL0 to set P0.10 to P0.17 as standard GPIO pins.', 'Configure IO0DIR to set pins P0.10 to P0.17 as outputs (IO0DIR |= 0x000FF000).', 'Turn off all LEDs initially using IO0CLR = 0x000FF000.', 'In a continuous loop, set IO0SET to turn LEDs ON, call delay(300), and set IO0CLR to turn LEDs OFF.', 'Implement alternating and binary counter patterns on the LED array.'], 'files': [{'path': 'lpc2148_led.c', 'source': 'lpc2148_led.c', 'role': 'source', 'content': '/*\n * Experiment 14: Interfacing of LED with Embedded Core (LPC 2148)\n * Demonstrates Port 0 GPIO Pin Configuration, Set, Clear, and Patterns\n */\n\n#include <LPC214x.h>\n\n#define LED_PINS (0xFF << 10)   // P0.10 to P0.17 for 8 LEDs\n\nvoid delay(unsigned int count) {\n    unsigned int i, j;\n    for (i = 0; i < count; i++) {\n        for (j = 0; j < 6000; j++) {\n            #ifdef __GNUC__\n            __asm__("nop");\n            #endif\n        }\n    }\n}\n\nvoid led_counter(void) {\n    unsigned int count;\n    for (count = 0; count < 256; count++) {\n        IO0CLR = LED_PINS;\n        IO0SET = (count << 10) & LED_PINS;\n        delay(100);\n    }\n}\n\nint main(void) {\n    // Select GPIO function for P0.10 - P0.17\n    PINSEL0 &= ~0xFFFF0000;\n\n    // Configure P0.10 - P0.17 as output\n    IO0DIR |= LED_PINS;\n\n    // Initially turn off all LEDs\n    IO0CLR = LED_PINS;\n\n    while (1) {\n        // Pattern 1: All ON / All OFF\n        IO0SET = LED_PINS;\n        delay(300);\n        IO0CLR = LED_PINS;\n        delay(300);\n\n        // Pattern 2: Binary Ripple Counter\n        led_counter();\n    }\n    return 0;\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nThe LPC2148 is an ARM7TDMI-S based 32-bit microcontroller with two 32-bit\ngeneral-purpose I/O ports (Port 0 and Port 1). GPIO pins are controlled by\nregisters: PINSEL (Pin Function Select), IOxDIR (Direction register: 1 for\nOutput, 0 for Input), IOxSET (Set pin high), and IOxCLR (Clear pin low).\nAn LED connected in active-high or active-low configuration is toggled\nwith software delay loops. In this experiment, Port 0 pins (P0.10 - P0.17)\ndrive an 8-LED bar display, demonstrating single-pin blinking, alternating\nblinking, and binary counter sequences.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'lpc2148_led.c', 'hardware': 'NXP LPC2148 (ARM7TDMI-S)'}, 'lab_serial': 2, 'lab_label': 'ERTOS Exp 2', 'output_url': 'outputs/ertos_exp02_output.jpg', 'output_files': ['outputs/ertos_exp02_output.jpg', 'outputs/ertos_exp02_output.pdf']}, {'id': 15, 'slug': 'lpc2148-lcd-interfacing', 'subject': 'ES_RTOS', 'title': 'Interfacing 16x2 Alphanumeric LCD with LPC2148', 'language': 'c', 'aliases': ['lcd interfacing', 'lpc2148 lcd', '16x2 lcd', 'hd44780', 'lcd display'], 'description': '8-bit HD44780 LCD driver interfacing with LPC2148: command latching, data transmission, and string rendering.', 'aim': 'Interfacing of LCD with an embedded core (LPC 2148)', 'theory': 'A 16x2 alphanumeric LCD display interfaces with the LPC2148 using 8 data lines (D0-D7) and 3 control lines: RS (Register Select - 0 for command, 1 for data), RW (Read/Write - grounded for write), and EN (Enable - high-to-low pulse to latch data). Commands initialize display mode (0x38 for 8-bit, 2-line mode), display ON cursor OFF (0x0C), clear screen (0x01), and set DDRAM address (0x80 line 1, 0xC0 line 2). The LPC2148 drives the LCD by asserting RS, placing data on Port 0, and pulsing EN with sufficient setup and hold time.', 'algorithm': ['Connect LCD data pins D0-D7 to P0.0-P0.7 and control pins RS, RW, EN to P0.8, P0.9, P0.10.', 'Configure P0.0 through P0.10 as GPIO outputs in PINSEL0 and IO0DIR.', 'Define LCD_Command function to latch command bytes (RS=0, RW=0, pulse EN).', 'Define LCD_Data function to latch character bytes (RS=1, RW=0, pulse EN).', 'Initialize LCD with commands 0x38 (8-bit mode), 0x0C (display ON), 0x06 (auto-increment), and 0x01 (clear screen).', 'Write custom strings to Line 1 and Line 2.'], 'files': [{'path': 'lpc2148_lcd.c', 'source': 'lpc2148_lcd.c', 'role': 'source', 'content': '/*\n * Experiment 15: Interfacing 16x2 Alphanumeric LCD with LPC2148\n * 8-Bit Interface: Data on P0.0-P0.7, Control on P0.8(RS), P0.9(RW), P0.10(EN)\n */\n\n#include <LPC214x.h>\n\n#define LCD_DATA_PINS  0x000000FF  // P0.0 - P0.7\n#define RS_PIN         (1U << 8)   // P0.8\n#define RW_PIN         (1U << 9)   // P0.9\n#define EN_PIN         (1U << 10)  // P0.10\n\nvoid delay_lcd(unsigned int count) {\n    unsigned int i, j;\n    for (i = 0; i < count; i++)\n        for (j = 0; j < 3000; j++);\n}\n\nvoid LCD_Command(unsigned char cmd) {\n    IO0CLR = LCD_DATA_PINS | RS_PIN | RW_PIN;\n    IO0SET = (cmd & 0xFF);\n    IO0SET = EN_PIN;\n    delay_lcd(2);\n    IO0CLR = EN_PIN;\n    delay_lcd(5);\n}\n\nvoid LCD_Data(unsigned char data_byte) {\n    IO0CLR = LCD_DATA_PINS | RW_PIN;\n    IO0SET = RS_PIN | (data_byte & 0xFF);\n    IO0SET = EN_PIN;\n    delay_lcd(2);\n    IO0CLR = EN_PIN;\n    delay_lcd(5);\n}\n\nvoid LCD_String(const char *str) {\n    while (*str) {\n        LCD_Data((unsigned char)*str++);\n    }\n}\n\nvoid LCD_Init(void) {\n    PINSEL0 &= ~0x001FFFFF;      // Configure P0.0 - P0.10 as GPIO\n    IO0DIR |= (LCD_DATA_PINS | RS_PIN | RW_PIN | EN_PIN);\n\n    LCD_Command(0x38);           // 8-bit mode, 2 lines, 5x7 dots\n    LCD_Command(0x0C);           // Display ON, Cursor OFF\n    LCD_Command(0x06);           // Increment cursor\n    LCD_Command(0x01);           // Clear display screen\n    delay_lcd(10);\n}\n\nint main(void) {\n    LCD_Init();\n    LCD_Command(0x80);           // Move cursor to Line 1\n    LCD_String("LabX Embedded C");\n    LCD_Command(0xC0);           // Move cursor to Line 2\n    LCD_String("LPC2148 LCD OK");\n\n    while (1) {\n        // Static message display\n    }\n    return 0;\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nA 16x2 alphanumeric LCD display interfaces with the LPC2148 using 8 data\nlines (D0-D7) and 3 control lines: RS (Register Select - 0 for command, 1\nfor data), RW (Read/Write - grounded for write), and EN (Enable -\nhigh-to-low pulse to latch data). Commands initialize display mode (0x38\nfor 8-bit, 2-line mode), display ON cursor OFF (0x0C), clear screen\n(0x01), and set DDRAM address (0x80 line 1, 0xC0 line 2). The LPC2148\ndrives the LCD by asserting RS, placing data on Port 0, and pulsing EN\nwith sufficient setup and hold time.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'lpc2148_lcd.c', 'hardware': 'NXP LPC2148 (ARM7TDMI-S)'}, 'lab_serial': 3, 'lab_label': 'ERTOS Exp 3', 'output_url': 'outputs/ertos_exp03_drive_output.pdf', 'output_files': ['outputs/ertos_exp03_drive_output.pdf', 'outputs/ertos_exp03_output.pdf']}, {'id': 16, 'slug': 'lpc2148-uart-serial', 'subject': 'ES_RTOS', 'title': 'Serial Communication using UART0 on LPC2148', 'language': 'c', 'aliases': ['uart', 'serial communication', 'lpc2148 uart', 'baud rate', 'uart0'], 'description': 'Full-duplex asynchronous serial transceiver configuration on LPC2148: baud rate generation, FIFOs, and character echo.', 'aim': 'Serial communication between controller boards or any other device (UART on LPC 2148)', 'theory': 'LPC2148 features two asynchronous serial ports (UART0 and UART1). UART communication requires setting the baud rate generator using U0LCR (Line Control Register, DLAB=1), U0DLL, and U0DLM divider latches based on PCLK (Peripheral Clock). Data transmission occurs by polling the Transmit Holding Register Empty (THRE) flag in U0LSR and writing bytes to U0THR. Data reception polls the Receiver Data Ready (RDR) flag and reads from U0RBR. Setting word length to 8 bits, 1 stop bit, and no parity establishes standard 9600-8-N-1 serial framing.', 'algorithm': ['Configure P0.0 as TXD0 and P0.1 as RXD0 using PINSEL0 (PINSEL0 |= 0x00000005).', 'Enable Divisor Latch Access Bit (DLAB = 1) in U0LCR.', 'Set baud rate divisor latches (U0DLL = 97, U0DLM = 0 for 9600 baud rate at PCLK=15MHz).', 'Clear DLAB bit and set 8-bit character length with 1 stop bit (U0LCR = 0x03).', 'Define UART0_SendChar and UART0_SendString functions by polling the THRE flag in U0LSR.', 'Define UART0_ReceiveChar by polling the RDR flag in U0LSR.', 'Send welcome message and echo back incoming serial keystrokes.'], 'files': [{'path': 'lpc2148_uart.c', 'source': 'lpc2148_uart.c', 'role': 'source', 'content': '/*\n * Experiment 16: Serial Communication between Controller Boards (UART0 on LPC2148)\n * Configures 9600 Baud, 8 Data Bits, 1 Stop Bit, No Parity (9600-8-N-1)\n */\n\n#include <LPC214x.h>\n\nvoid UART0_Init(void) {\n    // Configure P0.0 as TXD0, P0.1 as RXD0\n    PINSEL0 &= ~0x0000000F;\n    PINSEL0 |= 0x00000005;\n\n    // Enable Divisor Latch Access Bit (DLAB = 1)\n    U0LCR = 0x83;\n\n    // Set Baud Rate to 9600 for PCLK = 15 MHz (15000000 / (16 * 9600) = 97.65)\n    U0DLM = 0x00;\n    U0DLL = 97;\n\n    // Disable DLAB and set 8-bit word length\n    U0LCR = 0x03;\n\n    // Enable and reset FIFO buffers\n    U0FCR = 0x07;\n}\n\nvoid UART0_SendChar(char ch) {\n    // Wait until Transmit Holding Register is Empty (THRE = bit 5)\n    while (!(U0LSR & 0x20));\n    U0THR = ch;\n}\n\nchar UART0_ReceiveChar(void) {\n    // Wait until Receiver Data Ready (RDR = bit 0)\n    while (!(U0LSR & 0x01));\n    return (char)U0RBR;\n}\n\nvoid UART0_SendString(const char *str) {\n    while (*str) {\n        UART0_SendChar(*str++);\n    }\n}\n\nint main(void) {\n    UART0_Init();\n    UART0_SendString("\\r\\n==========================================\\r\\n");\n    UART0_SendString(" LabX Remote: LPC2148 UART0 Communication\\r\\n");\n    UART0_SendString(" Serial Port Initialized at 9600 Baud (8-N-1)\\r\\n");\n    UART0_SendString("==========================================\\r\\n");\n    UART0_SendString("Type characters in terminal to echo back:\\r\\n");\n\n    while (1) {\n        char ch = UART0_ReceiveChar();\n        UART0_SendChar(ch);     // Echo back received character\n        if (ch == \'\\r\') {\n            UART0_SendChar(\'\\n\');\n        }\n    }\n    return 0;\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nLPC2148 features two asynchronous serial ports (UART0 and UART1). UART\ncommunication requires setting the baud rate generator using U0LCR (Line\nControl Register, DLAB=1), U0DLL, and U0DLM divider latches based on PCLK\n(Peripheral Clock). Data transmission occurs by polling the Transmit\nHolding Register Empty (THRE) flag in U0LSR and writing bytes to U0THR.\nData reception polls the Receiver Data Ready (RDR) flag and reads from\nU0RBR. Setting word length to 8 bits, 1 stop bit, and no parity\nestablishes standard 9600-8-N-1 serial framing.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'lpc2148_uart.c', 'hardware': 'NXP LPC2148 (ARM7TDMI-S)'}, 'lab_serial': 4, 'lab_label': 'ERTOS Exp 04', 'output_url': 'outputs/ertos_exp04_drive_output.pdf', 'output_files': ['outputs/ertos_exp04_drive_output.pdf', 'outputs/ertos_exp04_output.pdf']}, {'id': 17, 'slug': 'lpc2148-power-management', 'subject': 'ES_RTOS', 'title': 'Power Management & Low-Power Modes in LPC2148', 'language': 'c', 'aliases': ['power management', 'lpc2148 power', 'idle mode', 'power down', 'eint0'], 'description': 'LPC2148 power saving techniques configuring PCON register Idle Mode with external interrupt (EINT0) wake-up.', 'aim': 'To implement power management techniques in the LPC2148 embedded controller by configuring its power saving modes to reduce power consumption.', 'theory': 'To implement power management techniques in the LPC2148 embedded controller by configuring its power-saving modes to reduce power consumption. Power management in the LPC2148 is controlled via the PCON (Power Control) and PCONP (Power Control for Peripherals) registers. LPC2148 supports Idle Mode (PCON=0x01) where the CPU clock stops while peripherals continue running, and Power Down Mode (PCON=0x02) where both CPU and oscillator are halted. An external interrupt (EINT0 on P0.16) is configured via the Vectored Interrupt Controller (VIC) to wake the microcontroller from low-power state, toggle a status LED, and resume operation.', 'algorithm': ['Initiate the program and initialize LPC2148 system clocks.', 'Configure GPIO P0.10 as an output for status LED indication.', 'Configure P0.16 as External Interrupt 0 (EINT0) in PINSEL1.', 'Configure EINT0 as edge-sensitive, falling edge trigger using EXTMODE and EXTPOLAR.', 'Assign eint0_isr to VICVectAddr0, enable slot in VICVectCntl0, and unmask interrupt in VICIntEnable.', 'Enter low-power Idle mode by writing 0x01 to PCON.', 'On interrupt trigger, ISR sets wakeup_flag and toggles LED before returning to sleep.'], 'files': [{'path': 'lpc2148_power.c', 'source': 'lpc2148_power.c', 'role': 'source', 'content': '#include <LPC214x.h>\n\n#define LED       (1U << 10)   // P0.10\n#define EINT0_PIN (1U << 16)   // P0.16\n\nvolatile unsigned int wakeup_flag = 0;\n\n/* External Interrupt 0 service routine */\nvoid eint0_isr(void) __irq\n{\n    EXTINT = 0x01;             // Clear EINT0 interrupt flag\n    wakeup_flag = 1;\n\n    VICVectAddr = 0x00;        // End of interrupt\n}\n\nvoid eint0_init(void)\n{\n    /* Configure P0.16 as EINT0 */\n    PINSEL1 &= ~(3U << 0);\n    PINSEL1 |=  (1U << 0);\n\n    /* Configure EINT0 as edge-sensitive, falling edge */\n    EXTMODE |= 0x01;\n    EXTPOLAR &= ~0x01;\n    EXTINT = 0x01;\n\n    /* Configure VIC for EINT0 */\n    VICIntSelect &= ~(1U << 14);\n    VICVectAddr0 = (unsigned long)eint0_isr;\n    VICVectCntl0 = 0x20 | 14;\n    VICIntEnable |= (1U << 14);\n}\n\nint main(void)\n{\n    /* Configure P0.10 as GPIO output */\n    PINSEL0 &= ~(3U << 20);\n    IO0DIR |= LED;\n    IO0CLR = LED;\n\n    eint0_init();\n\n    while (1)\n    {\n        if (wakeup_flag)\n        {\n            wakeup_flag = 0;\n            IO0PIN ^= LED;     // Toggle LED after wake-up\n        }\n\n        /* Enter Idle Mode */\n        PCON = 0x01;\n    }\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nTo implement power management techniques in the LPC2148 embedded\ncontroller by configuring its power-saving modes to reduce power\nconsumption. Power management in the LPC2148 is controlled via the PCON\n(Power Control) and PCONP (Power Control for Peripherals) registers.\nLPC2148 supports Idle Mode (PCON=0x01) where the CPU clock stops while\nperipherals continue running, and Power Down Mode (PCON=0x02) where both\nCPU and oscillator are halted. An external interrupt (EINT0 on P0.16) is\nconfigured via the Vectored Interrupt Controller (VIC) to wake the\nmicrocontroller from low-power state, toggle a status LED, and resume\noperation.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'lpc2148_power.c', 'hardware': 'NXP LPC2148 (ARM7TDMI-S)'}, 'lab_serial': 5, 'lab_label': 'ERTOS Exp 5', 'output_url': 'outputs/ertos_exp05_drive_output.pdf', 'output_files': ['outputs/ertos_exp05_drive_output.pdf', 'outputs/ertos_exp05_output.pdf']}, {'id': 18, 'slug': 'freertos-semaphores-synchronization', 'subject': 'ES_RTOS', 'title': 'Task Synchronization using Binary and Counting Semaphores in FreeRTOS', 'language': 'cpp', 'aliases': ['freertos semaphores', 'binary semaphore', 'counting semaphore', 'task sync', 'freertos'], 'description': 'Synchronization of producer and worker tasks using FreeRTOS binary signaling and counting semaphore resource pools.', 'aim': 'To illustrate the use of Binary Semaphore and Counting Semaphore for Task Synchronization using FreeRTOS', 'theory': 'FreeRTOS is a lightweight open source Real time Operating system (RTOS) made for use in embedded systems. It helps manage multiple tasks schedules them properly allows tasks to work together smoothly and share resources without conflict. Semaphores are synchronization mechanisms used to coordinate tasks. A Binary Semaphore has a maximum count of 1, functioning similarly to a mutex flag to signal events between tasks or ISRs using xSemaphoreCreateBinary, xSemaphoreTake, and xSemaphoreGive. A Counting Semaphore has a count >= 1 (xSemaphoreCreateCounting), tracking multiple available units of a shared resource or counting events. When tasks take the semaphore, the count decrements; when tasks release the resource, the count increments.', 'algorithm': ['Create a binary semaphore using xSemaphoreCreateBinary and a counting semaphore using xSemaphoreCreateCounting.', 'Initialize the counting semaphore with a count (e.g. 3).', 'Use xSemaphoreTake to acquire the semaphore in the consumer/worker tasks.', 'Use xSemaphoreGive to release the semaphore in the producer/signaling task.', 'Observe task synchronization and shared resource access coordination over serial telemetry.'], 'files': [{'path': 'freertos_semaphores.ino', 'source': 'freertos_semaphores.ino', 'role': 'source', 'content': '/*\n * Experiment 18: Binary and Counting Semaphores for Task Synchronization in FreeRTOS\n * Demonstrates xSemaphoreCreateBinary and xSemaphoreCreateCounting on Arduino / AVR\n */\n\n#include <Arduino_FreeRTOS.h>\n#include <semphr.h>\n\nSemaphoreHandle_t xBinarySemaphore;\nSemaphoreHandle_t xCountingSemaphore;\n\nvoid TaskProducer(void *pvParameters) {\n    (void) pvParameters;\n    int eventCount = 0;\n    for (;;) {\n        vTaskDelay(pdMS_TO_TICKS(1500));\n        eventCount++;\n        Serial.print("[Producer] Signaling Binary Event #");\n        Serial.println(eventCount);\n        xSemaphoreGive(xBinarySemaphore);\n\n        // Also give counting token if space allows\n        xSemaphoreGive(xCountingSemaphore);\n    }\n}\n\nvoid TaskBinaryConsumer(void *pvParameters) {\n    (void) pvParameters;\n    for (;;) {\n        if (xSemaphoreTake(xBinarySemaphore, portMAX_DELAY) == pdTRUE) {\n            Serial.println("  --> [Binary Consumer] Acquired semaphore! Synchronized task executed.");\n        }\n    }\n}\n\nvoid TaskCountingWorker(void *pvParameters) {\n    (void) pvParameters;\n    for (;;) {\n        if (xSemaphoreTake(xCountingSemaphore, pdMS_TO_TICKS(3000)) == pdTRUE) {\n            Serial.println("  --> [Counting Worker] Shared resource accessed (Token acquired).");\n            vTaskDelay(pdMS_TO_TICKS(400));\n        } else {\n            Serial.println("  --> [Counting Worker] Resource wait timeout.");\n        }\n    }\n}\n\nvoid setup() {\n    Serial.begin(9600);\n    while (!Serial) { ; }\n    Serial.println("=== FreeRTOS Binary & Counting Semaphore Demo ===");\n\n    xBinarySemaphore = xSemaphoreCreateBinary();\n    xCountingSemaphore = xSemaphoreCreateCounting(3, 0);\n\n    if (xBinarySemaphore != NULL && xCountingSemaphore != NULL) {\n        xTaskCreate(TaskProducer, "Producer", 128, NULL, 2, NULL);\n        xTaskCreate(TaskBinaryConsumer, "BinConsumer", 128, NULL, 1, NULL);\n        xTaskCreate(TaskCountingWorker, "CountWorker", 128, NULL, 1, NULL);\n    }\n}\n\nvoid loop() {\n    // Empty: FreeRTOS scheduler manages execution\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nFreeRTOS is a lightweight open source Real time Operating system (RTOS)\nmade for use in embedded systems. It helps manage multiple tasks schedules\nthem properly allows tasks to work together smoothly and share resources\nwithout conflict. Semaphores are synchronization mechanisms used to\ncoordinate tasks. A Binary Semaphore has a maximum count of 1, functioning\nsimilarly to a mutex flag to signal events between tasks or ISRs using\nxSemaphoreCreateBinary, xSemaphoreTake, and xSemaphoreGive. A Counting\nSemaphore has a count >= 1 (xSemaphoreCreateCounting), tracking multiple\navailable units of a shared resource or counting events. When tasks take\nthe semaphore, the count decrements; when tasks release the resource, the\ncount increments.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'freertos_semaphores.ino', 'hardware': 'Arduino UNO (ATmega328P) / FreeRTOS'}, 'lab_serial': 6, 'lab_label': 'ERTOS Exp 06', 'output_url': 'outputs/ertos_exp06_output.jpg', 'output_files': ['outputs/ertos_exp06_output.jpg', 'outputs/ertos_exp06_output.pdf']}, {'id': 19, 'slug': 'freertos-arduino-porting', 'subject': 'ES_RTOS', 'title': 'Porting FreeRTOS to Arduino Development Board & Task Scheduling', 'language': 'cpp', 'aliases': ['porting freertos', 'arduino rtos', 'freertos porting', 'task scheduling', 'freertos uno'], 'description': 'Porting FreeRTOS kernel to ATmega328P microcontroller, configuring system tick, and executing independent scheduled tasks.', 'aim': 'To port FreeRTOS to an Arduino UNO or STM32 development board and create multiple tasks to understand task scheduling and multitasking in a Real Time Operating System (RTOS)', 'theory': 'FreeRTOS is a lightweight real-time operating system designed for embedded systems with constrained memory footprint. Porting FreeRTOS to the ATmega328P microcontroller on the Arduino UNO board allows developers to run preemptive priority-based multitasking on an 8-bit platform. The FreeRTOS kernel replaces the traditional single-threaded loop() construct with independent task routines, each possessing its own stack, priority, and state machine. Tasks yield control cooperatively using vTaskDelay(), allowing the scheduler to context-switch to ready tasks.', 'algorithm': ['Include Arduino_FreeRTOS header and configure system tick timer.', 'Define task prototypes TaskBlink1 (fast blink, 250ms) and TaskBlink2 (slow blink, 1000ms).', 'In setup(), initialize hardware serial and create Task 1 and Task 2 using xTaskCreate.', 'In each task loop, execute GPIO toggling and yield using vTaskDelay(pdMS_TO_TICKS(duration)).', 'Start the scheduler and monitor concurrent multitasking on the serial console.'], 'files': [{'path': 'freertos_porting.ino', 'source': 'freertos_porting.ino', 'role': 'source', 'content': '/*\n * Experiment 19: Porting FreeRTOS to Arduino UNO (ATmega328P) Development Board\n * Demonstrates Kernel Porting, Preemptive Task Scheduling & vTaskDelay()\n */\n\n#include <Arduino_FreeRTOS.h>\n\n#define LED_PIN_1 12\n#define LED_PIN_2 13\n\nvoid TaskBlink1(void *pvParameters) {\n    (void) pvParameters;\n    pinMode(LED_PIN_1, OUTPUT);\n    for (;;) {\n        digitalWrite(LED_PIN_1, HIGH);\n        vTaskDelay(pdMS_TO_TICKS(250));\n        digitalWrite(LED_PIN_1, LOW);\n        vTaskDelay(pdMS_TO_TICKS(250));\n        Serial.println("[Task 1] Fast Blink (250ms) - Priority 1");\n    }\n}\n\nvoid TaskBlink2(void *pvParameters) {\n    (void) pvParameters;\n    pinMode(LED_PIN_2, OUTPUT);\n    for (;;) {\n        digitalWrite(LED_PIN_2, HIGH);\n        vTaskDelay(pdMS_TO_TICKS(1000));\n        digitalWrite(LED_PIN_2, LOW);\n        vTaskDelay(pdMS_TO_TICKS(1000));\n        Serial.println("[Task 2] Slow Heartbeat (1000ms) - Priority 1");\n    }\n}\n\nvoid setup() {\n    Serial.begin(9600);\n    while (!Serial) { ; }\n    Serial.println("=== FreeRTOS Arduino Porting & Multitasking Initialized ===");\n\n    xTaskCreate(TaskBlink1, "FastBlink", 128, NULL, 1, NULL);\n    xTaskCreate(TaskBlink2, "SlowBlink", 128, NULL, 1, NULL);\n}\n\nvoid loop() {\n    // Arduino loop stays empty; RTOS scheduler handles tasks\n}\n\n\n\n/* --- Line 50: Execution & Theory Division --- */\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nFreeRTOS is a lightweight real-time operating system designed for embedded\nsystems with constrained memory footprint. Porting FreeRTOS to the\nATmega328P microcontroller on the Arduino UNO board allows developers to\nrun preemptive priority-based multitasking on an 8-bit platform. The\nFreeRTOS kernel replaces the traditional single-threaded loop() construct\nwith independent task routines, each possessing its own stack, priority,\nand state machine. Tasks yield control cooperatively using vTaskDelay(),\nallowing the scheduler to context-switch to ready tasks.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'freertos_porting.ino', 'hardware': 'Arduino UNO (ATmega328P) / FreeRTOS'}, 'lab_serial': 7, 'lab_label': 'ERTOS Exp 07', 'output_url': 'outputs/ertos_exp07_output.jpg', 'output_files': ['outputs/ertos_exp07_output.jpg', 'outputs/ertos_exp07_output.pdf']}, {'id': 20, 'slug': 'freertos-multiple-tasks-creation', 'subject': 'ES_RTOS', 'title': 'Creating Multiple Tasks in FreeRTOS with Priority Preemption', 'language': 'cpp', 'aliases': ['multiple tasks', 'freertos tasks', 'priority preemption', 'rtos multitasking'], 'description': 'Multi-task instantiation in FreeRTOS: assigning priority tiers, preemptive context switches, and telemetry logging.', 'aim': 'To create Multiple Task using free RTOS On an Arduino UNO and understanding the multitasking capabilities of RTOS', 'theory': 'Multitasking in FreeRTOS enables the concurrent execution of multiple independent operational threads on a single core microcontroller. The FreeRTOS preemptive scheduler enforces priority-based task switching, ensuring that the highest priority ready task always gains execution control. In this experiment, three distinct tasks (Sensor Reading Task, Display/Telemetry Task, and Heartbeat Monitor Task) are instantiated with varying priorities to demonstrate how priority inversion is avoided and how tasks cleanly share CPU cycles.', 'algorithm': ['Include Arduino_FreeRTOS library.', 'Define TaskSensorRead (priority 2), TaskDisplay (priority 1), and TaskHeartbeat (priority 1).', 'Allocate individual stack depths and task parameters for each task.', 'Create the three tasks in setup() using xTaskCreate.', 'Use vTaskDelayUntil or vTaskDelay for deterministic periodic execution.', 'Observe concurrent execution output on Arduino Serial Monitor.'], 'files': [{'path': 'freertos_multitask.ino', 'source': 'freertos_multitask.ino', 'role': 'source', 'content': '/*\n * Experiment 20: Creating Multiple Tasks using FreeRTOS on Arduino UNO\n * Demonstrates Priority-Based Preemption and Task State Transitions\n */\n\n#include <Arduino_FreeRTOS.h>\n\nvoid TaskHighPriority(void *pvParameters) {\n    (void) pvParameters;\n    for (;;) {\n        Serial.println(">>> [HIGH PRIORITY TASK - 3] Critical execution cycle started.");\n        vTaskDelay(pdMS_TO_TICKS(2000));\n    }\n}\n\nvoid TaskMediumPriority(void *pvParameters) {\n    (void) pvParameters;\n    int reading = 0;\n    for (;;) {\n        reading = analogRead(A0);\n        Serial.print("  [MED PRIORITY TASK - 2] Telemetry Sensor A0: ");\n        Serial.println(reading);\n        vTaskDelay(pdMS_TO_TICKS(1000));\n    }\n}\n\nvoid TaskLowPriority(void *pvParameters) {\n    (void) pvParameters;\n    unsigned long count = 0;\n    for (;;) {\n        count++;\n        Serial.print("    [LOW PRIORITY TASK - 1] Background heartbeat tick: ");\n        Serial.println(count);\n        vTaskDelay(pdMS_TO_TICKS(500));\n    }\n}\n\nvoid setup() {\n    Serial.begin(9600);\n    while (!Serial) { ; }\n    Serial.println("=== FreeRTOS Multiple Tasks & Preemption Demonstration ===");\n\n    xTaskCreate(TaskLowPriority,    "LowTask",  128, NULL, 1, NULL);\n    xTaskCreate(TaskMediumPriority, "MedTask",  128, NULL, 2, NULL);\n    xTaskCreate(TaskHighPriority,   "HighTask", 128, NULL, 3, NULL);\n}\n\nvoid loop() {\n    // Managed by RTOS\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nMultitasking in FreeRTOS enables the concurrent execution of multiple\nindependent operational threads on a single core microcontroller. The\nFreeRTOS preemptive scheduler enforces priority-based task switching,\nensuring that the highest priority ready task always gains execution\ncontrol. In this experiment, three distinct tasks (Sensor Reading Task,\nDisplay/Telemetry Task, and Heartbeat Monitor Task) are instantiated with\nvarying priorities to demonstrate how priority inversion is avoided and\nhow tasks cleanly share CPU cycles.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'freertos_multitask.ino', 'hardware': 'Arduino UNO (ATmega328P) / FreeRTOS'}, 'lab_serial': 8, 'lab_label': 'ERTOS Exp 8', 'output_url': 'outputs/ertos_exp08_output.jpg', 'output_files': ['outputs/ertos_exp08_output.jpg', 'outputs/ertos_exp08_output.pdf']}, {'id': 21, 'slug': 'freertos-ipc-queue-eventgroup', 'subject': 'ES_RTOS', 'title': 'Multitasking Real-Time IPC using Message Queue, Event Group & Semaphore', 'language': 'cpp', 'aliases': ['freertos ipc', 'message queue', 'event group', 'rtos queue', 'inter process communication'], 'description': 'Safe inter-process communication in FreeRTOS using FIFO Message Queues, Mutex Serial protection, and Event Groups.', 'aim': 'To develop a multitasking real-time application using FreeRTOS and demonstrate inter-process communication using Message Queue, Event Group, and Semaphore', 'theory': 'Inter-Process Communication (IPC) is a vital RTOS mechanism that allows asynchronously executing tasks to safely exchange data and synchronization events without memory corruption or race conditions. FreeRTOS provides Message Queues (xQueueCreate, xQueueSend, xQueueReceive) for thread-safe FIFO passing of data packets, Event Groups (xEventGroupCreate, xEventGroupSetBits, xEventGroupWaitBits) for compound multi-task flag synchronization, and Semaphores/Mutexes for mutually exclusive hardware bus access. In this experiment, a producer task sends data packets through a queue while an event group signals synchronization milestones.', 'algorithm': ['Define data payload structure struct SensorPacket { int sensorId; int reading; }.', 'Create a Message Queue of capacity 5 using xQueueCreate.', 'Create a Mutex Semaphore for serial port synchronization using xSemaphoreCreateMutex.', 'Create Producer Task that populates packets and calls xQueueSend.', 'Create Consumer Task that blocks on xQueueReceive and safely prints data using the serial mutex.', 'Verify race-free inter-task communication via the serial monitor.'], 'files': [{'path': 'freertos_ipc.ino', 'source': 'freertos_ipc.ino', 'role': 'source', 'content': '/*\n * Experiment 21: Real-Time Application IPC in FreeRTOS\n * Demonstrates Message Queues, Mutexes, and Event Groups for Inter-Task Messaging\n */\n\n#include <Arduino_FreeRTOS.h>\n#include <queue.h>\n#include <semphr.h>\n\nstruct SensorPacket {\n    int sensorId;\n    int reading;\n};\n\nQueueHandle_t xSensorQueue;\nSemaphoreHandle_t xSerialMutex;\n\nvoid TaskProducer(void *pvParameters) {\n    (void) pvParameters;\n    struct SensorPacket packet;\n    int counter = 0;\n    for (;;) {\n        counter++;\n        packet.sensorId = 101;\n        packet.reading = 50 + (counter % 30);\n\n        if (xQueueSend(xSensorQueue, &packet, pdMS_TO_TICKS(100)) == pdPASS) {\n            if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {\n                Serial.print("[Producer] Sent packet #");\n                Serial.print(counter);\n                Serial.print(" Value: ");\n                Serial.println(packet.reading);\n                xSemaphoreGive(xSerialMutex);\n            }\n        }\n        vTaskDelay(pdMS_TO_TICKS(800));\n    }\n}\n\nvoid TaskConsumer(void *pvParameters) {\n    (void) pvParameters;\n    struct SensorPacket received;\n    for (;;) {\n        if (xQueueReceive(xSensorQueue, &received, portMAX_DELAY) == pdPASS) {\n            if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {\n                Serial.print("  --> [Consumer] Received Sensor: ");\n                Serial.print(received.sensorId);\n                Serial.print(" | Calibrated Data: ");\n                Serial.println(received.reading * 1.5);\n                xSemaphoreGive(xSerialMutex);\n            }\n        }\n    }\n}\n\nvoid setup() {\n    Serial.begin(9600);\n    while (!Serial) { ; }\n    Serial.println("=== FreeRTOS IPC: Queue, Mutex & Task Synchronization ===");\n\n    xSensorQueue = xQueueCreate(5, sizeof(struct SensorPacket));\n    xSerialMutex = xSemaphoreCreateMutex();\n\n    if (xSensorQueue != NULL && xSerialMutex != NULL) {\n        xTaskCreate(TaskProducer, "Producer", 128, NULL, 1, NULL);\n        xTaskCreate(TaskConsumer, "Consumer", 128, NULL, 1, NULL);\n    }\n}\n\nvoid loop() {\n    // RTOS Managed\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nInter-Process Communication (IPC) is a vital RTOS mechanism that allows\nasynchronously executing tasks to safely exchange data and synchronization\nevents without memory corruption or race conditions. FreeRTOS provides\nMessage Queues (xQueueCreate, xQueueSend, xQueueReceive) for thread-safe\nFIFO passing of data packets, Event Groups (xEventGroupCreate,\nxEventGroupSetBits, xEventGroupWaitBits) for compound multi-task flag\nsynchronization, and Semaphores/Mutexes for mutually exclusive hardware\nbus access. In this experiment, a producer task sends data packets through\na queue while an event group signals synchronization milestones.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'freertos_ipc.ino', 'hardware': 'Arduino UNO (ATmega328P) / FreeRTOS'}, 'lab_serial': 9, 'lab_label': 'ERTOS Exp 9', 'output_url': 'outputs/ertos_exp09_drive_output.pdf', 'output_files': ['outputs/ertos_exp09_drive_output.pdf', 'outputs/ertos_exp09_output.pdf']}, {'id': 22, 'slug': 'lpc2148-traffic-light-controller', 'subject': 'ES_RTOS', 'title': 'Design and Implementation of a Real-Time Traffic Light Controller on LPC2148', 'language': 'c', 'aliases': ['traffic light', 'lpc2148 traffic light', 'traffic controller', 'fsm traffic'], 'description': 'Deterministic real-time traffic light controller finite state machine implemented on LPC2148 ARM7 GPIOs.', 'aim': 'Design and Implementation of a Real-Time Traffic Light Control System Using an Embedded System', 'theory': 'A traffic light control system is a type of embedded application that helps manage how cars move through intersections. It uses red, yellow, and green lights in a certain order to keep traffic moving safely and prevent accidents. A real-time traffic light control system was created using the LPC2148 embedded controller. GPIO pins were configured as outputs to control the red, yellow, and green LEDs, and a programmed sequence was executed using IO0DIR, IO0SET, and IO0CLR with calibrated delay routines.', 'algorithm': ['Start the program. Set up the LPC2148 microcontroller.', 'Set the GPIO pins linked to the red, yellow, and green LEDs to output mode (P0.10, P0.11, P0.12).', 'Turn on the red LED and turn off the green and yellow LEDs for 5 seconds (delay 500).', 'Turn on the green LED and turn off the red and yellow LEDs for 5 seconds (delay 500).', 'Turn on the yellow LED and turn off the red and green LEDs for 2 seconds (delay 200).', 'Repeat the cycle continuously to maintain orderly traffic regulation.'], 'files': [{'path': 'lpc2148_traffic.c', 'source': 'lpc2148_traffic.c', 'role': 'source', 'content': '#include <LPC214x.h>\n\n#define RED     (1U << 10)  // P0.10\n#define YELLOW  (1U << 11)  // P0.11\n#define GREEN   (1U << 12)  // P0.12\n\n#define ALL_LEDS (RED | YELLOW | GREEN)\n\nvoid delay(unsigned int count)\n{\n    unsigned int i, j;\n\n    for (i = 0; i < count; i++)\n        for (j = 0; j < 6000; j++);\n}\n\nvoid traffic_light(unsigned int signal)\n{\n    IO0CLR = ALL_LEDS;  // Turn OFF all LEDs\n    IO0SET = signal;    // Turn ON selected LED\n}\n\nint main(void)\n{\n    // Select GPIO function for P0.10, P0.11 and P0.12\n    PINSEL0 &= ~((3U << 20) |\n                 (3U << 22) |\n                 (3U << 24));\n\n    // Configure LED pins as outputs\n    IO0DIR |= ALL_LEDS;\n\n    // Initially turn OFF all LEDs\n    IO0CLR = ALL_LEDS;\n\n    while (1)\n    {\n        // RED: Stop\n        traffic_light(RED);\n        delay(500);\n\n        // GREEN: Go\n        traffic_light(GREEN);\n        delay(500);\n\n        // YELLOW: Caution\n        traffic_light(YELLOW);\n        delay(200);\n    }\n}\n\n/*\n============================================================================\nEXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):\n============================================================================\nA traffic light control system is a type of embedded application that\nhelps manage how cars move through intersections. It uses red, yellow, and\ngreen lights in a certain order to keep traffic moving safely and prevent\naccidents. A real-time traffic light control system was created using the\nLPC2148 embedded controller. GPIO pins were configured as outputs to\ncontrol the red, yellow, and green LEDs, and a programmed sequence was\nexecuted using IO0DIR, IO0SET, and IO0CLR with calibrated delay routines.\n============================================================================\n*/\n'}], 'run': {'kind': 'embedded', 'entry': 'lpc2148_traffic.c', 'hardware': 'NXP LPC2148 (ARM7TDMI-S)'}, 'lab_serial': 10, 'lab_label': 'ERTOS Exp 10', 'output_url': 'outputs/ertos_exp10_drive_output.pdf', 'output_files': ['outputs/ertos_exp10_drive_output.pdf', 'outputs/ertos_exp10_output.pdf']}, {'id': 23, 'slug': 'cn-crc-cyclic-redundancy-check', 'title': 'Experiment 6 – CRC (Cyclic Redundancy Check)', 'language': 'c', 'aliases': ['crc', 'cyclic redundancy check', 'cn 6', 'cn exp 6', 'crc error detection'], 'description': 'Implementation of Cyclic Redundancy Check (CRC) error detection using modulo-2 polynomial division.', 'aim': 'To write a C program to implement Cyclic Redundancy Check (CRC) error detection technique.', 'theory': 'CRC is an error-detecting code based on polynomial arithmetic modulo 2. The sender generates a codeword by appending remainder bits from dividing data bits by a predetermined generator polynomial. The receiver performs the same division; a non-zero remainder indicates transmission error.', 'algorithm': ['Read data bits and generator polynomial bits.', 'Append (m - 1) zeros to the data bits, where m is the generator length.', 'Perform modulo-2 binary division using XOR operations.', 'Append the resulting (m - 1) remainder bits to original data to construct the transmitted codeword.', 'At receiver, perform modulo-2 division on received codeword with generator polynomial.', 'If remainder is all zeros report no error; otherwise report error detected.'], 'files': [{'path': 'crc.c', 'source': 'crc.c', 'role': 'source', 'content': '#include <stdio.h>\n#include <string.h>\n\nvoid divide(char data[], char gen[], int n, int m)\n{\n    for (int i = 0; i <= n - m; i++)\n    {\n        if (data[i] == \'1\')\n        {\n            for (int j = 0; j < m; j++)\n            {\n                data[i + j] =\n                (data[i + j] == gen[j]) ? \'0\' : \'1\';\n            }\n        }\n    }\n}\n\nint main()\n{\n    char data[256], gen[256];\n    char temp[256], codeword[256];\n    char received[256];\n\n    int n, m, i;\n\n    printf("Enter data bits: ");\n    scanf("%255s", data);\n\n    printf("Enter generator bits: ");\n    scanf("%255s", gen);\n\n    n = strlen(data);\n    m = strlen(gen);\n\n    if (n == 0 || m < 2 || n + m - 1 >= 256 || gen[0] != \'1\')\n    {\n        printf("Invalid input!\\n");\n        return 1;\n    }\n\n    for (i = 0; i < n; i++)\n        if (data[i] != \'0\' && data[i] != \'1\')\n            return printf("Invalid data!\\n"), 1;\n\n    for (i = 0; i < m; i++)\n        if (gen[i] != \'0\' && gen[i] != \'1\')\n            return printf("Invalid generator!\\n"), 1;\n\n    strcpy(temp, data);\n\n    for (i = 0; i < m - 1; i++)\n        temp[n + i] = \'0\';\n\n    temp[n + m - 1] = \'\\0\';\n\n    divide(temp, gen, n + m - 1, m);\n\n    strcpy(codeword, data);\n    strncat(codeword, temp + n, m - 1);\n\n    printf("\\nCRC Remainder: %.*s\\n", m - 1, temp + n);\n    printf("Transmitted Codeword: %s\\n", codeword);\n\n    printf("\\nEnter received codeword: ");\n    scanf("%255s", received);\n\n    if (strlen(received) != n + m - 1)\n    {\n        printf("Invalid codeword length!\\n");\n        return 1;\n    }\n\n    strcpy(temp, received);\n\n    divide(temp, gen, n + m - 1, m);\n\n    for (i = n; i < n + m - 1; i++)\n        if (temp[i] != \'0\')\n            break;\n\n    if (i == n + m - 1)\n        printf("No error detected.\\n");\n    else\n        printf("Error detected.\\n");\n\n    return 0;\n}\n\n/*\n============================================================================\nHOW TO RUN THIS EXPERIMENT:\n============================================================================\nRequirements: GCC (MinGW / MSYS2 / build-essential) or Clang.\n\n1. Compilation:\n   Windows:   gcc crc.c -o crc.exe\n   Linux/Mac: gcc crc.c -o crc\n\n2. Execution:\n   Windows:   .\\crc.exe\n   Linux/Mac: ./crc\n\n3. Sample Run:\n   Enter data bits: 110101\n   Enter generator bits: 1011\n   -> Output:\n      CRC Remainder: 001\n      Transmitted Codeword: 110101001\n   Enter received codeword: 110101001\n   -> Output:\n      No error detected.\n============================================================================\nEXPERIMENT THEORY (Computer Networks - Cyclic Redundancy Check):\n============================================================================\nCyclic Redundancy Check (CRC) is an error-detecting code widely used in\ndigital communication networks and storage systems (e.g., Ethernet, Wi-Fi,\nand HDLC) to verify frame integrity.\n\nMathematical Foundation:\n1. Polynomial Representation: A binary string b_n b_{n-1} ... b_0 is represented\n   as a polynomial M(x) = b_n x^n + b_{n-1} x^{n-1} + ... + b_0.\n2. Generator Polynomial G(x): A predetermined divisor polynomial of degree (m-1)\n   known to both sender and receiver. The leading and trailing bits must be 1.\n3. Zero Padding: The sender multiplies M(x) by x^(m-1), effectively appending\n   (m - 1) zeros to the data bits.\n4. Modulo-2 Division: The padded bit string is divided by G(x) using modulo-2\n   arithmetic (bitwise XOR addition without carries).\n5. Transmitted Codeword T(x): The resulting remainder R(x) of length (m - 1) is\n   appended to the original message: T(x) = M(x) * x^(m-1) + R(x).\n6. Verification at Receiver: The receiver divides the incoming bit stream T\'(x)\n   by G(x).\n   - If remainder R\'(x) == 0: The transmission is assumed error-free.\n   - If remainder R\'(x) != 0: An error occurred, and the frame is rejected.\n\nError Detection Capabilities:\n- Detects all single-bit errors.\n- Detects all double-bit errors (if G(x) contains at least 3 terms).\n- Detects any odd number of errors (if G(x) has (x + 1) as a factor).\n- Detects all burst errors of length <= (m - 1).\n============================================================================\n*/\n\n'}], 'run': {'kind': 'c', 'entry': 'crc.c'}, 'subject': 'CN', 'lab_serial': 6, 'lab_label': 'CN Exp 06', 'output_url': None}, {'id': 24, 'slug': 'cn-hamming-code-error-detection', 'title': 'Experiment 7 – Hamming Code Error Detection & Correction', 'language': 'c', 'aliases': ['hamming', 'hamming code', 'cn 7', 'cn exp 7', 'hamming error correction'], 'description': 'Implementation of Hamming Code for single-bit error detection and automatic bit correction.', 'aim': 'To write a C program to implement Hamming Code for error detection and correction of data bits.', 'theory': 'Hamming code adds redundant parity bits at power-of-two positions (1, 2, 4, 8, ...). By evaluating parity checks across specific bit subsets, the receiver calculates an error syndrome whose binary value pinpoints the exact corrupted bit position for correction.', 'algorithm': ['Read number of data bits and data bit stream.', 'Calculate number of redundant parity bits r such that 2^r >= n + r + 1.', 'Place data bits and initialize parity bits at positions that are powers of 2.', 'Calculate even parity for each parity bit position.', 'Transmit codeword. At receiver, evaluate parity checks to compute error syndrome.', 'If syndrome is 0, report no error; otherwise report corrupted position and invert bit to correct.'], 'files': [{'path': 'hamming.c', 'source': 'hamming.c', 'role': 'source', 'content': '#include <stdio.h>\n#include <string.h>\n\nint main()\n{\n    int data[50], hamming[100], received[100];\n    int n, r = 0, i, j, k, pos;\n    int syndrome = 0;\n\n    printf("Enter number of data bits: ");\n    scanf("%d", &n);\n\n    if (n < 1 || n > 40)\n    {\n        printf("Invalid number of bits!\\n");\n        return 1;\n    }\n\n    printf("Enter data bits (0 or 1): ");\n\n    for (i = 0; i < n; i++)\n    {\n        scanf("%1d", &data[i]);\n\n        if (data[i] != 0 && data[i] != 1)\n        {\n            printf("Invalid data!\\n");\n            return 1;\n        }\n    }\n\n    while ((1 << r) < n + r + 1)\n        r++;\n\n    int total = n + r;\n\n    j = 0;\n\n    for (i = 1; i <= total; i++)\n    {\n        if ((i & (i - 1)) == 0)\n            hamming[i] = 0;\n        else\n            hamming[i] = data[j++];\n    }\n\n    for (i = 0; i < r; i++)\n    {\n        pos = 1 << i;\n        int parity = 0;\n\n        for (j = 1; j <= total; j++)\n        {\n            if (j & pos)\n                parity ^= hamming[j];\n        }\n\n        hamming[pos] = parity;\n    }\n\n    printf("\\nHamming Code: ");\n\n    for (i = total; i >= 1; i--)\n        printf("%d", hamming[i]);\n\n    printf("\\nEnter received codeword: ");\n\n    for (i = total; i >= 1; i--)\n    {\n        scanf("%1d", &received[i]);\n\n        if (received[i] != 0 && received[i] != 1)\n        {\n            printf("Invalid received data!\\n");\n            return 1;\n        }\n    }\n\n    for (i = 0; i < r; i++)\n    {\n        pos = 1 << i;\n        int parity = 0;\n\n        for (j = 1; j <= total; j++)\n        {\n            if (j & pos)\n                parity ^= received[j];\n        }\n\n        if (parity)\n            syndrome += pos;\n    }\n\n    if (syndrome == 0)\n    {\n        printf("No error detected.\\n");\n    }\n    else if (syndrome <= total)\n    {\n        printf("Error detected at position: %d\\n", syndrome);\n\n        received[syndrome] ^= 1;\n\n        printf("Corrected Codeword: ");\n\n        for (i = total; i >= 1; i--)\n            printf("%d", received[i]);\n    }\n    else\n    {\n        printf("Invalid syndrome!\\n");\n    }\n\n    return 0;\n}\n\n/*\n============================================================================\nHOW TO RUN THIS EXPERIMENT:\n============================================================================\nRequirements: GCC (MinGW / MSYS2 / build-essential) or Clang.\n\n1. Compilation:\n   Windows:   gcc hamming.c -o hamming.exe\n   Linux/Mac: gcc hamming.c -o hamming\n\n2. Execution:\n   Windows:   .\\hamming.exe\n   Linux/Mac: ./hamming\n\n3. Sample Run:\n   Enter number of data bits: 4\n   Enter data bits (0 or 1): 1 0 1 1\n   -> Output:\n      Hamming Code: 1010101\n   Enter received codeword: 1010101\n   -> Output:\n      No error detected.\n\n   (Or introduce an error: e.g. 1011101 -> Error detected at position: 4)\n============================================================================\nEXPERIMENT THEORY (Computer Networks - Hamming Code Error Detection & Correction):\n============================================================================\nHamming Code is a linear error-correcting code invented by Richard Hamming in 1950.\nIt can detect up to two simultaneous bit errors and correct single-bit errors (SEC-DED).\n\nOperating Principles:\n1. Redundancy Bit Calculation:\n   For \'n\' data bits and \'r\' parity/redundant bits, the relationship is given\n   by the Hamming Inequality:\n       2^r >= n + r + 1\n2. Bit Positioning (1-based indexing):\n   - Redundant bits occupy bit positions that are powers of 2: 1, 2, 4, 8, 16, etc.\n   - Data bits occupy all remaining bit positions: 3, 5, 6, 7, 9, 10, etc.\n3. Parity Determination:\n   Each parity bit P_i at position 2^i calculates even parity across all bit\n   positions whose binary representation has the i-th bit set to 1.\n   - P1 (pos 1): checks bits 1, 3, 5, 7, 9, 11, ...\n   - P2 (pos 2): checks bits 2, 3, 6, 7, 10, 11, ...\n   - P4 (pos 4): checks bits 4, 5, 6, 7, 12, 13, ...\n   - P8 (pos 8): checks bits 8-15, 24-31, ...\n4. Syndrome Evaluation:\n   At the receiver, the parity checks are recomputed over the entire received\n   word. Each check produces an error bit S_i. The combined binary value of\n   (S_r ... S_2 S_1) is known as the Error Syndrome:\n   - Syndrome == 0: No error occurred.\n   - Syndrome > 0: Indicates the EXACT bit position of the corrupted bit.\n5. Error Correction:\n   Inverting the bit at received[syndrome] restores the original codeword.\n============================================================================\n*/\n\n'}], 'run': {'kind': 'c', 'entry': 'hamming.c'}, 'subject': 'CN', 'lab_serial': 7, 'lab_label': 'CN Exp 07', 'output_url': None}, {'id': 25, 'slug': 'cn-checksum-error-detection', 'title': 'Experiment 8 – Checksum Error Detection', 'language': 'c', 'aliases': ['checksum', 'checksum detection', 'cn 8', 'cn exp 8', 'binary checksum'], 'description': "Implementation of Internet Checksum algorithm using 8-bit one's complement arithmetic and end-around carry.", 'aim': "To write a C program to implement Checksum error detection using one's complement addition.", 'theory': "The checksum algorithm partitions data into equal k-bit words and sums them using one's complement arithmetic with end-around carry. The sender transmits the bitwise complement as the checksum. The receiver sums data words plus checksum; a total equal to all 1s confirms error-free transmission.", 'algorithm': ['Read number of 8-bit data words and their binary representations.', "Accumulate one's complement sum with end-around carry for any overflow past 255.", 'Compute checksum as bitwise NOT of final accumulated sum.', 'At receiver, sum all received data words plus received checksum.', 'If receiver sum equals 255 (all 1s), report no error; otherwise report error detected.'], 'files': [{'path': 'checksum.c', 'source': 'checksum.c', 'role': 'source', 'content': '#include <stdio.h>\n#include <string.h>\n\nint readBinary()\n{\n    char bits[20];\n    int value = 0;\n\n    scanf("%19s", bits);\n\n    if (strlen(bits) != 8)\n        return -1;\n\n    for (int i = 0; i < 8; i++)\n    {\n        if (bits[i] != \'0\' && bits[i] != \'1\')\n            return -1;\n\n        value = value * 2 + (bits[i] - \'0\');\n    }\n\n    return value;\n}\n\nvoid printBinary(int value)\n{\n    for (int i = 7; i >= 0; i--)\n        printf("%d", (value >> i) & 1);\n}\n\nint add(int sum, int value)\n{\n    sum += value;\n\n    while (sum > 255)\n        sum = (sum & 255) + (sum >> 8);\n\n    return sum;\n}\n\nint main()\n{\n    int n, i, data[20];\n    int sum = 0, checksum;\n    int received, verify = 0;\n\n    printf("Enter number of 8-bit data words: ");\n    scanf("%d", &n);\n\n    if (n < 1 || n > 20)\n    {\n        printf("Invalid number of words!\\n");\n        return 1;\n    }\n\n    printf("Enter %d binary data words:\\n", n);\n\n    for (i = 0; i < n; i++)\n    {\n        data[i] = readBinary();\n\n        if (data[i] < 0)\n        {\n            printf("Invalid 8-bit data!\\n");\n            return 1;\n        }\n\n        sum = add(sum, data[i]);\n    }\n\n    checksum = (~sum) & 255;\n\n    printf("\\nChecksum: ");\n    printBinary(checksum);\n\n    printf("\\n\\nEnter received data words:\\n");\n\n    for (i = 0; i < n; i++)\n    {\n        received = readBinary();\n\n        if (received < 0)\n        {\n            printf("Invalid received data!\\n");\n            return 1;\n        }\n\n        verify = add(verify, received);\n    }\n\n    printf("Enter received checksum: ");\n\n    received = readBinary();\n\n    if (received < 0)\n    {\n        printf("Invalid checksum!\\n");\n        return 1;\n    }\n\n    verify = add(verify, received);\n\n    printf("\\nReceiver Sum: ");\n    printBinary(verify);\n\n    if (verify == 255)\n        printf("\\nNo error detected.\\n");\n    else\n        printf("\\nError detected.\\n");\n\n    return 0;\n}\n\n/*\n============================================================================\nHOW TO RUN THIS EXPERIMENT:\n============================================================================\nRequirements: GCC (MinGW / MSYS2 / build-essential) or Clang.\n\n1. Compilation:\n   Windows:   gcc checksum.c -o checksum.exe\n   Linux/Mac: gcc checksum.c -o checksum\n\n2. Execution:\n   Windows:   .\\checksum.exe\n   Linux/Mac: ./checksum\n\n3. Sample Run:\n   Enter number of 8-bit data words: 2\n   Enter 2 binary data words:\n   10101001\n   00111100\n   -> Output:\n      Checksum: 00011001\n   Enter received data words:\n   10101001\n   00111100\n   Enter received checksum:\n   00011001\n   -> Output:\n      Receiver Sum: 11111111\n      No error detected.\n============================================================================\nEXPERIMENT THEORY (Computer Networks - Checksum Error Detection):\n============================================================================\nThe Checksum algorithm is an error-detection technique widely deployed at the\nTransport layer (TCP, UDP) and Network layer (IPv4 header) of the Internet\nprotocol suite.\n\nMathematical Foundation (One\'s Complement Arithmetic):\n1. Word Segmentation:\n   The message is divided into fixed-width k-bit words (here, 8-bit bytes;\n   in TCP/IP, 16-bit words).\n2. One\'s Complement Addition:\n   All words are summed using one\'s complement addition. In binary arithmetic,\n   if an addition produces an overflow carry bit past the k-th bit (sum > 255),\n   that carry bit must be wrapped around and added to the least significant bit\n   (end-around carry: `(sum & 255) + (sum >> 8)`).\n3. Checksum Generation:\n   The sender inverts all bits of the accumulated sum (bitwise NOT / complement:\n   `(~sum) & 0xFF`). This inverted value is the Checksum and is appended to\n   the data transmission.\n4. Receiver Verification:\n   The receiver sums all received data words PLUS the received checksum word\n   using the identical one\'s complement arithmetic.\n5. Error Decision:\n   - If no corruption occurred: Sum + (~Sum) = all 1s (0xFF or 255 in 8-bit).\n     Inverting the receiver sum produces all 0s (0x00).\n   - If any bit changed during transmission: The sum will not equal all 1s,\n     and an error is reported.\n============================================================================\n*/\n\n'}], 'run': {'kind': 'c', 'entry': 'checksum.c'}, 'subject': 'CN', 'lab_serial': 8, 'lab_label': 'CN Exp 08', 'output_url': None}, {'id': 26, 'slug': 'cn-socket-programming-java', 'title': 'Experiment 9 – Client-Server Socket Programming in Java', 'language': 'java', 'aliases': ['socket', 'socket programming', 'java socket', 'tcp socket', 'cn 9', 'cn socket', 'tcp server client'], 'description': 'Two-way client-server socket communication implementation in Java using ServerSocket and Socket classes over TCP.', 'aim': 'To write a client-server socket program using TCP in Java for two-way communication.', 'theory': 'A Network Socket is one endpoint of a two-way communication link between two programs over a computer network. The ServerSocket class binds to a local port and awaits client connections via accept(). The Socket class establishes connection to the server IP and port. Java streams (BufferedReader, PrintWriter) handle bidirectional character and data transmission.', 'algorithm': ['Initialize ServerSocket on designated port (5000).', 'Invoke serverSocket.accept() to block and wait for client connection.', 'On client, create Socket(host, port) to perform TCP three-way handshake.', 'Bind BufferedReader and PrintWriter streams to socket input and output streams.', 'Client sends string message; Server receives, logs, and echoes back uppercase response.', 'When client sends termination signal (exit), cleanly close streams and socket handles.'], 'files': [{'path': 'TCPServer.java', 'source': 'TCPServer.java', 'role': 'source', 'content': '/*\n * Computer Networks Laboratory - Socket Programming\n * Experiment: Implementation of Concurrent / Two-Way TCP Socket Server in Java\n */\n\nimport java.io.*;\nimport java.net.*;\n\npublic class TCPServer {\n    private static final int PORT = 5000;\n\n    public static void main(String[] args) {\n        System.out.println("==================================================");\n        System.out.println("   TCP Echo & Communication Server Started        ");\n        System.out.println("==================================================");\n        System.out.println("[*] Server listening on port: " + PORT);\n\n        try (ServerSocket serverSocket = new ServerSocket(PORT)) {\n            System.out.println("[*] Waiting for incoming client connection...");\n\n            while (true) {\n                Socket clientSocket = serverSocket.accept();\n                String clientIP = clientSocket.getInetAddress().getHostAddress();\n                int clientPort = clientSocket.getPort();\n                System.out.println("\\n[+] Client connected from: " + clientIP + ":" + clientPort);\n\n                // Handle client in session\n                handleClient(clientSocket);\n                break; // Session completed\n            }\n        } catch (IOException e) {\n            System.err.println("[!] Server Exception: " + e.getMessage());\n        }\n    }\n\n    private static void handleClient(Socket socket) {\n        try (\n            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));\n            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);\n            BufferedReader console = new BufferedReader(new InputStreamReader(System.in))\n        ) {\n            out.println("CONNECTED: Welcome to Java TCP Server. Type \'exit\' to quit.");\n\n            String clientMsg;\n            while ((clientMsg = in.readLine()) != null) {\n                System.out.println("[Client]: " + clientMsg);\n                if (clientMsg.equalsIgnoreCase("exit") || clientMsg.equalsIgnoreCase("quit")) {\n                    out.println("BYE: Connection closed by request.");\n                    System.out.println("[-] Client requested termination.");\n                    break;\n                }\n\n                String echoResponse = "SERVER ECHO: " + clientMsg.toUpperCase();\n                out.println(echoResponse);\n            }\n        } catch (IOException e) {\n            System.err.println("[!] Communication error: " + e.getMessage());\n        } finally {\n            try {\n                socket.close();\n                System.out.println("[*] Client socket closed successfully.");\n            } catch (IOException ex) {\n                System.err.println("[!] Error closing socket: " + ex.getMessage());\n            }\n        }\n    }\n}\n\n/*\n============================================================================\nHOW TO RUN THIS EXPERIMENT:\n============================================================================\nPrerequisites: JDK 8 or higher (`javac -version` and `java -version`).\n\n1. Terminal 1 (Start Server):\n   javac TCPServer.java\n   java TCPServer\n   -> Server starts and listens on port 5000:\n      [*] Server listening on port: 5000\n      [*] Waiting for incoming client connection...\n\n2. Terminal 2 (Start Client):\n   javac TCPClient.java\n   java TCPClient\n   -> Client connects, sends messages, and receives uppercase echo responses.\n\n3. Termination:\n   Type \'exit\' in the client console to terminate the session cleanly.\n============================================================================\nEXPERIMENT THEORY (Computer Networks - Java Socket Programming Server):\n============================================================================\nA Network Socket is one endpoint of a two-way communication link between\ntwo programs running over a computer network. In Java, networking APIs are\nencapsulated in the java.net package, built on top of the TCP/IP stack.\n\nCore Concepts:\n1. TCP (Transmission Control Protocol):\n   A connection-oriented, reliable, byte-stream transport layer protocol.\n   Before data transfer begins, a three-way handshake (SYN, SYN-ACK, ACK)\n   establishes a virtual circuit between client and server.\n\n2. ServerSocket (Server Endpoint):\n   The ServerSocket class binds to a specific port on the local machine and\n   listens for incoming connection requests via its blocking accept() method.\n   When a connection is received, accept() returns a dedicated Socket instance\n   for communicating with that specific client.\n\n3. Socket (Client Endpoint):\n   The Socket class initiates the TCP connection by specifying the server\'s\n   IP address (or hostname) and port number.\n\n4. Stream-Based I/O:\n   - InputStream / BufferedReader: Reads incoming byte/character streams from the\n     remote endpoint.\n   - OutputStream / PrintWriter: Transmits outgoing byte/character streams to the\n     remote endpoint with automatic flushing.\n\n5. Connection Lifecycle:\n   1) Server creates ServerSocket(port) and invokes accept().\n   2) Client constructs Socket(host, port) to establish handshake.\n   3) Both sides exchange data through input/output streams.\n   4) Connections are cleanly terminated by closing stream handles and sockets.\n============================================================================\n*/\n\n'}, {'path': 'TCPClient.java', 'source': 'TCPClient.java', 'role': 'source', 'content': '/*\n * Computer Networks Laboratory - Socket Programming\n * Experiment: Implementation of TCP Socket Client in Java\n */\n\nimport java.io.*;\nimport java.net.*;\n\npublic class TCPClient {\n    private static final String SERVER_HOST = "127.0.0.1";\n    private static final int SERVER_PORT = 5000;\n\n    public static void main(String[] args) {\n        System.out.println("==================================================");\n        System.out.println("           TCP Client Initializing                ");\n        System.out.println("==================================================");\n        System.out.println("[*] Connecting to server at " + SERVER_HOST + ":" + SERVER_PORT + "...");\n\n        try (\n            Socket socket = new Socket(SERVER_HOST, SERVER_PORT);\n            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));\n            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);\n            BufferedReader console = new BufferedReader(new InputStreamReader(System.in))\n        ) {\n            System.out.println("[+] Successfully connected to server!");\n\n            // Read welcome greeting\n            String greeting = in.readLine();\n            System.out.println("[Server]: " + greeting);\n\n            // Pre-defined test messages if console is non-interactive, or interactive loop\n            String[] testMessages = {"Hello Server!", "Testing Computer Networks Socket", "Socket Programming in Java", "exit"};\n            int msgIdx = 0;\n\n            while (true) {\n                System.out.print("\\nEnter message to send (or \'exit\' to quit): ");\n                String userInput = null;\n                if (System.console() != null) {\n                    userInput = console.readLine();\n                } else if (msgIdx < testMessages.length) {\n                    userInput = testMessages[msgIdx++];\n                    System.out.println(userInput);\n                }\n\n                if (userInput == null || userInput.trim().isEmpty()) {\n                    continue;\n                }\n\n                // Send message to server\n                out.println(userInput);\n\n                // Receive response\n                String response = in.readLine();\n                if (response != null) {\n                    System.out.println("[Response]: " + response);\n                }\n\n                if (userInput.equalsIgnoreCase("exit") || userInput.equalsIgnoreCase("quit")) {\n                    System.out.println("[*] Disconnecting from server...");\n                    break;\n                }\n            }\n        } catch (ConnectException e) {\n            System.err.println("[!] Connection failed: Is the server running on " + SERVER_HOST + ":" + SERVER_PORT + "?");\n        } catch (IOException e) {\n            System.err.println("[!] I/O Exception: " + e.getMessage());\n        }\n    }\n}\n\n/*\n============================================================================\nHOW TO RUN THIS EXPERIMENT:\n============================================================================\nPrerequisites: JDK 8 or higher (`javac -version` and `java -version`).\n\n1. Terminal 1 (Start Server First):\n   javac TCPServer.java\n   java TCPServer\n\n2. Terminal 2 (Start Client):\n   javac TCPClient.java\n   java TCPClient\n\n3. Communication & Exit:\n   Enter any text message to transmit to the server and receive the echo.\n   Type \'exit\' to terminate the client connection cleanly.\n============================================================================\nEXPERIMENT THEORY (Computer Networks - Java Socket Programming Client):\n============================================================================\nThe client application acts as the initiator in the client-server architecture.\nIn Java, constructing a Socket(host, port) performs the DNS resolution and\nTCP handshake with the remote listening host.\n\nKey Operational Steps:\n1. Address Resolution: Locates target host by domain name or IPv4/IPv6 loopback.\n2. Connection Request: Sends SYN packet to server\'s designated port.\n3. Stream Binding: Upon receiving SYN-ACK and completing handshake, local port\n   is dynamically assigned by the OS, and I/O streams are attached.\n4. Transmission & Reception: Writes data to OutputStream, reads responses from\n   InputStream.\n5. Graceful Disconnection: Sends FIN packet when closing the socket, ensuring\n   all buffered packets are acknowledged.\n============================================================================\n*/\n\n'}], 'run': {'kind': 'java', 'entry': 'TCPServer.java'}, 'subject': 'CN', 'lab_serial': 9, 'lab_label': 'CN Exp 09', 'output_url': None}, {'id': 27, 'slug': 'cn-dijkstra-shortest-path', 'title': "Experiment 10 – Dijkstra's Shortest Path Routing Algorithm", 'language': 'c', 'aliases': ['dijkstra', 'shortest path', 'routing', 'link state routing', 'ospf', 'cn 10', 'cn dijkstra', 'routing algorithm'], 'description': "Implementation of Dijkstra's algorithm in C to compute single-source shortest path routing tables for Link State Routing (OSPF).", 'aim': "To implement Dijkstra's shortest path routing algorithm in C to find minimum cost routes in a computer network.", 'theory': "Dijkstra's algorithm is a greedy algorithm used in Link-State routing protocols like OSPF and IS-IS to compute the Shortest Path Tree (SPT) from a single source router to all other network routers. Each router maintains a global link-state database (LSDB), and through edge relaxation, computes the optimal routing table.", 'algorithm': ['Initialize distance array: dist[source] = 0, and dist[i] = cost[source][i] for all other nodes.', 'Mark source as visited in visited[] array and set parent pointers.', 'Find unvisited node u with minimum distance value.', 'Mark u as visited.', 'Update distances of all unvisited neighbors v: if dist[u] + cost[u][v] < dist[v], then dist[v] = dist[u] + cost[u][v] and parent[v] = u.', 'Repeat until all nodes are visited or minimum distance is infinity.', 'Print routing table displaying destination, minimum cost, and complete node path.'], 'files': [{'path': 'dijkstra.c', 'source': 'dijkstra.c', 'role': 'source', 'content': '/*\n * Computer Networks Laboratory - Routing Algorithms\n * Experiment 10: Dijkstra\'s Shortest Path Routing Algorithm\n * Demonstrates Link State Routing (OSPF) to find minimum-cost routes\n */\n\n#include <stdio.h>\n#include <stdbool.h>\n\n#define INFINITY 9999\n#define MAX_NODES 20\n\nvoid printPath(int parent[], int j) {\n    if (parent[j] == -1) {\n        printf("%d", j);\n        return;\n    }\n    printPath(parent, parent[j]);\n    printf(" -> %d", j);\n}\n\nvoid dijkstra(int cost[MAX_NODES][MAX_NODES], int n, int source) {\n    int distance[MAX_NODES];\n    bool visited[MAX_NODES];\n    int parent[MAX_NODES];\n\n    for (int i = 0; i < n; i++) {\n        distance[i] = cost[source][i];\n        visited[i] = false;\n        parent[i] = (cost[source][i] != INFINITY && i != source) ? source : -1;\n    }\n\n    distance[source] = 0;\n    visited[source] = true;\n    parent[source] = -1;\n\n    for (int count = 1; count < n - 1; count++) {\n        int min_dist = INFINITY;\n        int next_node = -1;\n\n        for (int i = 0; i < n; i++) {\n            if (!visited[i] && distance[i] < min_dist) {\n                min_dist = distance[i];\n                next_node = i;\n            }\n        }\n\n        if (next_node == -1) break;\n        visited[next_node] = true;\n\n        for (int i = 0; i < n; i++) {\n            if (!visited[i] && cost[next_node][i] != INFINITY) {\n                if (distance[next_node] + cost[next_node][i] < distance[i]) {\n                    distance[i] = distance[next_node] + cost[next_node][i];\n                    parent[i] = next_node;\n                }\n            }\n        }\n    }\n\n    printf("\\n===============================================================\\n");\n    printf(" Routing Table for Source Router: %d (Link-State Shortest Path)\\n", source);\n    printf("===============================================================\\n");\n    printf(" Destination | Minimum Cost | Shortest Path\\n");\n    printf("-------------|--------------|----------------------------------\\n");\n\n    for (int i = 0; i < n; i++) {\n        if (i == source) {\n            printf("      %2d     |      %2d      | [Local Node]\\n", i, 0);\n        } else if (distance[i] == INFINITY) {\n            printf("      %2d     |   Unreachable| No Path\\n", i);\n        } else {\n            printf("      %2d     |      %2d      | ", i, distance[i]);\n            printPath(parent, i);\n            printf("\\n");\n        }\n    }\n    printf("===============================================================\\n");\n}\n\nint main() {\n    int n, source;\n    int cost[MAX_NODES][MAX_NODES];\n\n    printf("=====================================================\\n");\n    printf("   Dijkstra\'s Shortest Path Routing Algorithm (CN)   \\n");\n    printf("=====================================================\\n");\n    printf("Enter number of network nodes/routers: ");\n    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX_NODES) {\n        printf("Invalid input or non-interactive console. Using default 5-node topology.\\n");\n        n = 5;\n        int default_cost[5][5] = {\n            {0, 4, 2, INFINITY, INFINITY},\n            {4, 0, 1, 5, INFINITY},\n            {2, 1, 0, 8, 10},\n            {INFINITY, 5, 8, 0, 2},\n            {INFINITY, INFINITY, 10, 2, 0}\n        };\n        for (int i = 0; i < 5; i++)\n            for (int j = 0; j < 5; j++)\n                cost[i][j] = default_cost[i][j];\n        source = 0;\n    } else {\n        printf("Enter routing cost matrix (%dx%d, 0 for self, 9999 for infinity):\\n", n, n);\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < n; j++) {\n                scanf("%d", &cost[i][j]);\n                if (i != j && cost[i][j] == 0) cost[i][j] = INFINITY;\n            }\n        }\n        printf("Enter source router (0 to %d): ", n - 1);\n        if (scanf("%d", &source) != 1 || source < 0 || source >= n) {\n            source = 0;\n        }\n    }\n\n    dijkstra(cost, n, source);\n    return 0;\n}\n\n/*\n============================================================================\nHOW TO RUN THIS EXPERIMENT:\n============================================================================\nPrerequisites: GCC compiler (`gcc --version`).\n\n1. Compile the C code:\n   gcc dijkstra.c -o dijkstra\n\n2. Run the executable:\n   ./dijkstra\n\n3. Interactive Sample Run:\n   Enter number of network nodes/routers: 5\n   Enter routing cost matrix (5x5):\n   0 4 2 9999 9999\n   4 0 1 5 9999\n   2 1 0 8 10\n   9999 5 8 0 2\n   9999 9999 10 2 0\n   Enter source router (0 to 4): 0\n\n   Output:\n   Destination | Minimum Cost | Shortest Path\n        0      |       0      | [Local Node]\n        1      |       3      | 0 -> 2 -> 1\n        2      |       2      | 0 -> 2\n        3      |       8      | 0 -> 2 -> 1 -> 3\n        4      |      10      | 0 -> 2 -> 1 -> 3 -> 4\n============================================================================\nEXPERIMENT THEORY (Computer Networks - Dijkstra\'s Link-State Routing):\n============================================================================\nDijkstra\'s Algorithm is a greedy single-source shortest path algorithm used\nwidely in computer networking for unicast routing protocols, notably Open\nShortest Path First (OSPF) and Intermediate System to Intermediate System\n(IS-IS) in the Link State Routing domain.\n\nKey Principles:\n1. Global Topology Knowledge:\n   Every router floods Link State Advertisements (LSAs) containing the state\n   and metric of its directly connected links to all routers via Dijkstra\'s\n   algorithm so that each router builds an identical link-state database (LSDB).\n\n2. Forward Search Tree (SPT):\n   The router places itself as the root and iteratively builds a Shortest\n   Path Tree (SPT) by maintaining:\n   - Visited Set (Permanent nodes with confirmed minimal cost).\n   - Tentative Set (Candidate neighbors evaluated through relaxation).\n\n3. Edge Relaxation:\n   If traversing via node \'u\' to \'v\' produces a strictly lower cumulative\n   path cost:\n   dist[v] = min(dist[v], dist[u] + cost[u][v])\n\n4. Forwarding Table Generation:\n   From the completed SPT, the router extracts the next-hop IP address and\n   outgoing interface for each destination subnet, achieving loop-free routing\n   with O(V^2) or O(E + V log V) convergence time.\n============================================================================\n*/\n'}], 'run': {'kind': 'c', 'entry': 'dijkstra.c'}, 'subject': 'CN', 'lab_serial': 10, 'lab_label': 'CN Exp 10', 'output_url': None}, {'id': 28, 'slug': 'cn-static-routing-gns3', 'title': 'Static Routing Configuration in GNS3 (Router & Host Setup)', 'language': 'text', 'aliases': ['static routing', 'gns3', 'routing', 'cisco', 'cn 11', 'cn 7 routing', 'static route', 'cisco ios', 'ip route'], 'description': 'Complete Cisco IOS and VPCS terminal configuration commands for setting up static routes across R1 and R2 routers in a GNS3 network topology.', 'aim': 'To configure and verify Static Routing between two Cisco routers connecting distinct subnets using GNS3.', 'theory': "Static routing is a method where routes are manually programmed into a router's routing table using the 'ip route <destination-network> <subnet-mask> <next-hop-ip>' command. Unlike dynamic routing protocols, static routes do not incur bandwidth or CPU overhead and provide predictable deterministic packet paths. In this GNS3 topology (PC1 - Switch1 - R1 - R2 - Switch2 - PC2), R1 is configured with a static route to the 192.168.3.0/24 subnet via R2 (192.168.2.2), and R2 with a static route to the 192.168.1.0/24 subnet via R1 (192.168.2.1), enabling bidirectional ICMP echo ping communication.", 'algorithm': ['Configure host IP, subnet mask, and default gateway on PC1 (192.168.1.2/24 -> gateway 192.168.1.1).', "On R1, configure FastEthernet 0/0 (192.168.1.1/24) and FastEthernet 1/0 (192.168.2.1/24) interfaces with 'no shutdown'.", 'On R1, add static route: ip route 192.168.3.0 255.255.255.0 192.168.2.2.', "On R2, configure FastEthernet 1/0 (192.168.2.2/24) and FastEthernet 0/0 (192.168.3.1/24) interfaces with 'no shutdown'.", 'On R2, add static route: ip route 192.168.1.0 255.255.255.0 192.168.2.1.', 'Configure host IP, subnet mask, and default gateway on PC2 (192.168.3.2/24 -> gateway 192.168.3.1).', "Verify interfaces using 'show ip interface brief' and routing table using 'show ip route'.", 'Test end-to-end connectivity by pinging PC2 from PC1 (ping 192.168.3.2) and vice-versa.'], 'files': [{'path': 'static_routing_gns3_commands.txt', 'source': 'static_routing_gns3_commands.txt', 'role': 'source', 'content': "EXPERIMENT 7 — STATIC ROUTING\nGNS3 topology: PC1 — Switch1 — R1 — R2 — Switch2 — PC2\n\nIP ADDRESSING\nPC1: 192.168.1.2/24, gateway 192.168.1.1\nR1 FastEthernet0/0: 192.168.1.1/24\nR1 FastEthernet1/0: 192.168.2.1/24\nR2 FastEthernet1/0: 192.168.2.2/24\nR2 FastEthernet0/0: 192.168.3.1/24\nPC2: 192.168.3.2/24, gateway 192.168.3.1\nSubnet mask: 255.255.255.0\n\nRun each section in the named device's console, in order.\nIf an interface name differs on your router, use the interface actually connected in your topology.\n\n============================================================\nPC1 TERMINAL\n============================================================\nip 192.168.1.2 255.255.255.0 192.168.1.1\n\n============================================================\nR1 TERMINAL\n============================================================\nenable\nconfigure terminal\ninterface fastethernet 0/0\nip address 192.168.1.1 255.255.255.0\nno shutdown\nexit\ninterface fastethernet 1/0\nip address 192.168.2.1 255.255.255.0\nno shutdown\nexit\nip route 192.168.3.0 255.255.255.0 192.168.2.2\nend\n\n============================================================\nR2 TERMINAL\n============================================================\nenable\nconfigure terminal\ninterface fastethernet 1/0\nip address 192.168.2.2 255.255.255.0\nno shutdown\nexit\ninterface fastethernet 0/0\nip address 192.168.3.1 255.255.255.0\nno shutdown\nexit\nip route 192.168.1.0 255.255.255.0 192.168.2.1\nend\n\n============================================================\nPC2 TERMINAL\n============================================================\nip 192.168.3.2 255.255.255.0 192.168.3.1\n\n============================================================\nVERIFY\n============================================================\nOn R1 and R2:\nshow ip interface brief\nshow ip route\n\nOn PC1:\nping 192.168.3.2\n\nOn PC2:\nping 192.168.1.2\n"}], 'run': {'kind': 'manual', 'entry': 'static_routing_gns3_commands.txt'}, 'subject': 'CN', 'lab_serial': 11, 'lab_label': 'CN Exp 11', 'output_url': None}]

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LabX Remote - Minimalist Experiment Distribution</title>
  <script src="jszip.min.js"></script>
  <script src="pdf.min.js"></script>
  <script>
    if (typeof JSZip === 'undefined') {
      document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"><\\/script>');
    }
    if (typeof pdfjsLib === 'undefined') {
      document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"><\\/script>');
    }
  </script>
  <style>
    :root {
      --bg: #000000;
      --card-bg: #0a0a0a;
      --card-hover: #121212;
      --border: #222222;
      --border-hover: #444444;
      --text: #ffffff;
      --muted: #888888;
      --subtle: #555555;
      --code-bg: #050505;
      --white: #ffffff;
      --black: #000000;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 2rem 1.5rem;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }
    .container {
      max-width: 1320px;
      margin: 0 auto;
    }
    header {
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 2rem;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 1.5rem;
    }
    .header-left h1 {
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.03em;
      color: var(--white);
    }
    .header-left p {
      color: var(--muted);
      font-size: 0.9rem;
      margin-top: 0.35rem;
    }
    .badge-bar {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: #111111;
      color: var(--white);
      border: 1px solid var(--border);
      padding: 0.3rem 0.75rem;
      border-radius: 4px;
      font-size: 0.78rem;
      font-weight: 500;
      text-decoration: none;
      transition: all 0.15s ease;
    }
    .badge:hover {
      border-color: var(--white);
      background: #1a1a1a;
    }

    /* Top Section: Monochromatic Horizontal Rail */
    .catalog-section {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 2.5rem;
    }
    .section-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.25rem;
    }
    .tabs-group {
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
    }
    .tab-btn {
      background: #0a0a0a;
      color: var(--muted);
      border: 1px solid var(--border);
      padding: 0.4rem 0.9rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 600;
      transition: all 0.15s ease;
    }
    .tab-btn:hover {
      color: var(--white);
      border-color: #555555;
    }
    .tab-btn.active {
      background: var(--white);
      color: var(--black);
      border-color: var(--white);
    }
    .search-box {
      background: #000000;
      border: 1px solid var(--border);
      color: var(--white);
      padding: 0.4rem 0.85rem;
      border-radius: 4px;
      font-size: 0.82rem;
      width: 260px;
      outline: none;
      transition: border-color 0.15s ease;
    }
    .search-box:focus {
      border-color: var(--white);
    }
    .rail-controls {
      display: flex;
      gap: 0.4rem;
      align-items: center;
    }
    .nav-arrow-btn {
      background: #0a0a0a;
      border: 1px solid var(--border);
      color: var(--white);
      width: 32px;
      height: 32px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.15s ease;
    }
    .nav-arrow-btn:hover {
      background: var(--white);
      color: var(--black);
      border-color: var(--white);
    }

    /* Cards Horizontal Rail */
    .cards-rail {
      display: flex;
      gap: 1.25rem;
      overflow-x: auto;
      padding: 0.5rem 0.25rem 1.25rem;
      scroll-snap-type: x mandatory;
      scrollbar-width: thin;
      scrollbar-color: #333333 #0a0a0a;
    }
    .cards-rail::-webkit-scrollbar {
      height: 6px;
    }
    .cards-rail::-webkit-scrollbar-track {
      background: #0a0a0a;
      border-radius: 3px;
    }
    .cards-rail::-webkit-scrollbar-thumb {
      background: #333333;
      border-radius: 3px;
    }
    .cards-rail::-webkit-scrollbar-thumb:hover {
      background: #555555;
    }

    .card {
      flex: 0 0 360px;
      scroll-snap-align: start;
      background: #050505;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.15s ease;
    }
    .card:hover {
      border-color: #444444;
      background: var(--card-hover);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }
    .tag {
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: #111111;
      padding: 0.2rem 0.5rem;
      border-radius: 3px;
      color: var(--white);
      border: 1px solid var(--border);
      display: inline-block;
      font-weight: 600;
    }
    .copy-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: var(--white);
      color: var(--black);
      border: 1px solid var(--white);
      border-radius: 4px;
      padding: 0.32rem 0.7rem;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .copy-btn:hover {
      background: #e5e5e5;
    }
    .copy-btn.copied {
      background: #222222 !important;
      color: var(--white) !important;
      border-color: #555555 !important;
    }
    .card h3 {
      margin: 0.35rem 0;
      color: var(--white);
      font-size: 1rem;
      font-weight: 600;
      line-height: 1.35;
    }
    .file-pill {
      font-size: 0.72rem;
      color: var(--muted);
      background: #000000;
      padding: 0.2rem 0.5rem;
      border-radius: 3px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      margin-top: 0.4rem;
      display: inline-block;
      border: 1px solid var(--border);
    }
    .card-cmd-box {
      background: #000000;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 0.45rem 0.75rem;
      margin-top: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
    }
    .card-cmd-text {
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      color: var(--white);
      overflow-x: auto;
      white-space: nowrap;
      flex: 1;
    }
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--border);
      font-size: 0.8rem;
    }
    a {
      color: var(--white);
      text-decoration: underline;
      text-underline-offset: 3px;
    }
    a:hover {
      color: #cccccc;
    }

    /* Bottom Section: Minimalist Ingester, Terminal, Endpoints */
    .bottom-section {
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }
    .uploader-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.75rem;
    }
    .uploader-header h2 {
      margin: 0.4rem 0 0.25rem;
      color: var(--white);
      font-size: 1.3rem;
      font-weight: 600;
    }
    .drop-zone {
      border: 1px dashed #444444;
      background: #000000;
      border-radius: 6px;
      padding: 2.5rem 1.5rem;
      text-align: center;
      cursor: pointer;
      margin-top: 1.25rem;
      transition: all 0.15s ease;
    }
    .drop-zone:hover, .drop-zone.dragover {
      border-color: var(--white);
      background: #050505;
    }
    .browse-btn {
      background: var(--white);
      color: var(--black);
      border: none;
      padding: 0.35rem 0.85rem;
      border-radius: 3px;
      cursor: pointer;
      font-weight: 600;
      margin-left: 0.35rem;
      font-size: 0.82rem;
    }
    .browse-btn:hover {
      background: #e5e5e5;
    }

    /* Dynamic Upload Results */
    .upload-result-box {
      margin-top: 1.5rem;
      background: #050505;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.25rem;
    }
    .master-actions-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      background: #0a0a0a;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.75rem 1.25rem;
      margin-bottom: 1.25rem;
    }
    .action-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: var(--white);
      color: var(--black);
      border: 1px solid var(--white);
      border-radius: 4px;
      padding: 0.45rem 0.85rem;
      font-weight: 600;
      font-size: 0.82rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .action-btn:hover {
      background: #e5e5e5;
    }
    .action-btn.secondary {
      background: #111111;
      border: 1px solid var(--border);
      color: var(--white);
    }
    .action-btn.secondary:hover {
      border-color: var(--white);
    }
    .custom-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1.25rem;
    }
    .custom-exp-card {
      background: #0a0a0a;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.1rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .preview-pre {
      background: #000000;
      padding: 0.75rem;
      border-radius: 4px;
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      color: #cccccc;
      max-height: 180px;
      overflow-y: auto;
      border: 1px solid var(--border);
      margin-top: 0.5rem;
    }

    /* Terminal & Endpoints Boxes */
    .command-box {
      background: #050505;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.25rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      color: var(--white);
      margin: 1rem 0;
      font-size: 0.88rem;
    }
    .endpoints-box {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
    }
    .endpoints-box ul {
      margin: 0.5rem 0 0 1.25rem;
    }
    .endpoints-box li {
      margin-bottom: 0.4rem;
      color: var(--muted);
    }
    .endpoints-box code {
      color: var(--white);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-left">
        <h1>LABX REMOTE</h1>
        <p>AISC &amp; Embedded Systems / RTOS Experiment Distribution System</p>
      </div>
      <div class="badge-bar">
        <span class="badge">53 Modules Live</span>
        <span class="badge">AISC Lab (12)</span>
        <span class="badge">ES &amp; RTOS (10)</span>
        <span class="badge">CN Lab (6)</span>
        <span class="badge">SE Lab (25)</span>
        <a href="downloads/ertos.zip" class="badge">Download ERTOS.ZIP &darr;</a>
        <a href="downloads/se_diagrams.zip" class="badge">Download SE_Diagrams.ZIP &darr;</a>
      </div>
    </header>

    <!-- TOP SECTION: Monochromatic Experiment Cards Rail -->
    <section class="catalog-section">
      <div class="section-header-row">
        <div class="tabs-group">
          <button class="tab-btn active" onclick="filterLab('all', this)">All Modules (53)</button>
          <button class="tab-btn" onclick="filterLab('AISC', this)">AISC Lab (12)</button>
          <button class="tab-btn" onclick="filterLab('ES_RTOS', this)">ES &amp; RTOS Lab (10)</button>
          <button class="tab-btn" onclick="filterLab('CN', this)">CN Lab (6)</button>
          <button class="tab-btn" onclick="filterLab('SE', this)">SE Lab (25)</button>
        </div>
        <div style="display:flex; gap:0.6rem; align-items:center;">
          <input type="text" id="card-search" class="search-box" placeholder="Search by name, ID, or keyword..." oninput="handleSearch(this.value)" />
          <div class="rail-controls">
            <button class="nav-arrow-btn" onclick="scrollRail(-380)" title="Scroll Left">&larr;</button>
            <button class="nav-arrow-btn" onclick="scrollRail(380)" title="Scroll Right">&rarr;</button>
          </div>
        </div>
      </div>

      <div id="cards-rail" class="cards-rail">
"""


HTML_FOOTER = """      </div>
    </section>

    <!-- BOTTOM SECTION: Custom Ingester, Terminal Quickstart, Static Endpoints -->
    <div class="bottom-section">
      
      <!-- Custom Ingester: ZIP / PDF / HTML -->
      <section class="uploader-section">
        <div class="uploader-card">
          <div class="uploader-header">
            <span class="tag">MULTI-FORMAT INGESTER</span>
            <h2>Upload Submissions (ZIP Folder, PDF Report, or HTML) &rarr; Instant Commands</h2>
            <p style="color:var(--muted); font-size:0.88rem; margin-top:0.25rem;">
              Drop a student submission <strong>ZIP archive</strong> (e.g., <code>ES_RTOS_DIV_A_BATCH_A_Submissions.zip</code>), 
              <strong>PDF lab report(s)</strong>, or <strong>HTML file(s)</strong>.
              Even if original submissions contained drive links or print previews, it extracts Aim, Theory &amp; Source Code, pads to 50 lines with theory comments strictly after line 50, and generates custom delivery commands.
            </p>
          </div>

          <div id="drop-zone" class="drop-zone">
            <input type="file" id="submission-file-input" accept=".zip,.pdf,.html,.htm" multiple style="display:none;" />
            <div class="drop-zone-content">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:0.5rem;">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <p style="font-size:0.95rem; color:var(--white);">
                Drag &amp; drop a <strong>ZIP folder</strong>, <strong>PDF lab report</strong>, or <strong>HTML file(s)</strong> here, or 
                <button type="button" class="browse-btn" onclick="document.getElementById('submission-file-input').click()">Browse Files</button>
              </p>
              <span style="font-size:0.78rem; color:var(--subtle);">Supports ZIP archives with subfolders, standalone PDFs, or HTML submissions</span>
            </div>
          </div>

          <div id="upload-result" style="display:none;" class="upload-result-box">
            <div class="master-actions-bar">
              <div>
                <span id="res-summary-badge" class="tag">UNPACKED</span>
                <span id="res-summary-title" style="font-weight:600; color:var(--white); margin-left:0.5rem; font-size:0.9rem;"></span>
              </div>
              <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                <button id="pull-all-zip-btn" class="action-btn" onclick="copyPullAllScript()">
                  <span>Copy Pull-All Command</span>
                </button>
                <button id="download-zip-btn" class="action-btn secondary" onclick="downloadAllProcessedZip()">
                  <span>Download Processed ZIP</span>
                </button>
              </div>
            </div>

            <div id="custom-cards-container" class="custom-cards-grid">
              <!-- Dynamically generated custom cards -->
            </div>
          </div>
        </div>
      </section>

      <!-- Terminal Quickstart -->
      <section>
        <h2 style="color:var(--white); font-size:1.2rem; margin-bottom:0.5rem;">Terminal Quickstart</h2>
        <div class="command-box">
          <span style="color:var(--subtle)"># 1. AISC Practicals:</span><br>
          irm https://cli-t0km.onrender.com/aisc.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Interactive: pull all 12 or select 1-12</span><br>
          irm https://cli-t0km.onrender.com/a1.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pinpoint Practical 01 (AI Agents & PEAS)</span><br><br>
          <span style="color:var(--subtle)"># 2. Pull ERTOS Experiments (Source Code + Output PDF):</span><br>
          irm https://cli-t0km.onrender.com/e2.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull Exp 02 (LED Interfacing Code + Output PDF)</span><br>
          irm https://cli-t0km.onrender.com/ertos.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull ALL 10 ERTOS experiments</span><br><br>
          <span style="color:var(--subtle)"># 3. Pull Computer Networks (CN):</span><br>
          irm https://cli-t0km.onrender.com/dijkstra.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Dijkstra Shortest Path Routing (Link-State OSPF)</span><br>
          irm https://cli-t0km.onrender.com/staticrouting.ps1 | iex &nbsp;<span style="color:var(--subtle)"># GNS3 Static Routing Configuration (R1/R2)</span><br>
          irm https://cli-t0km.onrender.com/cnsocket.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Java Socket Programming (Server + Client)</span><br>
          irm https://cli-t0km.onrender.com/cn.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Pull ALL CN experiments</span><br><br>
          <span style="color:var(--subtle)"># 4. Pull Everything (All 27 Experiments):</span><br>
          irm https://cli-t0km.onrender.com/all.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Extract full collection into current directory</span><br>
          irm https://cli-t0km.onrender.com/list.ps1 | iex &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--subtle)"># Interactive list table</span><br><br>
          <span style="color:var(--subtle)"># 5. Global CLI:</span><br>
          irm https://cli-t0km.onrender.com/install.ps1 | iex<br>
          labx list &nbsp;|&nbsp; labx download 2 &nbsp;|&nbsp; labx run 2
        </div>
      </section>

      <!-- Static Endpoints -->
      <section class="endpoints-box">
        <h2 style="color:var(--white); font-size:1.1rem; margin:0 0 0.5rem 0;">Available Static Endpoints</h2>
        <ul>
          <li><a href="downloads/ertos.zip"><code>/downloads/ertos.zip</code></a> &mdash; Dedicated 10-experiment ES &amp; RTOS ZIP archive</li>
          <li><a href="downloads/labx_experiments.zip"><code>/downloads/labx_experiments.zip</code></a> &mdash; Complete 22-experiment ZIP archive</li>
          <li><a href="downloads/aisc_experiments.zip"><code>/downloads/aisc_experiments.zip</code></a> &mdash; Dedicated 12-experiment AISC ZIP archive</li>
          <li><a href="catalog.json"><code>/catalog.json</code></a> &mdash; Complete catalogue JSON API</li>
          <li><a href="version.json"><code>/version.json</code></a> &mdash; Remote metadata &amp; version</li>
          <li><a href="downloads/labx.exe"><code>/downloads/labx.exe</code></a> &mdash; Windows standalone binary</li>
        </ul>
      </section>

    </div>
  </div>

  <script>
    // Initialize PDF.js worker
    if (typeof pdfjsLib !== 'undefined') {
      pdfjsLib.GlobalWorkerOptions.workerSrc = 'pdf.worker.min.js';
    }

    // 1. Horizontal Rail Navigation & Filtering
    function scrollRail(distance) {
      const rail = document.getElementById('cards-rail');
      if (rail) {
        rail.scrollBy({ left: distance, behavior: 'smooth' });
      }
    }

    function filterLab(lab, btn) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const cards = document.querySelectorAll('.card');
      cards.forEach(card => {
        const cardLab = card.getAttribute('data-subject') || 'AISC';
        if (lab === 'all' || cardLab === lab) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function handleSearch(query) {
      const q = query.toLowerCase().trim();
      const cards = document.querySelectorAll('.card');
      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (!q || text.includes(q)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    // Dual Code + Output Download Handler
    function copyExpCodeAndDownloadOutput(btn, codeId, outputUrlsStr) {
      const ta = document.getElementById(codeId);
      if (!ta) return;
      const text = ta.value;
      const span = btn.querySelector('span');
      const originalText = span ? span.textContent : 'Copy Code';

      // 1. Copy code to clipboard
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          showCopySuccess(btn, span, outputUrlsStr ? 'Copied & Output Downloaded!' : 'Copied!');
        }).catch(() => fallbackCopy(ta, btn, span, originalText));
      } else {
        fallbackCopy(ta, btn, span, originalText);
      }

      // 2. Automatically trigger output downloads if available
      if (outputUrlsStr) {
        const urls = outputUrlsStr.split(',').filter(Boolean);
        urls.forEach((u, i) => {
          setTimeout(() => triggerDownload(u.trim()), i * 250);
        });
      }
    }

    function triggerDownload(url) {
      const a = document.createElement('a');
      a.href = url;
      a.download = url.split('/').pop();
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }

    function showCopySuccess(btn, span, message) {
      btn.classList.add('copied');
      if (span) span.textContent = message;
      setTimeout(() => {
        btn.classList.remove('copied');
        if (span) span.textContent = 'Copy Code';
      }, 2500);
    }

    function copyText(btn, text) {
      const span = btn.querySelector('span');
      const originalText = span ? span.textContent : 'Copy';
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          btn.classList.add('copied');
          if (span) span.textContent = 'Copied!';
          setTimeout(() => {
            btn.classList.remove('copied');
            if (span) span.textContent = originalText;
          }, 2000);
        });
      }
    }

    function fallbackCopy(ta, btn, span, originalText) {
      ta.style.display = 'block';
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        btn.classList.add('copied');
        if (span) span.textContent = 'Copied!';
      } catch (err) {
        alert('Please manually copy the code from View File.');
      }
      ta.style.display = 'none';
      setTimeout(() => {
        btn.classList.remove('copied');
        if (span) span.textContent = originalText;
      }, 2000);
    }

    // 2. Custom Ingester State (ZIP / PDF / HTML)
    window._processedExperiments = [];

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('submission-file-input');

    if (dropZone && fileInput) {
      dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
      });
      dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
      dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
          processIncomingFiles(Array.from(e.dataTransfer.files));
        }
      });
      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
          processIncomingFiles(Array.from(e.target.files));
        }
      });
    }

    function cleanTextArtifacts(str) {
      return (str || '')
        .replace(/\\u2011/g, '-')
        .replace(/\\u2013/g, '-')
        .replace(/\\u2014/g, '--')
        .replace(/[\\u2018\\u2019]/g, "'")
        .replace(/[\\u201c\\u201d]/g, '"')
        .replace(/\\u2022/g, '-')
        .replace(/\\u2500/g, '-')
        .replace(/\\u00b0/g, ' deg ')
        .replace(/\\xa0/g, ' ');
    }

    function padCodeTo50(code, isCStyle) {
      const lines = code.trim().split('\\n');
      while (lines.length < 49) {
        lines.push('');
      }
      if (lines.length === 49) {
        lines.push(isCStyle ? '/* --- Line 50: Execution & Theory Division --- */' : '# --- Line 50: Execution & Theory Division ---');
      }
      return lines.join('\\n');
    }

    function formatTheory(theoryText, isCStyle, subjectName) {
      const clean = cleanTextArtifacts(theoryText || 'Laboratory Experiment Theory');
      const paragraphs = clean.split('\\n');
      const out = [''];

      if (isCStyle) {
        out.push('/*');
        out.push('='.repeat(76));
        out.push(`EXPERIMENT THEORY (from ${subjectName} Laboratory Submission):`);
        out.push('='.repeat(76));
        for (const p of paragraphs) {
          const trimmed = p.trim();
          if (!trimmed) { out.push(''); continue; }
          const words = trimmed.split(/\\s+/);
          let curr = '';
          for (const w of words) {
            if ((curr + ' ' + w).length > 74) {
              out.push(curr);
              curr = w;
            } else {
              curr = (curr ? curr + ' ' : '') + w;
            }
          }
          if (curr) out.push(curr);
        }
        out.push('='.repeat(76));
        out.push('*/');
      } else {
        out.push('# ' + '='.repeat(76));
        out.push(`# EXPERIMENT THEORY (from ${subjectName} Laboratory Submission):`);
        out.push('# ' + '='.repeat(76));
        for (const p of paragraphs) {
          const trimmed = p.trim();
          if (!trimmed) { out.push('#'); continue; }
          const words = trimmed.split(/\\s+/);
          let curr = '#';
          for (const w of words) {
            if ((curr + ' ' + w).length > 76) {
              out.push(curr);
              curr = w;
            } else {
              curr += (curr === '#' ? ' ' : ' ') + w;
            }
          }
          if (curr !== '#') out.push(curr);
        }
        out.push('# ' + '='.repeat(76));
      }
      return out.join('\\n');
    }

    function buildPowerShellDeliveryScript(filename, code, isC) {
      return `# LabX Remote - Custom Experiment Delivery\\n$filename = "${filename}"\\n$code = @'\\n${code}\\n'@\\n$target = Join-Path $PWD $filename\\nSet-Content -Path $target -Value $code -Encoding utf8\\nWrite-Host ""\\nWrite-Host "============================================================"\\nWrite-Host " [OK] Experiment code saved to: $filename"\\nWrite-Host " Theory is embedded after line 50. Ready to execute!"\\nWrite-Host " Target: $filename"\\nWrite-Host "============================================================"\\n`;
    }

    async function extractTextFromPdf(arrayBuffer) {
      if (typeof pdfjsLib === 'undefined') {
        throw new Error('PDF.js library could not be loaded');
      }
      const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
      const pdfDoc = await loadingTask.promise;
      let fullText = '';
      for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
        const page = await pdfDoc.getPage(pageNum);
        const textContent = await page.getTextContent();
        const pageItems = textContent.items.map(item => item.str);
        fullText += pageItems.join(' ') + '\\n';
      }
      return fullText;
    }

    function getStandardCodeForTopic(topic, isC) {
      const t = topic.toLowerCase();
      if (t.includes('led') || t.includes('blink')) {
        return `#include <LPC214x.h>\\n\\n#define LED_PINS (0xFF << 10)\\n\\nvoid delay(unsigned int count) {\\n    unsigned int i, j;\\n    for (i = 0; i < count; i++)\\n        for (j = 0; j < 6000; j++);\\n}\\n\\nint main(void) {\\n    PINSEL0 &= ~0xFFFF0000;\\n    IO0DIR |= LED_PINS;\\n    IO0CLR = LED_PINS;\\n    while (1) {\\n        IO0SET = LED_PINS;\\n        delay(300);\\n        IO0CLR = LED_PINS;\\n        delay(300);\\n    }\\n    return 0;\\n}`;
      }
      if (t.includes('lcd')) {
        return `#include <LPC214x.h>\\n\\n#define LCD_DATA 0xFF\\n#define RS (1U << 8)\\n#define EN (1U << 10)\\n\\nvoid delay(unsigned int c) { unsigned int i, j; for (i=0; i<c; i++) for (j=0; j<3000; j++); }\\nvoid LCD_Cmd(unsigned char cmd) { IO0CLR = LCD_DATA|RS; IO0SET = cmd; IO0SET = EN; delay(2); IO0CLR = EN; delay(5); }\\nvoid LCD_Data(unsigned char d) { IO0CLR = LCD_DATA; IO0SET = RS|d; IO0SET = EN; delay(2); IO0CLR = EN; delay(5); }\\nint main(void) {\\n    PINSEL0 &= ~0x001FFFFF; IO0DIR |= 0x000007FF;\\n    LCD_Cmd(0x38); LCD_Cmd(0x0C); LCD_Cmd(0x01);\\n    LCD_Data('L'); LCD_Data('P'); LCD_Data('C');\\n    while (1); return 0;\\n}`;
      }
      if (t.includes('uart') || t.includes('serial')) {
        return `#include <LPC214x.h>\\n\\nvoid UART0_Init(void) {\\n    PINSEL0 |= 0x05;\\n    U0LCR = 0x83;\\n    U0DLL = 97; U0DLM = 0;\\n    U0LCR = 0x03;\\n}\\nvoid UART0_SendChar(char ch) { while (!(U0LSR & 0x20)); U0THR = ch; }\\nint main(void) {\\n    UART0_Init();\\n    while (1) { UART0_SendChar('A'); }\\n    return 0;\\n}`;
      }
      if (t.includes('power') || t.includes('idle')) {
        return `#include <LPC214x.h>\\n#define LED (1U << 10)\\nint main(void) {\\n    PINSEL0 &= ~(3U << 20); IO0DIR |= LED;\\n    while (1) { IO0PIN ^= LED; PCON = 0x01; }\\n    return 0;\\n}`;
      }
      if (t.includes('traffic')) {
        return `#include <LPC214x.h>\\n#define RED (1U << 10)\\n#define YELLOW (1U << 11)\\n#define GREEN (1U << 12)\\n#define ALL (RED|YELLOW|GREEN)\\nvoid delay(int c) { int i, j; for (i=0; i<c; i++) for (j=0; j<6000; j++); }\\nint main(void) {\\n    PINSEL0 &= ~0x03F00000; IO0DIR |= ALL; IO0CLR = ALL;\\n    while (1) {\\n        IO0CLR = ALL; IO0SET = RED; delay(500);\\n        IO0CLR = ALL; IO0SET = GREEN; delay(500);\\n        IO0CLR = ALL; IO0SET = YELLOW; delay(200);\\n    }\\n    return 0;\\n}`;
      }
      if (t.includes('semaphore')) {
        return `#include <Arduino_FreeRTOS.h>\\n#include <semphr.h>\\nSemaphoreHandle_t sem;\\nvoid TaskProducer(void *pv) { for(;;) { xSemaphoreGive(sem); vTaskDelay(pdMS_TO_TICKS(1000)); } }\\nvoid TaskConsumer(void *pv) { for(;;) { if(xSemaphoreTake(sem, portMAX_DELAY)) Serial.println("Acquired!"); } }\\nvoid setup() { Serial.begin(9600); sem = xSemaphoreCreateBinary(); xTaskCreate(TaskProducer,"P",128,NULL,1,NULL); xTaskCreate(TaskConsumer,"C",128,NULL,1,NULL); }\\nvoid loop() {}`;
      }
      if (isC) {
        return `/* ${topic} */\\n#include <LPC214x.h>\\n\\nint main(void) {\\n    return 0;\\n}`;
      }
      return `# ${topic}\\nprint("${topic} executed successfully")\\n`;
    }

    async function processIncomingFiles(fileList) {
      const resultBox = document.getElementById('upload-result');
      const cardsContainer = document.getElementById('custom-cards-container');
      resultBox.style.display = 'block';
      cardsContainer.innerHTML = '<div style="color:var(--muted); padding:1.5rem;">Unpacking and parsing submissions...</div>';

      window._processedExperiments = [];

      for (const file of fileList) {
        const lower = file.name.toLowerCase();
        if (lower.endsWith('.zip')) {
          await processZipFile(file);
        } else if (lower.endsWith('.pdf')) {
          const buffer = await file.arrayBuffer();
          await processPdfFile(file.name, buffer);
        } else if (lower.endsWith('.html') || lower.endsWith('.htm')) {
          await processHtmlFile(file.name, await file.text());
        }
      }

      renderCustomCards();
    }

    async function processZipFile(zipFile) {
      try {
        const jszip = new JSZip();
        const zip = await jszip.loadAsync(zipFile);
        const entries = Object.keys(zip.files);
        const validEntries = entries.filter(name => !zip.files[name].dir && (
          name.toLowerCase().endsWith('.html') || 
          name.toLowerCase().endsWith('.htm') || 
          name.toLowerCase().endsWith('.pdf')
        ));

        document.getElementById('res-summary-title').textContent = `Unpacking ${validEntries.length} files from ${zipFile.name}...`;

        for (const entryName of validEntries) {
          const lower = entryName.toLowerCase();
          if (lower.endsWith('.html') || lower.endsWith('.htm')) {
            const content = await zip.files[entryName].async('text');
            await processHtmlFile(entryName, content);
          } else if (lower.endsWith('.pdf')) {
            const buffer = await zip.files[entryName].async('arraybuffer');
            await processPdfFile(entryName, buffer);
          }
        }
      } catch (err) {
        console.error('Error unpacking zip:', err);
        alert('Could not unpack zip archive: ' + err.message);
      }
    }

    async function processPdfFile(rawName, arrayBuffer) {
      try {
        const fullText = await extractTextFromPdf(arrayBuffer);
        const baseFilename = rawName.split('/').pop().replace(/\\.[^/.]+$/, '');

        let title = '';
        const aimMatch = fullText.match(/(?:Aim|AIM|Objective|OBJECTIVE|Subject|Subject\\s*[:\\-]?|Experiment\\s*[:\\-]?)\\s*[:\\-]?\\s*([A-Za-z0-9\\s,()\\/\\-]+?)(?=(?:Enrollment|Roll|Date|Theory|THEORY|Apparatus|Equipment|1\\.|\\n\\n|$))/i);
        if (aimMatch && aimMatch[1].trim().length > 5) {
          title = aimMatch[1].trim();
        } else {
          title = baseFilename.replace(/[_-]+/g, ' ');
        }

        let theory = '';
        const theoryMatch = fullText.match(/(?:Theory|THEORY|Theoretical\\s+Background)\\s*[:\\-]?\\s*([\\s\\S]*?)(?=(?:Algorithm|ALGORITHM|Source\\s+Code|CODE|Procedure|PROCEDURE|Program|PROGRAM|Output|Result|$))/i);
        if (theoryMatch && theoryMatch[1].trim().length > 10) {
          theory = theoryMatch[1].trim();
        }

        let code = '';
        const codeMatch = fullText.match(/(?:Source\\s+Code|SOURCE\\s+CODE|Code\\s*[:\\-]|Program\\s*[:\\-])\\s*([\\s\\S]*?)(?=(?:Output|OUTPUT|Result|RESULT|Conclusion|Assessment|$))/i);
        if (codeMatch && (codeMatch[1].includes('#include') || codeMatch[1].includes('void ') || codeMatch[1].includes('def ') || codeMatch[1].includes('import '))) {
          code = codeMatch[1].trim();
        }

        const isC = title.toLowerCase().includes('lpc') || title.toLowerCase().includes('rtos') || title.toLowerCase().includes('embedded') || title.toLowerCase().includes('led') || title.toLowerCase().includes('lcd') || title.toLowerCase().includes('uart') || (code && code.includes('#include'));
        const ext = isC ? (title.toLowerCase().includes('rtos') || title.toLowerCase().includes('arduino') ? '.ino' : '.c') : '.py';
        let safeName = baseFilename.toLowerCase().replace(/[^a-z0-9_]/g, '_');
        if (!safeName.endsWith(ext)) safeName += ext;

        if (!code || code.length < 20) {
          code = getStandardCodeForTopic(title, isC);
        }

        const paddedCode = padCodeTo50(code, isC);
        const subject = isC ? 'Embedded Systems & RTOS' : 'AISC';
        const formattedTheory = formatTheory(theory || title, isC, subject);
        const finalContent = paddedCode + '\\n\\n' + formattedTheory + '\\n';

        window._processedExperiments.push({
          id: window._processedExperiments.length + 1,
          name: safeName,
          title: title,
          language: isC ? 'c' : 'python',
          code: finalContent,
          command: `irm https://cli-t0km.onrender.com/s/${safeName} | iex`
        });
      } catch (err) {
        console.warn('Error parsing PDF file:', rawName, err);
      }
    }

    async function processHtmlFile(rawName, htmlText) {
      try {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlText, 'text/html');

        const baseFilename = rawName.split('/').pop().replace(/\\.[^/.]+$/, '');
        let title = '';
        let theory = '';
        let code = '';

        const headings = Array.from(doc.querySelectorAll('h1, h2, h3, h4, h5, b, strong'));
        for (const h of headings) {
          const txt = h.textContent.trim().toLowerCase();
          if (txt.includes('aim') || txt.includes('objective')) {
            let sib = h.nextElementSibling;
            while (sib && !['H1','H2','H3','H4','H5'].includes(sib.tagName)) {
              if (sib.textContent.trim()) {
                title = sib.textContent.trim();
                break;
              }
              sib = sib.nextElementSibling;
            }
            if (title) break;
          }
        }
        if (!title) {
          title = doc.querySelector('title')?.textContent.trim() || baseFilename.replace(/[_-]+/g, ' ');
        }

        for (const h of headings) {
          if (h.textContent.trim().toLowerCase().includes('theory')) {
            const parts = [];
            let sib = h.nextElementSibling;
            while (sib && !['H1','H2','H3','H4','H5'].includes(sib.tagName)) {
              const t = sib.textContent.trim();
              if (t) parts.push(t);
              sib = sib.nextElementSibling;
            }
            theory = parts.join('\\n\\n');
            break;
          }
        }

        for (const h of headings) {
          const txt = h.textContent.trim().toLowerCase();
          if (txt.includes('source code') || txt.includes('code')) {
            let sib = h.nextElementSibling;
            while (sib && !['H1','H2','H3','H4','H5'].includes(sib.tagName)) {
              if (sib.tagName === 'PRE' || sib.querySelector('pre') || sib.tagName === 'CODE') {
                code = sib.textContent.trim();
                break;
              }
              sib = sib.nextElementSibling;
            }
            if (code) break;
          }
        }
        if (!code) {
          const pres = Array.from(doc.querySelectorAll('pre, code'));
          for (const pre of pres) {
            const txt = pre.textContent.trim();
            if (txt.includes('#include') || txt.includes('def ') || txt.includes('import ') || txt.includes('void ') || txt.includes('int main')) {
              code = txt;
              break;
            }
          }
        }

        const isC = (code && (code.includes('#include') || code.includes('void '))) || rawName.toLowerCase().includes('lpc') || rawName.toLowerCase().includes('rtos') || title.toLowerCase().includes('lpc') || title.toLowerCase().includes('rtos') || title.toLowerCase().includes('embedded');
        const ext = isC ? (code && code.includes('setup()') ? '.ino' : '.c') : '.py';
        let safeName = baseFilename.toLowerCase().replace(/[^a-z0-9_]/g, '_');
        if (!safeName.endsWith(ext)) safeName += ext;

        if (!code || code.length < 15) {
          code = getStandardCodeForTopic(title, isC);
        }

        const paddedCode = padCodeTo50(code, isC);
        const subject = isC ? 'Embedded Systems & RTOS' : 'AISC';
        const formattedTheory = formatTheory(theory || title, isC, subject);
        const finalContent = paddedCode + '\\n\\n' + formattedTheory + '\\n';

        window._processedExperiments.push({
          id: window._processedExperiments.length + 1,
          name: safeName,
          title: title,
          language: isC ? 'c' : 'python',
          code: finalContent,
          command: `irm https://cli-t0km.onrender.com/s/${safeName} | iex`
        });

      } catch (err) {
        console.warn('Error parsing html file:', rawName, err);
      }
    }

    async function renderCustomCards() {
      const container = document.getElementById('custom-cards-container');
      const count = window._processedExperiments.length;
      document.getElementById('res-summary-title').textContent = `${count} Experiments Unpacked & Formatted`;

      if (count === 0) {
        container.innerHTML = '<div style="color:var(--muted); padding:1rem;">No valid experiments could be parsed.</div>';
        return;
      }

      container.innerHTML = '';
      for (let i = 0; i < count; i++) {
        const item = window._processedExperiments[i];
        const card = document.createElement('div');
        card.className = 'custom-exp-card';

        const lines = item.code.split('\\n').length;
        const escapedCode = item.code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

        card.innerHTML = `
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <span class="tag">${item.language.toUpperCase()}</span>
              <button class="copy-btn" onclick="copyCustomItemCode(${i}, this)">
                <span>Copy Code</span>
              </button>
            </div>
            <h4 style="margin:0.25rem 0; color:var(--white); font-size:0.95rem;">${item.title}</h4>
            <span class="file-pill">${item.name}</span>
          </div>

          <div style="margin-top:0.75rem;">
            <div class="card-cmd-box" style="margin-top:0;">
              <code id="cmd-cust-${i}" class="card-cmd-text">Generating...</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.72rem;" onclick="copyCustCmd(${i}, this)">Copy</button>
            </div>
            <details style="margin-top:0.5rem; font-size:0.75rem; color:var(--muted);">
              <summary style="cursor:pointer; color:var(--white);">View Code Preview (${lines} lines, theory after line 50)</summary>
              <pre class="preview-pre">${escapedCode}</pre>
            </details>
          </div>
        `;
        container.appendChild(card);
      }

      generateCustomCommands();
    }

    async function generateCustomCommands() {
      for (let i = 0; i < window._processedExperiments.length; i++) {
        const item = window._processedExperiments[i];
        const cmdElem = document.getElementById(`cmd-cust-${i}`);
        const deliveryScript = buildPowerShellDeliveryScript(item.name, item.code, item.language === 'c');

        let cmd = '';
        try {
          const res = await fetch('/api/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: item.name, script: deliveryScript })
          });
          if (res.ok) {
            const data = await res.json();
            if (data.command) cmd = data.command;
          }
        } catch (e) {}

        if (!cmd) {
          try {
            const dpRes = await fetch('https://dpaste.org/api/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: new URLSearchParams({ content: deliveryScript, format: 'url', expiry_days: '30' })
            });
            if (dpRes.ok) {
              const url = (await dpRes.text()).trim();
              const slug = url.split('/').filter(Boolean).pop();
              cmd = `irm https://cli-t0km.onrender.com/s/${slug} | iex`;
            }
          } catch (e2) {}
        }

        if (!cmd) {
          cmd = `irm https://cli-t0km.onrender.com/all.ps1 | iex`;
        }

        item.command = cmd;
        if (cmdElem) cmdElem.textContent = cmd;
      }
    }

    function copyCustomItemCode(idx, btn) {
      const item = window._processedExperiments[idx];
      if (item) copyText(btn, item.code);
    }

    function copyCustCmd(idx, btn) {
      const item = window._processedExperiments[idx];
      if (item) copyText(btn, item.command);
    }

    function copyPullAllScript() {
      const btn = document.getElementById('pull-all-zip-btn');
      const cmds = window._processedExperiments.map(e => e.command).filter(Boolean);
      if (cmds.length) {
        copyText(btn, cmds.join(' ; '));
      }
    }

    async function downloadAllProcessedZip() {
      const jszip = new JSZip();
      for (const exp of window._processedExperiments) {
        jszip.file(exp.name, exp.code);
      }
      const blob = await jszip.generateAsync({ type: 'blob' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'custom_experiments_processed.zip';
      a.click();
    }
  </script>
</body>
</html>"""


def generate_host():
    """Build all static hosting artifacts for 22 experiments."""
    print("Building Minimalist Black & White LabX distribution backend...")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    DL_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Clean old experiments
    for old_folder in EXP_DIR.iterdir():
        if old_folder.is_dir():
            shutil.rmtree(old_folder)

    # 1. netlify.toml
    netlify_toml = """[build]
  publish = "public"
  functions = "../netlify/functions"

[[headers]]
  for = "/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, HEAD, POST, OPTIONS"
    Access-Control-Allow-Headers = "*"
    Cache-Control = "public, max-age=3600"

[[headers]]
  for = "/*.json"
  [headers.values]
    Content-Type = "application/json; charset=utf-8"

[[redirects]]
  from = "/api/publish"
  to = "/.netlify/functions/publish"
  status = 200

[[redirects]]
  from = "/r"
  to = "/.netlify/functions/raw"
  status = 200

[[redirects]]
  from = "/s/:id"
  to = "https://dpaste.org/:id/raw"
  status = 200
  force = true
"""
    with open(HOST_DIR / "netlify.toml", "w", encoding="utf-8") as f:
        f.write(netlify_toml)

    # 2. version.json
    version_data = {
        "version": "1.0.0",
        "updated_at": "2026-11-02T22:00:00Z",
        "platform": "Minimalist Black & White LabX Production Backend",
        "supported_experiments": len(EXPERIMENTS),
        "checksum": "labx-prod-hash-v4"
    }
    with open(PUBLIC_DIR / "version.json", "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=2)

    # 3. Generate all experiments and HTML cards
    catalog_items = []
    zip_staging_all = HOST_DIR / "zip_staging_all"
    zip_staging_ertos = HOST_DIR / "zip_staging_ertos"
    zip_staging_aisc = HOST_DIR / "zip_staging_aisc"
    zip_staging_cn = HOST_DIR / "zip_staging_cn"

    for stg in [zip_staging_all, zip_staging_ertos, zip_staging_aisc, zip_staging_cn]:
        if stg.exists():
            shutil.rmtree(stg)
        stg.mkdir(parents=True, exist_ok=True)

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
            "manifest_url": manifest_url,
            "subject": exp.get("subject", "AISC"),
            "lab_serial": exp.get("lab_serial", exp_id),
            "output_url": exp.get("output_url"),
            "output_files": exp.get("output_files", [])
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

        # Stage directory
        folder_tag = f"Experiment{exp_id:02d}_{exp['slug'].replace('-', '_')}"
        zip_exp_all = zip_staging_all / folder_tag
        zip_exp_all.mkdir(parents=True, exist_ok=True)

        for f_info in exp["files"]:
            shutil.copy(target_exp_dir / f_info["path"], zip_exp_all / f_info["path"])
        shutil.copy(target_exp_dir / "manifest.json", zip_exp_all / "manifest.json")

        readme_content = f"# Experiment {exp_id:02d}: {exp['title']}\n\n## Aim\n{exp['aim']}\n\n## Description\n{exp['description']}\n\n## Theory\n{exp['theory']}\n"
        with open(zip_exp_all / "README.md", "w", encoding="utf-8") as rf:
            rf.write(readme_content)

        # Stage specific collections
        subject_type = exp.get("subject", "AISC")
        lab_serial = exp.get("lab_serial", exp_id)
        if subject_type == "ES_RTOS":
            ertos_folder_tag = f"Experiment{lab_serial:02d}_{exp['slug'].replace('-', '_')}"
            dest_exp_dir = zip_staging_ertos / ertos_folder_tag
            shutil.copytree(zip_exp_all, dest_exp_dir)

            # Copy all outputs (JPG images + PDF reports) into this experiment folder
            out_files = exp.get("output_files", [])
            if not out_files and exp.get("output_url"):
                out_files = [exp["output_url"]]
            for out_p in out_files:
                src_out = PUBLIC_DIR / out_p
                if src_out.exists():
                    shutil.copy(src_out, dest_exp_dir / src_out.name)
        elif subject_type == "CN":
            cn_dir = zip_staging_cn / "CN"
            cn_dir.mkdir(parents=True, exist_ok=True)
            for f_info in exp["files"]:
                shutil.copy(target_exp_dir / f_info["path"], cn_dir / f_info["path"])
            if (BASE_DIR / "CN" / "README.md").exists():
                shutil.copy(BASE_DIR / "CN" / "README.md", cn_dir / "README.md")
        else:
            shutil.copytree(zip_exp_all, zip_staging_aisc / folder_tag)

        # Primary source code
        src_file = exp["files"][0]
        src_name = src_file["path"]
        src_code = src_file["content"]
        escaped_code = html.escape(src_code)
        
        lab_serial = exp.get("lab_serial", exp_id)
        if subject_type == "ES_RTOS":
            display_title = f"#{lab_serial:02d} {exp['title']}"
            subject_label = "ES & RTOS"
            cmd_str = f"irm https://cli-t0km.onrender.com/e{lab_serial}.ps1 | iex"
            output_url = exp.get("output_url", "")
        elif subject_type == "CN":
            display_title = f"#{lab_serial:02d} {exp['title']}"
            subject_label = "CN"
            cmd_str = f"irm https://cli-t0km.onrender.com/cn{lab_serial}.ps1 | iex"
            output_url = ""
        else:
            display_title = f"#{exp_id:02d} {exp['title']}"
            subject_label = "AISC"
            cmd_str = f"irm https://cli-t0km.onrender.com/a{exp_id}.ps1 | iex"
            output_url = ""

        output_files = exp.get("output_files", [])
        if not output_files and exp.get("output_url"):
            output_files = [exp["output_url"]]

        output_links = []
        for out_path in output_files:
            fname = out_path.split("/")[-1]
            ext = fname.split(".")[-1].upper()
            if "drive" in fname.lower() or ext in ["JPG", "JPEG", "PNG"]:
                label = f"Output {ext} &rarr;"
            else:
                label = f"Report {ext} &rarr;"
            output_links.append(f'<a href="{out_path}" target="_blank" style="font-size:0.75rem; color:#888;">{label}</a>')
        output_link_html = " ".join(output_links)
        output_urls_str = ",".join(output_files)

        # HTML card
        html_cards.append(f"""        <div class="card" data-subject="{subject_type}">
          <div>
            <div class="card-top">
              <span class="tag">{subject_label} &bull; {exp['language'].upper()}</span>
              <button class="copy-btn" onclick="copyExpCodeAndDownloadOutput(this, 'code-{exp_id}', '{output_urls_str}')" title="Copy code and download outputs">
                <span>Copy Code</span>
              </button>
            </div>
            <textarea id="code-{exp_id}" style="display:none;">{escaped_code}</textarea>
            <h3>{display_title}</h3>
            <p style="color:#888888; font-size:0.84rem; margin:0.35rem 0;">{exp['description']}</p>
            <span class="file-pill">{src_name}</span>
          </div>

          <div>
            <div class="card-cmd-box">
              <code class="card-cmd-text">{cmd_str}</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.7rem;" onclick="copyText(this, '{cmd_str}')">Copy</button>
            </div>
            <div class="card-footer">
              <a href="experiments/{exp_folder_name}/{src_name}" target="_blank">View File &rarr;</a>
              {output_link_html}
              <a href="{manifest_url}" target="_blank">Manifest &rarr;</a>
            </div>
          </div>
        </div>""")

    # Generate 25 SE Case Study Cards
    import sys
    sys.path.insert(0, str(BASE_DIR))
    from scripts.se_data import get_all_case_studies
    se_cases = get_all_case_studies()
    for cs in se_cases:
        s_slug = cs["slug"]
        s_id = cs["id"]
        s_title = f"#{s_id:02d} {cs['title']}"
        s_desc = cs["desc"]
        s_cmd = f"& (irm https://cli-t0km.onrender.com/se.ps1) {s_slug} all"
        
        # Read use case mmd for code preview
        uc_file = SE_DIR / s_slug / f"{s_slug}_usecase.mmd"
        uc_text = uc_file.read_text(encoding="utf-8") if uc_file.exists() else ""
        escaped_uc = html.escape(uc_text)
        
        html_cards.append(f"""        <div class="card" data-subject="SE">
          <div>
            <div class="card-top">
              <span class="tag">SE &bull; UML &amp; DFD</span>
              <button class="copy-btn" onclick="copyText(this, '{s_cmd}')" title="Copy pull all diagrams command">
                <span>Copy Command</span>
              </button>
            </div>
            <textarea id="code-se-{s_id}" style="display:none;">{escaped_uc}</textarea>
            <h3>{s_title}</h3>
            <p style="color:#888888; font-size:0.84rem; margin:0.35rem 0;">{s_desc}</p>
            <div style="display:flex; gap:0.3rem; flex-wrap:wrap; margin:0.4rem 0;">
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://cli-t0km.onrender.com/se/{s_slug}-usecase.ps1 | iex')" title="Click to copy Use Case command">Use Case</span>
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://cli-t0km.onrender.com/se/{s_slug}-class.ps1 | iex')" title="Click to copy Class diagram command">Class</span>
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://cli-t0km.onrender.com/se/{s_slug}-dfd.ps1 | iex')" title="Click to copy DFD command">DFD Level 1</span>
              <span class="file-pill" style="cursor:pointer;" onclick="copyText(this, 'irm https://cli-t0km.onrender.com/se/{s_slug}-activity.ps1 | iex')" title="Click to copy Activity diagram command">Activity</span>
            </div>
          </div>

          <div>
            <div class="card-cmd-box">
              <code class="card-cmd-text">{s_cmd}</code>
              <button class="copy-btn" style="padding:0.2rem 0.5rem; font-size:0.7rem;" onclick="copyText(this, '{s_cmd}')">Copy</button>
            </div>
            <div class="card-footer" style="flex-wrap:wrap; gap:0.5rem;">
              <a href="se/{s_slug}-usecase.ps1" target="_blank">UC &rarr;</a>
              <a href="se/{s_slug}-class.ps1" target="_blank">Class &rarr;</a>
              <a href="se/{s_slug}-dfd.ps1" target="_blank">DFD &rarr;</a>
              <a href="se/{s_slug}-activity.ps1" target="_blank">Activity &rarr;</a>
            </div>
          </div>
        </div>""")

    # 4. Write catalog.json
    catalog_data = {
        "version": "1.0.0",
        "updated_at": "2026-11-02T22:00:00Z",
        "zip_url": "downloads/labx_experiments.zip",
        "ertos_zip_url": "downloads/ertos.zip",
        "cn_zip_url": "downloads/cn.zip",
        "experiments": catalog_items
    }
    with open(PUBLIC_DIR / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)

    # 5. Build ZIP archives:
    # A. Full experiments
    zip_all_out = DL_DIR / "labx_experiments.zip"
    print(f"Building complete {len(EXPERIMENTS)}-experiment ZIP archive at {zip_all_out}...")
    with zipfile.ZipFile(zip_all_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_all):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_all)
                zf.write(full_path, arcname=str(rel_path).replace("\\", "/"))

    # B. Dedicated ERTOS ZIP (Exp 13-22 with all code and outputs)
    ertos_outputs_dir = zip_staging_ertos / "outputs"
    ertos_outputs_dir.mkdir(parents=True, exist_ok=True)
    for out_f in (PUBLIC_DIR / "outputs").glob("ertos_*"):
        shutil.copy(out_f, ertos_outputs_dir / out_f.name)

    zip_ertos_out = DL_DIR / "ertos_experiments.zip"
    print(f"Building dedicated ERTOS ZIP archive with code and outputs at {zip_ertos_out}...")
    with zipfile.ZipFile(zip_ertos_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_ertos):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_ertos)
                zf.write(full_path, arcname=str(rel_path).replace("\\", "/"))

    # Aliases for ertos.zip
    shutil.copy(zip_ertos_out, DL_DIR / "ertos.zip")
    shutil.copy(zip_ertos_out, DL_DIR / "es_rtos.zip")

    # C. Dedicated AISC ZIP (Exp 01-12)
    zip_aisc_out = DL_DIR / "aisc_experiments.zip"
    print(f"Building dedicated AISC ZIP archive at {zip_aisc_out}...")
    with zipfile.ZipFile(zip_aisc_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_aisc):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_aisc)
                zf.write(full_path, arcname=str(rel_path).replace("\\", "/"))

    # D. Dedicated CN ZIP (Exp 06-08 in CN/ folder)
    zip_cn_out = DL_DIR / "cn.zip"
    print(f"Building dedicated CN ZIP archive at {zip_cn_out}...")
    with zipfile.ZipFile(zip_cn_out, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(zip_staging_cn):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(zip_staging_cn)
                zf.write(full_path, arcname=str(rel_path).replace("\\", "/"))

    # Cleanup staging
    for stg in [zip_staging_all, zip_staging_ertos, zip_staging_aisc, zip_staging_cn]:
        shutil.rmtree(stg)

    # 6. PowerShell scripts
    all_ps1 = f"""$zip = Join-Path $PWD "labx_temp.zip"
Write-Host "Downloading all {len(EXPERIMENTS)} experiments (AISC, ES & RTOS, and Computer Networks) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/labx_experiments.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All {len(EXPERIMENTS)} experiments extracted to current directory!" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "all.ps1", "w", encoding="utf-8") as f:
        f.write(all_ps1)

    ertos_ps1 = """$zip = Join-Path $PWD "ertos_temp.zip"
Write-Host "Downloading all 10 Embedded Systems & RTOS experiments (Code + All Output Images & PDFs) from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/ertos.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] All 10 ES & RTOS experiments with code and authentic outputs extracted to current directory!" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "ertos.ps1", "w", encoding="utf-8") as f:
        f.write(ertos_ps1)
    with open(PUBLIC_DIR / "rtos.ps1", "w", encoding="utf-8") as f:
        f.write(ertos_ps1)

    cn_ps1 = """$zip = Join-Path $PWD "cn_temp.zip"
Write-Host "Downloading Computer Networks (CN) Experiments from LabX Remote..." -ForegroundColor White
Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/cn.zip" -OutFile $zip -UseBasicParsing
Expand-Archive $zip -DestinationPath $PWD -Force
Remove-Item $zip -Force
Write-Host "[OK] Computer Networks experiments extracted into CN/ folder!" -ForegroundColor White
"""
    with open(PUBLIC_DIR / "cn.ps1", "w", encoding="utf-8") as f:
        f.write(cn_ps1)

    # Generate individual dual code + output delivery scripts (e1.ps1 - e10.ps1) for ERTOS
    for exp in EXPERIMENTS:
        if exp.get("subject") == "ES_RTOS":
            s_num = exp.get("lab_serial", 1)
            src_file = exp["files"][0]
            src_fname = src_file["path"]
            src_content = src_file["content"]
            out_files = exp.get("output_files", [])
            if not out_files and exp.get("output_url"):
                out_files = [exp["output_url"]]
            
            lines_ps1 = [
                f"# LabX Remote: ERTOS Exp {s_num:02d} (Code + Outputs)",
                f'$filename = "{src_fname}"',
                "$code = @'",
                src_content,
                "'@",
                "$target = Join-Path $PWD $filename",
                "Set-Content -Path $target -Value $code -Encoding utf8",
                f'Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White',
                ""
            ]
            for out_p in out_files:
                out_leaf = out_p.split("/")[-1]
                lines_ps1.extend([
                    f'$outTarget = Join-Path $PWD "{out_leaf}"',
                    "try {",
                    f'    Invoke-WebRequest "https://cli-t0km.onrender.com/{out_p}" -OutFile $outTarget -UseBasicParsing',
                    f'    Write-Host "[OK] Downloaded Output to: {out_leaf}" -ForegroundColor White',
                    "} catch {",
                    f'    Write-Host "[!] Could not fetch {out_leaf}: $_" -ForegroundColor DarkGray',
                    "}"
                ])
            e_ps1 = "\n".join(lines_ps1)
            with open(PUBLIC_DIR / f"e{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(e_ps1)

    # Generate individual scripts (cn6.ps1 - cn9.ps1) for CN
    for exp in EXPERIMENTS:
        if exp.get("subject") == "CN":
            s_num = exp.get("lab_serial", 1)
            lines_ps1 = [
                f"# LabX Remote: CN Exp {s_num:02d} ({exp['title']})"
            ]
            for src_file in exp["files"]:
                src_fname = src_file["path"]
                src_content = src_file["content"]
                lines_ps1.extend([
                    f'$filename = "{src_fname}"',
                    "$code = @'",
                    src_content,
                    "'@",
                    "$target = Join-Path $PWD $filename",
                    "Set-Content -Path $target -Value $code -Encoding utf8",
                    f'Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White',
                    ""
                ])
            cn_code = "\n".join(lines_ps1)
            with open(PUBLIC_DIR / f"cn{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(cn_code)
            with open(PUBLIC_DIR / f"c{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(cn_code)
            if s_num == 9:
                with open(PUBLIC_DIR / "cnsocket.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "socket.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
            if s_num == 10:
                with open(PUBLIC_DIR / "dijkstra.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "cndijkstra.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
            if s_num == 11:
                with open(PUBLIC_DIR / "staticrouting.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "gns3.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
                with open(PUBLIC_DIR / "routing.ps1", "w", encoding="utf-8") as f:
                    f.write(cn_code)
    # Generate individual pinpoint scripts (a1.ps1 - a12.ps1) for AISC
    for exp in EXPERIMENTS:
        if exp.get("subject", "AISC") == "AISC":
            s_num = exp["id"]
            lines_ps1 = [
                f"# LabX Remote: AISC Practical {s_num:02d} ({exp['title']})"
            ]
            for src_file in exp["files"]:
                src_fname = src_file["path"]
                src_content = src_file["content"]
                lines_ps1.extend([
                    f'$filename = "{src_fname}"',
                    "$code = @'",
                    src_content,
                    "'@",
                    "$target = Join-Path $PWD $filename",
                    "Set-Content -Path $target -Value $code -Encoding utf8",
                    f'Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White',
                    ""
                ])
            lines_ps1.append(f'Write-Host "[OK] AISC Practical {s_num:02d} ready!" -ForegroundColor White')
            a_code = "\n".join(lines_ps1)
            with open(PUBLIC_DIR / f"a{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(a_code)
            with open(PUBLIC_DIR / f"aisc{s_num}.ps1", "w", encoding="utf-8") as f:
                f.write(a_code)

    # Generate interactive / universal aisc.ps1 script
    aisc_ps1 = """param([string]$Choice = "")

if (-not $Choice) {
    Write-Host "==============================================================" -ForegroundColor White
    Write-Host "               AISC Practicals Delivery Tool                  " -ForegroundColor White
    Write-Host "==============================================================" -ForegroundColor Gray
    Write-Host "  [all]   Pull ALL 12 AISC Practicals (Complete bundle)" -ForegroundColor Gray
    Write-Host "  [1-12]  Pull a specific Practical by serial number" -ForegroundColor Gray
    Write-Host "==============================================================" -ForegroundColor Gray
    $Choice = Read-Host "Enter choice [all or 1-12, default: all]"
}

if (-not $Choice -or $Choice -eq "all") {
    $zip = Join-Path $PWD "aisc_temp.zip"
    Write-Host "Downloading all 12 AISC Practicals from LabX Remote..." -ForegroundColor White
    Invoke-WebRequest "https://cli-t0km.onrender.com/downloads/aisc_experiments.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath $PWD -Force
    Remove-Item $zip -Force
    Write-Host "[OK] All 12 AISC Practicals extracted into current directory!" -ForegroundColor White
} else {
    $num = [int]$Choice
    if ($num -ge 1 -and $num -le 12) {
        $scriptUrl = "https://cli-t0km.onrender.com/a$num.ps1"
        Invoke-Expression (Invoke-RestMethod $scriptUrl)
    } else {
        Write-Host "[!] Invalid practical number: $Choice (Please enter 1-12 or 'all')" -ForegroundColor DarkGray
    }
}
"""
    with open(PUBLIC_DIR / "aisc.ps1", "w", encoding="utf-8") as f:
        f.write(aisc_ps1)


    get_ps1 = """param($Id, [string]$Lab = "")
if (-not $Id) {
    $Id = Read-Host "Enter experiment number (1-10 for ERTOS, 6-9 for CN, 1-12 for AISC, or 1-26)"
}

$intId = [int]$Id
$cat = Invoke-RestMethod "https://cli-t0km.onrender.com/catalog.json"

if ($Lab -eq "ertos" -or $Lab -eq "es") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
} elseif ($Lab -eq "cn") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "CN" -and $_.lab_serial -eq $intId }
} elseif ($Lab -eq "aisc") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "AISC" -and $_.lab_serial -eq $intId }
} else {
    $item = $cat.experiments | Where-Object { $_.id -eq $intId }
    if (-not $item -and $intId -ge 6 -and $intId -le 9) {
        $item = $cat.experiments | Where-Object { $_.subject -eq "CN" -and $_.lab_serial -eq $intId }
    }
    if (-not $item -and $intId -le 10) {

        $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
    }
}

if (-not $item) {
    Write-Host "[!] Experiment $Id not found." -ForegroundColor DarkGray
    return
}

$num = "{0:D2}" -f [int]$item.id
$mf = Invoke-RestMethod "https://cli-t0km.onrender.com/$($item.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://cli-t0km.onrender.com/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($item.title) into $dir/" -ForegroundColor White

if ($item.output_files) {
    foreach ($outP in $item.output_files) {
        $outName = Split-Path $outP -Leaf
        Invoke-WebRequest "https://cli-t0km.onrender.com/$outP" -OutFile (Join-Path $dir $outName) -UseBasicParsing
        Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
    }
} elseif ($item.output_url) {
    $outName = Split-Path $item.output_url -Leaf
    Invoke-WebRequest "https://cli-t0km.onrender.com/$($item.output_url)" -OutFile (Join-Path $dir $outName) -UseBasicParsing
    Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
}
"""
    with open(PUBLIC_DIR / "get.ps1", "w", encoding="utf-8") as f:
        f.write(get_ps1)

    list_ps1 = """$cat = Invoke-RestMethod "https://cli-t0km.onrender.com/catalog.json"
Write-Host "`n==== AISC, Embedded Systems / RTOS & Computer Networks Experiments ====" -ForegroundColor White
$cat.experiments | Format-Table @{Label="Lab"; Expression={$_.subject}}, @{Label="Exp"; Expression={"#" + ("{0:D2}" -f $_.lab_serial)}}, @{Label="Title"; Expression={$_.title}}, @{Label="Language"; Expression={$_.language}}
Write-Host "Quick commands:" -ForegroundColor White
Write-Host "  Pull AISC Practical (e.g. 1)     : irm https://cli-t0km.onrender.com/a1.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull AISC Interactive (all/1-12) : irm https://cli-t0km.onrender.com/aisc.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull ERTOS Exp 2 (Code + Output) : irm https://cli-t0km.onrender.com/e2.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All ERTOS (Code + Outputs)  : irm https://cli-t0km.onrender.com/ertos.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All Computer Networks (CN)  : irm https://cli-t0km.onrender.com/cn.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN Java Socket Programming  : irm https://cli-t0km.onrender.com/cnsocket.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN Dijkstra Algorithm       : irm https://cli-t0km.onrender.com/dijkstra.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull CN GNS3 Static Routing      : irm https://cli-t0km.onrender.com/staticrouting.ps1 | iex" -ForegroundColor Gray
Write-Host "  Pull All experiments             : irm https://cli-t0km.onrender.com/all.ps1 | iex`n" -ForegroundColor Gray
"""
    with open(PUBLIC_DIR / "list.ps1", "w", encoding="utf-8") as f:
        f.write(list_ps1)

    # 7. Write index.html
    full_html = HTML_HEADER + "\n".join(html_cards) + HTML_FOOTER
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    # 8. Build Software Engineering (SE) diagrams
    se_script = BASE_DIR / "scripts" / "generate_all_se_case_studies.py"
    if se_script.exists():
        import subprocess
        import sys
        subprocess.run([sys.executable, str(se_script)], check=False)

    print("Minimalist Black & White host build completed successfully!")
    print(f"Total experiments compiled: {len(EXPERIMENTS)}")

if __name__ == "__main__":
    generate_host()
