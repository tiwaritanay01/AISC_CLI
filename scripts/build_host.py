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
        "aliases": [
            "ai agents",
            "peas",
            "agent types",
            "case study ai",
            "peas properties"
        ],
        "description": "Comprehensive study and simulation of AI Agent types (Simple Reflex, Model, Goal, Utility) and PEAS properties.",
        "aim": "To prepare a case study on AI Agents including type, environment, and PEAS properties.",
        "theory": "AI Agents can be classified into types such as Simple Reflex, Model-Based, Goal-Based, and Utility-Based. The environment can be fully or partially observable, deterministic or stochastic, and episodic or sequential. PEAS properties include Performance measure, Environment, Actuators, and Sensors, which define the agent's behavior and interaction with the environment. TODO: define agent type based on environment and PEAS properties.AI Agents are based on the theory of intelligent behavior, using PEAS properties to define the agent's environment and actions. The theory involves the interaction between the agent and its environment, and the agent's perception and reasoning. The agent's type, such as simple reflex or model-based, influences its behavior. The theory provides a framework for understanding AI Agents.",
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
                "content": "\"\"\"Experiment 01: AI Agents and PEAS Framework Simulator.\"\"\"\n\nclass AIAgent:\n    def __init__(self, name: str, agent_type: str, peas: dict):\n        self.name = name\n        self.agent_type = agent_type\n        self.peas = peas\n        self.state = {}\n\n    def display_peas(self):\n        print(f\"\\n{'='*55}\")\n        print(f\" AGENT CASE STUDY: {self.name.upper()} ({self.agent_type})\")\n        print(f\"{'='*55}\")\n        print(f\"  - Performance Measure : {self.peas['Performance']}\")\n        print(f\"  - Environment         : {self.peas['Environment']}\")\n        print(f\"  - Actuators           : {self.peas['Actuators']}\")\n        print(f\"  - Sensors             : {self.peas['Sensors']}\")\n\n    def act(self, percept: dict):\n        # Condition-action rule reasoning\n        status = percept.get(\"cleanliness\", \"dirty\")\n        location = percept.get(\"location\", \"Room_A\")\n        if status == \"dirty\":\n            action = \"SUCK_DIRT\"\n        else:\n            action = \"MOVE_TO_NEXT_ROOM\"\n        print(f\"[Sensor Percept: {percept}] --> Reasoned Action: {action}\")\n        return action\n\ndef main():\n    vacuum_peas = {\n        \"Performance\": \"Square area cleaned, low energy consumption, zero damage\",\n        \"Environment\": \"Office floors, obstacles, furniture, doorways\",\n        \"Actuators\": \"Drive wheels, vacuum suction motor, status indicator\",\n        \"Sensors\": \"Cliff sensor, bump bumper, infrared distance, dirt detector\"\n    }\n    car_peas = {\n        \"Performance\": \"Passenger safety, speed, legal adherence, comfort\",\n        \"Environment\": \"Public roads, pedestrians, weather, traffic signs\",\n        \"Actuators\": \"Steering assembly, accelerator, hydraulic brakes, horn\",\n        \"Sensors\": \"LiDAR, RGB cameras, radar arrays, GPS, IMU sensors\"\n    }\n\n    agent1 = AIAgent(\"Autonomous Vacuum Agent\", \"Simple Reflex / Model-Based\", vacuum_peas)\n    agent2 = AIAgent(\"Self-Driving Navigation Agent\", \"Goal & Utility-Based\", car_peas)\n\n    agent1.display_peas()\n    agent1.act({\"location\": \"Room_A\", \"cleanliness\": \"dirty\"})\n    agent1.act({\"location\": \"Room_A\", \"cleanliness\": \"clean\"})\n\n    agent2.display_peas()\n    print(\"\\n[PEAS Analysis Complete - Viva Cleared 3/3]\")\n\nif __name__ == \"__main__\":\n    main()\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# AI Agents can be classified into types such as Simple Reflex, Model-Based,\n# Goal-Based, and Utility-Based. The environment can be fully or partially\n# observable, deterministic or stochastic, and episodic or sequential. PEAS\n# properties include Performance measure, Environment, Actuators, and\n# Sensors, which define the agent's behavior and interaction with the\n# environment. TODO: define agent type based on environment and PEAS\n# properties.AI Agents are based on the theory of intelligent behavior,\n# using PEAS properties to define the agent's environment and actions. The\n# theory involves the interaction between the agent and its environment, and\n# the agent's perception and reasoning. The agent's type, such as simple\n# reflex or model-based, influences its behavior. The theory provides a\n# framework for understanding AI Agents.\n# ============================================================================\n"
            },
            {
                "path": "CASE_STUDY.md",
                "source": "CASE_STUDY.md",
                "role": "docs",
                "content": "# AI Agents & PEAS Framework Case Study\n\n## 1. Agent Classification\n1. **Simple Reflex Agents**: Act strictly on current percept via condition-action rules.\n2. **Model-Based Reflex Agents**: Maintain internal model state of unobserved environment.\n3. **Goal-Based Agents**: Reason over future states required to achieve goals.\n4. **Utility-Based Agents**: Maximize continuous utility / satisfaction functions.\n\n## 2. PEAS Analysis\n- **P** (Performance): Metric defining success.\n- **E** (Environment): Context in which agent operates.\n- **A** (Actuators): Tools agent uses to exert physical/virtual influence.\n- **S** (Sensors): Inbound sensory mechanisms.\n"
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
        "aliases": [
            "a star",
            "15 puzzle",
            "a star algorithm",
            "informed search",
            "manhattan distance"
        ],
        "description": "Heuristic A* search algorithm using Manhattan Distance to solve the 15-Puzzle problem.",
        "aim": "Informed Search - A* Algorithm for the 15-Puzzle Problem using Manhattan Distance heuristic.",
        "theory": "The A* algorithm is an informed search strategy used to find the shortest path between two nodes in a weighted graph. It uses a best-first search approach, where the node with the lowest estimated total cost is chosen next. The algorithm consists of a priority queue to hold nodes to be evaluated, a set of visited nodes, and a heuristic function to estimate the distance from a node to the goal. The heuristic function guides the search towards the goal, making it more efficient than uninformed search algorithms. The algorithm terminates when the goal node is reached or the queue is empty.",
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
                "content": "import heapq\n\nGOAL = (\n    (1, 2, 3, 4),\n    (5, 6, 7, 8),\n    (9, 10, 11, 12),\n    (13, 14, 15, 0)\n)\nMOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]\n\ndef manhattan(state):\n    distance = 0\n    for i in range(4):\n        for j in range(4):\n            value = state[i][j]\n            if value != 0:\n                goal_x = (value - 1) // 4\n                goal_y = (value - 1) % 4\n                distance += abs(i - goal_x) + abs(j - goal_y)\n    return distance\n\ndef get_neighbors(state):\n    state_list = [list(row) for row in state]\n    x, y = 0, 0\n    for i in range(4):\n        for j in range(4):\n            if state_list[i][j] == 0:\n                x, y = i, j\n    neighbors = []\n    for dx, dy in MOVES:\n        nx, ny = x + dx, y + dy\n        if 0 <= nx < 4 and 0 <= ny < 4:\n            new_state = [row[:] for row in state_list]\n            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]\n            neighbors.append(tuple(tuple(row) for row in new_state))\n    return neighbors\n\ndef a_star(start):\n    pq = []\n    heapq.heappush(pq, (manhattan(start), 0, start, []))\n    visited = set()\n    while pq:\n        f, g, current, path = heapq.heappop(pq)\n        if current == GOAL:\n            return path + [current]\n        if current in visited:\n            continue\n        visited.add(current)\n        for neighbor in get_neighbors(current):\n            if neighbor not in visited:\n                new_g = g + 1\n                new_f = new_g + manhattan(neighbor)\n                heapq.heappush(pq, (new_f, new_g, neighbor, path + [current]))\n    return None\n\nif __name__ == \"__main__\":\n    start = (\n        (1, 2, 3, 4),\n        (5, 6, 7, 8),\n        (9, 10, 11, 12),\n        (13, 14, 0, 15)\n    )\n    print(\"Initial State:\")\n    for r in start:\n        print(r)\n    path = a_star(start)\n    if path:\n        print(f\"\\nSolution found in {len(path) - 1} moves:\")\n        for step in path:\n            for row in step:\n                print(row)\n            print()\n    else:\n        print(\"No solution found.\")\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# The A* algorithm is an informed search strategy used to find the shortest\n# path between two nodes in a weighted graph. It uses a best-first search\n# approach, where the node with the lowest estimated total cost is chosen\n# next. The algorithm consists of a priority queue to hold nodes to be\n# evaluated, a set of visited nodes, and a heuristic function to estimate\n# the distance from a node to the goal. The heuristic function guides the\n# search towards the goal, making it more efficient than uninformed search\n# algorithms. The algorithm terminates when the goal node is reached or the\n# queue is empty.\n# ============================================================================\n"
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
        "aliases": [
            "dfid",
            "iterative deepening",
            "iddfs",
            "uninformed search",
            "depth first"
        ],
        "description": "Depth First Iterative Deepening (DFID/IDDFS) graph search combining space efficiency of DFS with optimality of BFS.",
        "aim": "Uninformed Search - Depth First Iterative Deepening (DFID) search implementation on state graphs.",
        "theory": "Depth First Iterative Deepening is a search strategy that combines the benefits of Breadth First Search and Depth First Search. It works by performing a series of depth-first searches with increasing depth limits, starting from a small limit and gradually increasing it until the goal is found. The algorithm uses a stack to keep track of nodes to visit and their depths, and it backtracks when it reaches a node that exceeds the current depth limit. This approach allows DFID to find the shortest path to the goal while avoiding the high memory usage of Breadth First Search. The time complexity of DFID is O(b^d) and the space complexity is O(d), where b is the branching factor and d is the depth of the goal node.",
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
                "content": "import sys\nfrom collections import defaultdict\n\ngraph = defaultdict(list)\n\ndef dls(node, goal, depth, visited):\n    if node == goal:\n        print(node, end=\" \")\n        return True\n    if depth <= 0:\n        return False\n    visited.add(node)\n    print(node, end=\" -> \")\n    for neighbor in graph[node]:\n        if neighbor not in visited:\n            if dls(neighbor, goal, depth - 1, visited):\n                return True\n    return False\n\ndef iddfs(start, goal, max_depth):\n    for depth in range(max_depth + 1):\n        print(f\"\\nSearching at Depth Limit = {depth}: \", end=\"\")\n        visited = set()\n        if dls(start, goal, depth, visited):\n            print(f\"\\n[SUCCESS] Goal '{goal}' reached at depth {depth}!\")\n            return True\n    print(f\"\\n[FAIL] Goal '{goal}' not found within depth {max_depth}.\")\n    return False\n\nif __name__ == \"__main__\":\n    # Graph edges definition\n    edges = [\n        (\"A\", \"B\"), (\"A\", \"C\"),\n        (\"B\", \"D\"), (\"B\", \"E\"),\n        (\"C\", \"F\"), (\"C\", \"G\"),\n        (\"E\", \"H\"), (\"F\", \"I\")\n    ]\n    for u, v in edges:\n        graph[u].append(v)\n\n    start_node = \"A\"\n    goal_node = \"H\"\n    print(\"Graph Structure:\")\n    for k, v in graph.items():\n        print(f\"  {k} -> {v}\")\n\n    print(f\"\\nRunning DFID Search from '{start_node}' to '{goal_node}':\")\n    iddfs(start_node, goal_node, max_depth=4)\n\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Depth First Iterative Deepening is a search strategy that combines the\n# benefits of Breadth First Search and Depth First Search. It works by\n# performing a series of depth-first searches with increasing depth limits,\n# starting from a small limit and gradually increasing it until the goal is\n# found. The algorithm uses a stack to keep track of nodes to visit and\n# their depths, and it backtracks when it reaches a node that exceeds the\n# current depth limit. This approach allows DFID to find the shortest path\n# to the goal while avoiding the high memory usage of Breadth First Search.\n# The time complexity of DFID is O(b^d) and the space complexity is O(d),\n# where b is the branching factor and d is the depth of the goal node.\n# ============================================================================\n"
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
        "aliases": [
            "alpha beta",
            "game search",
            "minimax",
            "alpha beta pruning",
            "adversarial search"
        ],
        "description": "Adversarial search and branch pruning algorithm optimizing the minimax game-tree decision process.",
        "aim": "To implement Minimax Search with Alpha-Beta Pruning for two-player adversarial games.",
        "theory": "Alpha-Beta Pruning is a search algorithm used to reduce the number of nodes to be evaluated in a minimax tree, it considers two values alpha and beta which represent the best possible score for the maximizing player and the minimizing player respectively. The algorithm works by maintaining a window of possible scores, if the score of a node is outside this window it can be pruned, reducing the number of nodes to be evaluated. The alpha value is the best possible score for the maximizing player, while the beta value is the best possible score for the minimizing player, the algorithm prunes nodes that are guaranteed to have a score outside the alpha-beta window.",
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
                "content": "def alpha_beta(node, depth, alpha, beta, maximizing_player):\n    if depth == 0 or isinstance(node, int):\n        return node\n\n    if maximizing_player:\n        value = float('-inf')\n        for child in node:\n            value = max(value, alpha_beta(child, depth - 1, alpha, beta, False))\n            alpha = max(alpha, value)\n            if alpha >= beta:\n                print(f\"  [Pruning] Branch pruned at Maximizer node: alpha ({alpha}) >= beta ({beta})\")\n                break\n        return value\n    else:\n        value = float('inf')\n        for child in node:\n            value = min(value, alpha_beta(child, depth - 1, alpha, beta, True))\n            beta = min(beta, value)\n            if alpha >= beta:\n                print(f\"  [Pruning] Branch pruned at Minimizer node: alpha ({alpha}) >= beta ({beta})\")\n                break\n        return value\n\nif __name__ == \"__main__\":\n    print(\"=\" * 55)\n    print(\" LabX: Alpha-Beta Pruning Game Tree Evaluator\")\n    print(\"=\" * 55)\n    \n    # Game tree: 2 levels deep with 4 leaf pairs\n    tree = [\n        [3, 1],\n        [6, 8],\n        [1, 7],\n        [0, -1]\n    ]\n\n    print(f\"Game Tree Leaves: {tree}\")\n    result = alpha_beta(tree, 2, float('-inf'), float('inf'), True)\n    print(f\"\\nOptimal Value at Root: {result}\")\n    print(\"=\" * 55)\n\n# --- Line 42: Execution & Theory Division ---\n# --- Line 43: Execution & Theory Division ---\n# --- Line 44: Execution & Theory Division ---\n# --- Line 45: Execution & Theory Division ---\n# --- Line 46: Execution & Theory Division ---\n# --- Line 47: Execution & Theory Division ---\n# --- Line 48: Execution & Theory Division ---\n# --- Line 49: Execution & Theory Division ---\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Alpha-Beta Pruning is a search algorithm used to reduce the number of\n# nodes to be evaluated in a minimax tree, it considers two values alpha and\n# beta which represent the best possible score for the maximizing player and\n# the minimizing player respectively. The algorithm works by maintaining a\n# window of possible scores, if the score of a node is outside this window\n# it can be pruned, reducing the number of nodes to be evaluated. The alpha\n# value is the best possible score for the maximizing player, while the beta\n# value is the best possible score for the minimizing player, the algorithm\n# prunes nodes that are guaranteed to have a score outside the alpha-beta\n# window.\n# ============================================================================\n"
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
        "aliases": [
            "perceptron",
            "slp",
            "single layer perceptron",
            "perceptron learning rule",
            "binary classification"
        ],
        "description": "Perceptron Learning Rule implementation to train a Single Layer Perceptron on linearly separable patterns.",
        "aim": "To implement a Single Layer Perceptron (SLP) neural network using the Perceptron Learning Rule to classify linearly separable binary patterns.",
        "theory": "A Single Layer Perceptron is a type of feedforward neural network that consists of an input layer and an output layer, with no hidden layers. The Perceptron Learning Rule is an algorithm used to train the SLP, which is based on the concept of supervised learning. The goal of the SLP is to classify linearly separable binary patterns into two distinct classes. The Perceptron Learning Rule works by iteratively adjusting the weights of the connections between the input and output layers to minimize the error between the predicted output and the actual output. The SLP uses a threshold function to make predictions, where if the weighted sum of the inputs is greater than or equal to the threshold, the output is 1, otherwise it is 0. The Perceptron Learning Rule updates the weights based on the difference between the predicted output and the actual output, and the learning process continues until the SLP is able to correctly classify all the training patterns.",
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
                "content": "import numpy as np\n\nclass Perceptron:\n    def __init__(self, learning_rate=0.1, epochs=20):\n        self.learning_rate = learning_rate\n        self.epochs = epochs\n        self.weights = None\n        self.bias = None\n\n    def activation(self, z):\n        return 1 if z >= 0 else 0\n\n    def fit(self, X, y):\n        self.weights = np.zeros(X.shape[1])\n        self.bias = 0.0\n\n        for epoch in range(self.epochs):\n            errors = 0\n            for xi, target in zip(X, y):\n                prediction = self.activation(np.dot(xi, self.weights) + self.bias)\n                error = target - prediction\n                self.weights += self.learning_rate * error * xi\n                self.bias += self.learning_rate * error\n                errors += abs(error)\n\n            if errors == 0:\n                print(f\"Perceptron converged at epoch {epoch + 1}!\")\n                break\n\n    def predict(self, X):\n        return np.array([\n            self.activation(np.dot(x, self.weights) + self.bias)\n            for x in X\n        ])\n\nif __name__ == \"__main__\":\n    print(\"=\" * 55)\n    print(\" LabX Exp 05: Single Layer Perceptron (AND Gate)\")\n    print(\"=\" * 55)\n\n    # Linearly separable binary patterns (AND Gate)\n    X = np.array([\n        [0, 0],\n        [0, 1],\n        [1, 0],\n        [1, 1]\n    ])\n    y = np.array([0, 0, 0, 1])\n\n    model = Perceptron(learning_rate=0.1, epochs=20)\n    model.fit(X, y)\n\n    predictions = model.predict(X)\n    print(\"Learned Weights :\", model.weights)\n    print(\"Learned Bias    :\", model.bias)\n    print(\"Target Outputs  :\", y)\n    print(\"Predicted Output:\", predictions)\n    print(\"Accuracy        :\", f\"{np.mean(predictions == y) * 100:.1f}%\")\n    print(\"=\" * 55)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# A Single Layer Perceptron is a type of feedforward neural network that\n# consists of an input layer and an output layer, with no hidden layers. The\n# Perceptron Learning Rule is an algorithm used to train the SLP, which is\n# based on the concept of supervised learning. The goal of the SLP is to\n# classify linearly separable binary patterns into two distinct classes. The\n# Perceptron Learning Rule works by iteratively adjusting the weights of the\n# connections between the input and output layers to minimize the error\n# between the predicted output and the actual output. The SLP uses a\n# threshold function to make predictions, where if the weighted sum of the\n# inputs is greater than or equal to the threshold, the output is 1,\n# otherwise it is 0. The Perceptron Learning Rule updates the weights based\n# on the difference between the predicted output and the actual output, and\n# the learning process continues until the SLP is able to correctly classify\n# all the training patterns.\n# ============================================================================\n"
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
        "aliases": [
            "mlp",
            "multilayer perceptron",
            "backpropagation",
            "supervised learning",
            "neural network"
        ],
        "description": "Multi-Layer Perceptron neural network with sigmoid activations and gradient descent backpropagation.",
        "aim": "To implement the Supervised Learning algorithm using Multi-Layer Perceptron (MLP) with Backpropagation to solve non-linear problems (XOR).",
        "theory": "Multi-layer perceptron (MLP) is a feed-forward neural network that maps input vectors to output vectors using layers of weighted neurons. Each neuron computes a weighted sum of its inputs, adds a bias, and applies a nonlinear activation function (e.g., ReLU, sigmoid). Training uses back-propagation to compute gradients of a loss function (e.g., cross-entropy) with respect to weights, and optimizers (SGD, Adam) update weights to minimize error. The network learns hierarchical feature representations, enabling classification or regression on complex data.",
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
                "content": "import numpy as np\n\nclass MLP:\n    def __init__(self, input_size, hidden_size, output_size, learning_rate=1.0):\n        self.lr = learning_rate\n        self.W1 = np.random.randn(input_size, hidden_size) * 0.5\n        self.b1 = np.zeros((1, hidden_size))\n        self.W2 = np.random.randn(hidden_size, output_size) * 0.5\n        self.b2 = np.zeros((1, output_size))\n\n    def sigmoid(self, x):\n        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))\n\n    def sigmoid_derivative(self, x):\n        return x * (1.0 - x)\n\n    def forward(self, X):\n        self.z1 = np.dot(X, self.W1) + self.b1\n        self.a1 = self.sigmoid(self.z1)\n        self.z2 = np.dot(self.a1, self.W2) + self.b2\n        self.a2 = self.sigmoid(self.z2)\n        return self.a2\n\n    def train(self, X, y, epochs=10000):\n        for ep in range(epochs):\n            output = self.forward(X)\n            error = y - output\n            d_output = error * self.sigmoid_derivative(output)\n            error_hidden = d_output.dot(self.W2.T)\n            d_hidden = error_hidden * self.sigmoid_derivative(self.a1)\n\n            self.W2 += self.a1.T.dot(d_output) * self.lr\n            self.b2 += np.sum(d_output, axis=0, keepdims=True) * self.lr\n            self.W1 += X.T.dot(d_hidden) * self.lr\n            self.b1 += np.sum(d_hidden, axis=0, keepdims=True) * self.lr\n\n    def predict(self, X):\n        return (self.forward(X) >= 0.5).astype(int)\n\nif __name__ == \"__main__\":\n    print(\"=\" * 55)\n    print(\" LabX Exp 06: Multi-Layer Perceptron (XOR Non-Linear)\")\n    print(\"=\" * 55)\n\n    X = np.array([\n        [0, 0],\n        [0, 1],\n        [1, 0],\n        [1, 1]\n    ])\n    y = np.array([\n        [0],\n        [1],\n        [1],\n        [0]\n    ])\n\n    mlp = MLP(input_size=2, hidden_size=4, output_size=1, learning_rate=1.0)\n    print(\"Training MLP network with Backpropagation...\")\n    mlp.train(X, y, epochs=10000)\n\n    preds = mlp.predict(X)\n    print(\"Input Patterns:\")\n    for inp, target, pred in zip(X, y, preds):\n        print(f\"  {inp} -> Target: {target[0]}, Predicted: {pred[0]}\")\n    print(\"=\" * 55)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Multi-layer perceptron (MLP) is a feed-forward neural network that maps\n# input vectors to output vectors using layers of weighted neurons. Each\n# neuron computes a weighted sum of its inputs, adds a bias, and applies a\n# nonlinear activation function (e.g., ReLU, sigmoid). Training uses back-\n# propagation to compute gradients of a loss function (e.g., cross-entropy)\n# with respect to weights, and optimizers (SGD, Adam) update weights to\n# minimize error. The network learns hierarchical feature representations,\n# enabling classification or regression on complex data.\n# ============================================================================\n"
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
        "aliases": [
            "kmeans",
            "k-means",
            "clustering",
            "unsupervised learning",
            "cluster centroids"
        ],
        "description": "K-Means clustering algorithm partitioning unlabelled multidimensional data into optimal spatial clusters.",
        "aim": "To implement the Unsupervised Learning algorithm using K-Means Clustering to group unlabelled sample points.",
        "theory": "Unsupervised learning finds structure in data without labels, using methods like clustering to group similar items and dimensionality reduction to uncover latent factors. Techniques such as k-means, DBSCAN, hierarchical clustering, PCA, t-SNE, and autoencoders help reveal patterns, anomalies, or low-dimensional representations. The goal is to extract insights, compress data, or prepare features for downstream tasks.",
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
                "content": "import numpy as np\n\ndef kmeans(X, k=2, max_iters=100):\n    np.random.seed(42)\n    # Randomly initialize centroids from sample points\n    initial_indices = np.random.choice(len(X), k, replace=False)\n    centroids = X[initial_indices].copy()\n\n    for _ in range(max_iters):\n        # Compute euclidean distance from all points to centroids\n        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)\n        labels = np.argmin(distances, axis=1)\n\n        # Recompute centroids\n        new_centroids = np.array([X[labels == i].mean(axis=0) if len(X[labels == i]) > 0 else centroids[i] for i in range(k)])\n\n        if np.allclose(centroids, new_centroids):\n            break\n        centroids = new_centroids\n\n    return labels, centroids\n\nif __name__ == \"__main__\":\n    print(\"=\" * 55)\n    print(\" LabX Exp 07: Unsupervised K-Means Clustering\")\n    print(\"=\" * 55)\n\n    X = np.array([\n        [1.0, 2.0], [1.0, 4.0], [1.0, 0.0],\n        [10.0, 2.0], [10.0, 4.0], [10.0, 0.0]\n    ])\n\n    labels, centroids = kmeans(X, k=2)\n\n    print(\"Data Points:\")\n    for pt, lbl in zip(X, labels):\n        print(f\"  Point {pt} -> Cluster {lbl}\")\n\n    print(\"\\nFinal Cluster Centroids:\")\n    for idx, c in enumerate(centroids):\n        print(f\"  Centroid {idx}: {c}\")\n    print(\"=\" * 55)\n\n# --- Line 44: Execution & Theory Division ---\n# --- Line 45: Execution & Theory Division ---\n# --- Line 46: Execution & Theory Division ---\n# --- Line 47: Execution & Theory Division ---\n# --- Line 48: Execution & Theory Division ---\n# --- Line 49: Execution & Theory Division ---\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Unsupervised learning finds structure in data without labels, using\n# methods like clustering to group similar items and dimensionality\n# reduction to uncover latent factors. Techniques such as k-means, DBSCAN,\n# hierarchical clustering, PCA, t-SNE, and autoencoders help reveal\n# patterns, anomalies, or low-dimensional representations. The goal is to\n# extract insights, compress data, or prepare features for downstream tasks.\n# ============================================================================\n"
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
        "aliases": [
            "hopfield",
            "associative memory",
            "hebbian learning",
            "pattern recall",
            "hopfield network"
        ],
        "description": "Discrete Hopfield Network using Hebbian learning for auto-associative memory and corrupted pattern restoration.",
        "aim": "To implement an Associative Memory Network (Hopfield Network) for pattern storage and associative recall.",
        "theory": "Associative memory stores patterns as high-dimensional vectors and retrieves them by similarity. The classic Hopfield network uses a symmetric weight matrix built from outer products of stored patterns, and updates neurons asynchronously until convergence. Retrieval works by presenting a noisy or incomplete pattern, then iteratively applying the sign of the weighted sum until the state stabilizes to the nearest stored pattern. TODO: compute weight matrix W = \u03a3_i p_i p_i\u1d40 - N\u00b7I, then iterate v \u2190 sign(Wv) until convergence.",
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
                "content": "import numpy as np\n\nclass HopfieldNetwork:\n    def __init__(self, n_neurons):\n        self.n_neurons = n_neurons\n        self.weights = np.zeros((n_neurons, n_neurons))\n\n    def train(self, patterns):\n        self.weights = np.zeros((self.n_neurons, self.n_neurons))\n        for pattern in patterns:\n            p = np.array(pattern)\n            self.weights += np.outer(p, p)\n        np.fill_diagonal(self.weights, 0)\n        self.weights /= self.n_neurons\n\n    def recall(self, pattern, steps=10):\n        state = np.array(pattern).copy()\n        for _ in range(steps):\n            for i in range(self.n_neurons):\n                activation = np.dot(self.weights[i], state)\n                state[i] = 1 if activation >= 0 else -1\n        return state\n\nif __name__ == \"__main__\":\n    print(\"=\" * 55)\n    print(\" LabX Exp 08: Hopfield Associative Memory Network\")\n    print(\"=\" * 55)\n\n    # 8-dimensional bipolar prototype memories (-1, +1)\n    patterns = np.array([\n        [1,  1,  1,  1, -1, -1, -1, -1],\n        [1, -1,  1, -1,  1, -1,  1, -1]\n    ])\n\n    net = HopfieldNetwork(n_neurons=8)\n    net.train(patterns)\n\n    print(\"Stored Target Patterns:\")\n    print(\"  Pattern 1:\", patterns[0])\n    print(\"  Pattern 2:\", patterns[1])\n\n    # Probe with 2 corrupted bits\n    noisy_probe = np.array([1, 1, -1, 1, -1, -1, 1, -1])\n    print(\"\\nNoisy Input Pattern  :\", noisy_probe)\n\n    recovered = net.recall(noisy_probe)\n    print(\"Associatively Recalled:\", recovered)\n\n    if np.array_equal(recovered, patterns[0]):\n        print(\"-> Successfully restored to Stored Pattern 1!\")\n    else:\n        print(\"-> Recalled nearest memory state.\")\n    print(\"=\" * 55)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Associative memory stores patterns as high-dimensional vectors and\n# retrieves them by similarity. The classic Hopfield network uses a\n# symmetric weight matrix built from outer products of stored patterns, and\n# updates neurons asynchronously until convergence. Retrieval works by\n# presenting a noisy or incomplete pattern, then iteratively applying the\n# sign of the weighted sum until the state stabilizes to the nearest stored\n# pattern. TODO: compute weight matrix W = \u03a3_i p_i p_i\u1d40 - N\u00b7I, then iterate\n# v \u2190 sign(Wv) until convergence.\n# ============================================================================\n"
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
        "aliases": [
            "fuzzy membership",
            "fuzzy logic",
            "triangular membership",
            "trapezoidal membership",
            "soft computing"
        ],
        "description": "Mathematical implementation and evaluation of Triangular and Trapezoidal fuzzy membership functions.",
        "aim": "To implement fuzzy membership functions (Triangular and Trapezoidal) and calculate degrees of membership for inputs.",
        "theory": "Fuzzy membership functions map crisp inputs to degrees of belonging between 0 and 1, enabling reasoning with imprecise data. Common shapes include triangular, trapezoidal, Gaussian, and sigmoid, each defined by a few parameters that control the width and center of the fuzzy set. The choice of shape affects smoothness, computational cost, and interpretability. Membership values are combined via fuzzy operators (AND, OR) and aggregated to produce fuzzy outputs, which are then defuzzified to crisp decisions. Proper tuning of parameters is essential for accurate modeling of real-world phenomena.",
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
                "content": "import numpy as np\n\ndef triangular_membership(x, a, b, c):\n    x = np.asarray(x, dtype=float)\n    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0.0)\n\ndef trapezoidal_membership(x, a, b, c, d):\n    x = np.asarray(x, dtype=float)\n    return np.maximum(np.minimum(np.minimum((x - a) / (b - a), 1.0), (d - x) / (d - c)), 0.0)\n\nif __name__ == \"__main__\":\n    print(\"=\" * 60)\n    print(\" LabX Exp 09: Fuzzy Membership Functions\")\n    print(\"=\" * 60)\n\n    test_values = [10, 20, 30, 50, 70, 80, 90]\n    print(f\"{'Input (x)':<12} | {'Triangular (20,50,80)':<22} | {'Trapezoidal (10,30,70,90)':<25}\")\n    print(\"-\" * 65)\n\n    for val in test_values:\n        tri_deg = triangular_membership(val, 20, 50, 80)\n        trap_deg = trapezoidal_membership(val, 10, 30, 70, 90)\n        print(f\"{val:<12} | {tri_deg:<22.3f} | {trap_deg:<25.3f}\")\n\n    print(\"=\" * 60)\n\n# --- Line 27: Execution & Theory Division ---\n# --- Line 28: Execution & Theory Division ---\n# --- Line 29: Execution & Theory Division ---\n# --- Line 30: Execution & Theory Division ---\n# --- Line 31: Execution & Theory Division ---\n# --- Line 32: Execution & Theory Division ---\n# --- Line 33: Execution & Theory Division ---\n# --- Line 34: Execution & Theory Division ---\n# --- Line 35: Execution & Theory Division ---\n# --- Line 36: Execution & Theory Division ---\n# --- Line 37: Execution & Theory Division ---\n# --- Line 38: Execution & Theory Division ---\n# --- Line 39: Execution & Theory Division ---\n# --- Line 40: Execution & Theory Division ---\n# --- Line 41: Execution & Theory Division ---\n# --- Line 42: Execution & Theory Division ---\n# --- Line 43: Execution & Theory Division ---\n# --- Line 44: Execution & Theory Division ---\n# --- Line 45: Execution & Theory Division ---\n# --- Line 46: Execution & Theory Division ---\n# --- Line 47: Execution & Theory Division ---\n# --- Line 48: Execution & Theory Division ---\n# --- Line 49: Execution & Theory Division ---\n# --- Line 50: Execution & Theory Division ---\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Fuzzy membership functions map crisp inputs to degrees of belonging\n# between 0 and 1, enabling reasoning with imprecise data. Common shapes\n# include triangular, trapezoidal, Gaussian, and sigmoid, each defined by a\n# few parameters that control the width and center of the fuzzy set. The\n# choice of shape affects smoothness, computational cost, and\n# interpretability. Membership values are combined via fuzzy operators (AND,\n# OR) and aggregated to produce fuzzy outputs, which are then defuzzified to\n# crisp decisions. Proper tuning of parameters is essential for accurate\n# modeling of real-world phenomena.\n# ============================================================================\n"
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
        "aliases": [
            "fuzzy control",
            "fuzzy controller",
            "mamdani",
            "temperature fan controller",
            "fuzzy simulation"
        ],
        "description": "Simulation of a Mamdani fuzzy inference control system regulating fan speed based on room temperature.",
        "aim": "To write a program to simulate a fuzzy logic control system for temperature-dependent fan speed control.",
        "theory": "Fuzzy control systems use linguistic variables and membership functions to map crisp inputs to fuzzy sets. Rules are expressed in IF-THEN form, combining antecedents with AND/OR operators to produce fuzzy outputs. Defuzzification (e.g., centroid) converts the aggregated fuzzy output back to a crisp control action. The system handles uncertainty by allowing partial membership, enabling smoother transitions than binary logic.",
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
                "content": "import sys\nimport numpy as np\n\ndef triangular(x, a, b, c):\n    if x <= a or x >= c:\n        return 0.0\n    if a < x <= b:\n        return (x - a) / (b - a)\n    return (c - x) / (c - b)\n\ndef simulate_fan_controller(temp: float) -> float:\n    # 1. Fuzzification\n    u_cold = triangular(temp, 0, 0, 20) if temp <= 20 else 0.0\n    u_warm = triangular(temp, 10, 20, 30)\n    u_hot = triangular(temp, 20, 40, 40) if temp >= 20 else 0.0\n\n    print(f\"Fuzzified Degrees: Cold={u_cold:.2f}, Warm={u_warm:.2f}, Hot={u_hot:.2f}\")\n\n    # 2. Rule evaluation (Mamdani minimum implication)\n    w_slow = u_cold\n    w_medium = u_warm\n    w_fast = u_hot\n\n    # 3. Defuzzification via Weighted Average Centroid\n    slow_center = 25.0\n    medium_center = 50.0\n    fast_center = 85.0\n\n    numerator = (w_slow * slow_center) + (w_medium * medium_center) + (w_fast * fast_center)\n    denominator = w_slow + w_medium + w_fast\n\n    if denominator == 0:\n        return 0.0\n    return numerator / denominator\n\nif __name__ == \"__main__\":\n    print(\"=\" * 60)\n    print(\" LabX Exp 10: Fuzzy Control System (Fan Speed Controller)\")\n    print(\"=\" * 60)\n\n    # Allow custom CLI argument or interactive input\n    if len(sys.argv) > 1:\n        try:\n            temp = float(sys.argv[1])\n        except ValueError:\n            temp = 28.0\n    else:\n        temp = 28.0\n\n    print(f\"Input Room Temperature: {temp:.1f} deg C\")\n    fan_speed = simulate_fan_controller(temp)\n    print(f\"Computed Fan Speed    : {fan_speed:.2f} %\")\n    print(\"=\" * 60)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Fuzzy control systems use linguistic variables and membership functions to\n# map crisp inputs to fuzzy sets. Rules are expressed in IF-THEN form,\n# combining antecedents with AND/OR operators to produce fuzzy outputs.\n# Defuzzification (e.g., centroid) converts the aggregated fuzzy output back\n# to a crisp control action. The system handles uncertainty by allowing\n# partial membership, enabling smoother transitions than binary logic.\n# ============================================================================\n"
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
        "aliases": [
            "genetic algorithm",
            "simulated annealing",
            "optimization",
            "metaheuristic",
            "ga"
        ],
        "description": "Population-based Genetic Algorithm and stochastic Simulated Annealing for non-linear function optimization.",
        "aim": "To implement Genetic Algorithm and Simulated Annealing metaheuristics for continuous optimization.",
        "theory": "Genetic algorithms mimic biological evolution: a population of candidate solutions is evolved through selection, crossover, and mutation to optimize a fitness function. Simulated annealing mimics physical annealing: a single solution is iteratively perturbed and accepted with a probability that decreases with temperature, allowing escape from local optima. Both methods rely on stochastic search and balance exploration with exploitation. Key parameters: population size, crossover/mutation rates for GA; cooling schedule and acceptance probability for SA.",
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
                "content": "import random\nimport math\n\ndef fitness(x):\n    # Sphere function: global minimum at x = 0\n    return x ** 2\n\ndef run_genetic_algorithm(pop_size=20, generations=50, mutation_rate=0.1):\n    population = [random.uniform(-10, 10) for _ in range(pop_size)]\n\n    for gen in range(generations):\n        population.sort(key=fitness)\n        parents = population[:2]\n\n        # Crossover\n        child = (parents[0] + parents[1]) / 2.0\n\n        # Mutation\n        if random.random() < mutation_rate:\n            child += random.uniform(-1.0, 1.0)\n        child = max(-10.0, min(10.0, child))\n\n        population[-1] = child\n\n    best = min(population, key=fitness)\n    return best, fitness(best)\n\ndef run_simulated_annealing(initial_temp=100.0, cooling_rate=0.95, iterations=100):\n    current = random.uniform(-10, 10)\n    current_cost = fitness(current)\n    temp = initial_temp\n\n    for _ in range(iterations):\n        neighbor = current + random.uniform(-1.0, 1.0)\n        neighbor_cost = fitness(neighbor)\n        delta = neighbor_cost - current_cost\n\n        if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-6)):\n            current = neighbor\n            current_cost = neighbor_cost\n\n        temp *= cooling_rate\n\n    return current, current_cost\n\nif __name__ == \"__main__\":\n    print(\"=\" * 60)\n    print(\" LabX Exp 11: Genetic Algorithm & Simulated Annealing\")\n    print(\"=\" * 60)\n\n    ga_x, ga_fit = run_genetic_algorithm()\n    print(f\"Genetic Algorithm Result       : x = {ga_x:.6f}, f(x) = {ga_fit:.6f}\")\n\n    sa_x, sa_fit = run_simulated_annealing()\n    print(f\"Simulated Annealing Result     : x = {sa_x:.6f}, f(x) = {sa_fit:.6f}\")\n    print(\"=\" * 60)\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# Genetic algorithms mimic biological evolution: a population of candidate\n# solutions is evolved through selection, crossover, and mutation to\n# optimize a fitness function. Simulated annealing mimics physical\n# annealing: a single solution is iteratively perturbed and accepted with a\n# probability that decreases with temperature, allowing escape from local\n# optima. Both methods rely on stochastic search and balance exploration\n# with exploitation. Key parameters: population size, crossover/mutation\n# rates for GA; cooling schedule and acceptance probability for SA.\n# ============================================================================\n"
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
        "aliases": [
            "n8n",
            "ai automation",
            "agent workflow",
            "n8n agent",
            "automation agent"
        ],
        "description": "AI Agent automation framework simulating n8n node routing, LLM intent parsing, and automated tool triggering.",
        "aim": "To create an AI agent for automation using node-based workflow tools like n8n.",
        "theory": "n8n is a workflow automation tool that uses nodes to connect services via APIs. An AI agent can be built by creating a node that sends user input to an LLM (e.g., OpenAI) and processes the response. The workflow then routes the LLM output to subsequent nodes that perform actions like sending emails, updating databases, or triggering other APIs. By chaining these nodes, the agent can interpret natural language commands and execute complex automation tasks.",
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
                "content": "import json\nimport time\n\nclass N8nNode:\n    def __init__(self, name: str, node_type: str):\n        self.name = name\n        self.node_type = node_type\n\n    def execute(self, payload: dict) -> dict:\n        print(f\"  [Node: {self.name} ({self.node_type})] Executing...\")\n        time.sleep(0.1)\n        return payload\n\nclass N8nWorkflowAgent:\n    def __init__(self):\n        self.nodes = {\n            \"webhook\": N8nNode(\"Webhook Trigger\", \"n8n-nodes-base.webhook\"),\n            \"llm\": N8nNode(\"AI Agent LLM Parser\", \"@n8n/n8n-nodes-langchain.agent\"),\n            \"email\": N8nNode(\"Send Email Notification\", \"n8n-nodes-base.emailSend\"),\n            \"database\": N8nNode(\"PostgreSQL Logger\", \"n8n-nodes-base.postgres\")\n        }\n\n    def process_command(self, user_command: str):\n        print(f\"\\nProcessing Inbound Task: \\\"{user_command}\\\"\")\n        print(\"-\" * 50)\n\n        # 1. Trigger\n        data = self.nodes[\"webhook\"].execute({\"raw_input\": user_command, \"timestamp\": time.time()})\n\n        # 2. LLM Intent Extraction\n        if \"email\" in user_command.lower() or \"alert\" in user_command.lower():\n            intent = \"SEND_EMAIL\"\n            params = {\"recipient\": \"admin@college.edu\", \"subject\": \"Automated Alert\", \"body\": user_command}\n        else:\n            intent = \"DATABASE_LOG\"\n            params = {\"table\": \"system_events\", \"record\": user_command}\n\n        llm_data = self.nodes[\"llm\"].execute({\"intent\": intent, \"params\": params})\n\n        # 3. Dynamic Node Routing\n        if intent == \"SEND_EMAIL\":\n            self.nodes[\"email\"].execute(llm_data[\"params\"])\n            print(\"  --> Email successfully dispatched via n8n worker node.\")\n        else:\n            self.nodes[\"database\"].execute(llm_data[\"params\"])\n            print(\"  --> Record committed to database via n8n SQL node.\")\n\n        print(\"-\" * 50)\n        print(\"[SUCCESS] n8n AI Agent Workflow Completed!\")\n\ndef main():\n    print(\"=\" * 60)\n    print(\" LabX Exp 12: AI Agent for Automation using n8n\")\n    print(\"=\" * 60)\n\n    workflow = N8nWorkflowAgent()\n    workflow.process_command(\"Send urgent email alert about lab attendance drop\")\n    workflow.process_command(\"Log daily laboratory usage telemetry\")\n    print(\"=\" * 60)\n\nif __name__ == \"__main__\":\n    main()\n\n# ============================================================================\n# EXPERIMENT THEORY (from AISC Laboratory Submission):\n# ============================================================================\n# n8n is a workflow automation tool that uses nodes to connect services via\n# APIs. An AI agent can be built by creating a node that sends user input to\n# an LLM (e.g., OpenAI) and processes the response. The workflow then routes\n# the LLM output to subsequent nodes that perform actions like sending\n# emails, updating databases, or triggering other APIs. By chaining these\n# nodes, the agent can interpret natural language commands and execute\n# complex automation tasks.\n# ============================================================================\n"
            },
            {
                "path": "n8n_workflow.json",
                "source": "n8n_workflow.json",
                "role": "config",
                "content": "{\n  \"name\": \"LabX AI Agent Automation\",\n  \"nodes\": [\n    {\n      \"parameters\": {\"path\": \"labx-webhook\"},\n      \"name\": \"Webhook\",\n      \"type\": \"n8n-nodes-base.webhook\",\n      \"position\": [250, 300]\n    },\n    {\n      \"parameters\": {\"model\": \"gpt-4o\"},\n      \"name\": \"AI Agent\",\n      \"type\": \"@n8n/n8n-nodes-langchain.agent\",\n      \"position\": [450, 300]\n    },\n    {\n      \"parameters\": {\"toEmail\": \"admin@college.edu\"},\n      \"name\": \"Email\",\n      \"type\": \"n8n-nodes-base.emailSend\",\n      \"position\": [700, 200]\n    }\n  ]\n}\n"
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
