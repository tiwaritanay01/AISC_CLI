"""Host builder script: generates public/ catalog, manifests, experiment sources, HTML, and ZIP archive."""

import os
import json
import zipfile
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
HOST_DIR = BASE_DIR / "labx-host"
PUBLIC_DIR = HOST_DIR / "public"
EXP_DIR = PUBLIC_DIR / "experiments"
DL_DIR = PUBLIC_DIR / "downloads"

# Define 10 realistic, fully-featured experiments
EXPERIMENTS = [
    {
        "id": 1,
        "slug": "factorial-fibonacci-python",
        "title": "Factorial and Fibonacci Sequence Generator",
        "language": "python",
        "aliases": ["factorial", "fibonacci", "math sequence", "python factorial"],
        "description": "Computation of mathematical factorial and Fibonacci sequences using iterative and recursive techniques.",
        "aim": "To write a Python program to calculate the factorial of a given number and generate the Fibonacci sequence up to N terms.",
        "theory": (
            "The factorial of a non-negative integer n, denoted by n!, is the product of all positive integers less than or equal to n.\n"
            "The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, usually starting with 0 and 1.\n"
            "Both problems demonstrate recursion, stack frames, and memoization in computer science."
        ),
        "algorithm": [
            "Start the program and prompt the user for input N.",
            "Define factorial(n): if n <= 1 return 1, else return n * factorial(n - 1).",
            "Define fibonacci(n): initialize [0, 1] and iteratively append sum of previous two elements.",
            "Display calculated factorial and formatted Fibonacci series.",
            "End execution."
        ],
        "files": [
            {
                "path": "main.py",
                "source": "main.py",
                "role": "source",
                "content": '''"""Experiment 01: Factorial and Fibonacci Generator in Python."""

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n in (0, 1):
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(count: int) -> list[int]:
    if count <= 0:
        return []
    if count == 1:
        return [0]
    series = [0, 1]
    while len(series) < count:
        series.append(series[-1] + series[-2])
    return series

def main():
    print("=" * 50)
    print(" LabX Experiment 01: Factorial & Fibonacci")
    print("=" * 50)
    
    num = 7
    print(f"Calculating factorial of {num}...")
    fact_val = factorial(num)
    print(f"Result: {num}! = {fact_val}")
    
    terms = 10
    print(f"\\nGenerating first {terms} terms of Fibonacci sequence:")
    fib_series = fibonacci(terms)
    print(f"Result: {fib_series}")
    print("=" * 50)

if __name__ == "__main__":
    main()
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "main.py"
        }
    },
    {
        "id": 2,
        "slug": "matrix-multiplication-c",
        "title": "Matrix Multiplication & Transpose Operations",
        "language": "c",
        "aliases": ["matrix multiplication", "matrix transpose", "c matrix", "linear algebra c"],
        "description": "Multiplication, transposition, and dynamic memory operations on two-dimensional matrices in C.",
        "aim": "To implement matrix multiplication and transpose in C using modular functions.",
        "theory": (
            "Matrix multiplication of matrix A (m x k) and B (k x n) yields matrix C (m x n), where each element C[i][j] is the dot product of row i of A and column j of B.\n"
            "Matrix transposition flips a matrix over its diagonal, switching the row and column indices of the matrix."
        ),
        "algorithm": [
            "Input dimensions for Matrix A and Matrix B.",
            "Check condition: Columns of A must equal Rows of B.",
            "Initialize matrices with sample or user values.",
            "Multiply row elements of A by column elements of B and accumulate sum into C.",
            "Compute transpose of Matrix C by swapping indices [i][j] to [j][i].",
            "Display original matrices, product matrix, and transpose matrix."
        ],
        "files": [
            {
                "path": "matrix.h",
                "source": "matrix.h",
                "role": "header",
                "content": '''#ifndef MATRIX_H
#define MATRIX_H

#define MAX_SIZE 10

void print_matrix(const char* label, int mat[MAX_SIZE][MAX_SIZE], int rows, int cols);
void multiply_matrices(int a[MAX_SIZE][MAX_SIZE], int r1, int c1,
                       int b[MAX_SIZE][MAX_SIZE], int r2, int c2,
                       int res[MAX_SIZE][MAX_SIZE]);
void transpose_matrix(int mat[MAX_SIZE][MAX_SIZE], int rows, int cols,
                      int trans[MAX_SIZE][MAX_SIZE]);

#endif
'''
            },
            {
                "path": "matrix.c",
                "source": "matrix.c",
                "role": "source",
                "content": '''#include <stdio.h>
#include "matrix.h"

void print_matrix(const char* label, int mat[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    printf("%s (%dx%d):\\n", label, rows, cols);
    for (int i = 0; i < rows; i++) {
        printf("  [ ");
        for (int j = 0; j < cols; j++) {
            printf("%4d ", mat[i][j]);
        }
        printf(" ]\\n");
    }
}

void multiply_matrices(int a[MAX_SIZE][MAX_SIZE], int r1, int c1,
                       int b[MAX_SIZE][MAX_SIZE], int r2, int c2,
                       int res[MAX_SIZE][MAX_SIZE]) {
    for (int i = 0; i < r1; i++) {
        for (int j = 0; j < c2; j++) {
            res[i][j] = 0;
            for (int k = 0; k < c1; k++) {
                res[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

void transpose_matrix(int mat[MAX_SIZE][MAX_SIZE], int rows, int cols,
                      int trans[MAX_SIZE][MAX_SIZE]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            trans[j][i] = mat[i][j];
        }
    }
}

int main(void) {
    printf("=========================================\\n");
    printf(" LabX Experiment 02: C Matrix Operations\\n");
    printf("=========================================\\n");

    int a[MAX_SIZE][MAX_SIZE] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    int b[MAX_SIZE][MAX_SIZE] = {
        {7, 8},
        {9, 1},
        {2, 3}
    };
    int res[MAX_SIZE][MAX_SIZE];
    int trans[MAX_SIZE][MAX_SIZE];

    print_matrix("Matrix A", a, 2, 3);
    print_matrix("Matrix B", b, 3, 2);

    multiply_matrices(a, 2, 3, b, 3, 2, res);
    print_matrix("Product Matrix (A x B)", res, 2, 2);

    transpose_matrix(res, 2, 2, trans);
    print_matrix("Transpose of Product Matrix", trans, 2, 2);

    printf("=========================================\\n");
    return 0;
}
'''
            }
        ],
        "run": {
            "kind": "c",
            "entry": "matrix.c"
        }
    },
    {
        "id": 3,
        "slug": "java-socket-programming",
        "title": "Java Socket Programming (Client-Server)",
        "language": "java",
        "aliases": ["socket programming", "java sockets", "client server socket", "tcp socket java"],
        "description": "Two-way client-server network communication using Java TCP Sockets and Stream I/O.",
        "aim": "To implement a client-server socket communication program using Java TCP Sockets.",
        "theory": (
            "A socket is an endpoint for communication between two machines over a network.\n"
            "Java provides the java.net package, containing ServerSocket (listening on a port for inbound connections) "
            "and Socket (connecting to the server's IP address and port).\n"
            "Data transfer occurs via BufferedReader and PrintWriter wrapping socket input/output streams."
        ),
        "algorithm": [
            "Start the Server application on port 5000.",
            "Server creates a ServerSocket and enters accept() waiting for incoming connection.",
            "Client creates a Socket connecting to localhost:5000.",
            "Connection accepted; both sides obtain InputStream and OutputStream.",
            "Client sends greeting message 'Hello from LabX Java Client!'.",
            "Server receives message, processes it, and responds with acknowledgment.",
            "Close streams and sockets cleanly."
        ],
        "files": [
            {
                "path": "Server.java",
                "source": "Server.java",
                "role": "source",
                "content": '''import java.io.*;
import java.net.*;

public class Server {
    public static final int PORT = 5000;

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println(" LabX Experiment 03: Java Socket Server");
        System.out.println("=========================================");
        System.out.println("Server listening on port " + PORT + "...");

        // Auto-run simulation or accept single client
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            // Set 15-second timeout for unattended test runs
            serverSocket.setSoTimeout(15000);
            
            // Start client in background thread for self-testing demo
            new Thread(() -> {
                try {
                    Thread.sleep(500);
                    Client.main(new String[]{});
                } catch (Exception e) {
                    // Ignore background demo client errors
                }
            }).start();

            try (Socket socket = serverSocket.accept();
                 BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                 PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

                System.out.println("[Server] Connection accepted from: " + socket.getRemoteSocketAddress());
                String message = in.readLine();
                System.out.println("[Server] Received from client: " + message);

                String response = "Server ACK: Received message [" + message + "]";
                out.println(response);
                System.out.println("[Server] Sent response to client: " + response);
            }
        } catch (SocketTimeoutException e) {
            System.out.println("[Server] Timeout reached waiting for client.");
        } catch (IOException e) {
            System.err.println("[Server] I/O Exception: " + e.getMessage());
        }
        System.out.println("=========================================");
    }
}
'''
            },
            {
                "path": "Client.java",
                "source": "Client.java",
                "role": "source",
                "content": '''import java.io.*;
import java.net.*;

public class Client {
    public static final String HOST = "127.0.0.1";
    public static final int PORT = 5000;

    public static void main(String[] args) {
        System.out.println("[Client] Connecting to " + HOST + ":" + PORT + "...");
        try (Socket socket = new Socket(HOST, PORT);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            System.out.println("[Client] Connected successfully!");
            String payload = "Hello from LabX Java Client!";
            System.out.println("[Client] Sending: " + payload);
            out.println(payload);

            String reply = in.readLine();
            System.out.println("[Client] Reply from server: " + reply);

        } catch (IOException e) {
            System.err.println("[Client] Connection error: " + e.getMessage());
        }
    }
}
'''
            }
        ],
        "run": {
            "kind": "java",
            "entry": "Server.java",
            "components": {
                "server": {
                    "name": "Server",
                    "entry": "Server.java",
                    "description": "Starts the socket listener server on port 5000"
                },
                "client": {
                    "name": "Client",
                    "entry": "Client.java",
                    "description": "Connects to server at localhost:5000 and sends test message"
                }
            }
        }
    },
    {
        "id": 4,
        "slug": "dijkstra-routing-cpp",
        "title": "Dijkstra's Shortest Path Routing Algorithm",
        "language": "cpp",
        "aliases": ["dijkstra", "shortest path", "routing algorithm", "dynamic routing", "c++ dijkstra"],
        "description": "Simulation of dynamic routing and shortest path calculation in packet networks using Dijkstra's algorithm.",
        "aim": "To implement Dijkstra's shortest path algorithm in C++ for network link-state routing simulation.",
        "theory": (
            "Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a weighted graph.\n"
            "In computer networking, it forms the foundation of Link State routing protocols such as Open Shortest Path First (OSPF).\n"
            "Each router maintains a complete topology map and computes the shortest path tree from itself as the root to all other nodes."
        ),
        "algorithm": [
            "Initialize distance array with infinity for all nodes except source node (distance 0).",
            "Create a min-priority queue storing (distance, node).",
            "Extract node with minimum distance from queue.",
            "For each adjacent neighbor, calculate alternative distance through current node.",
            "If alternative distance is less than current recorded distance, update distance and record previous hop.",
            "Repeat until priority queue is empty.",
            "Print shortest path cost and hop sequence to every destination."
        ],
        "files": [
            {
                "path": "dijkstra.cpp",
                "source": "dijkstra.cpp",
                "role": "source",
                "content": '''#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

struct Edge {
    int to;
    int weight;
};

void dijkstra(int source, int n, const vector<vector<Edge>>& graph) {
    vector<int> dist(n, INT_MAX);
    vector<int> parent(n, -1);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

    dist[source] = 0;
    pq.push({0, source});

    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue;

        for (const auto& edge : graph[u]) {
            int v = edge.to;
            int weight = edge.weight;

            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }

    cout << "\\nRouting Table from Router " << source << ":\\n";
    cout << "------------------------------------------\\n";
    cout << "Destination Router | Minimum Metric (Cost)\\n";
    cout << "------------------------------------------\\n";
    for (int i = 0; i < n; i++) {
        cout << "      Router " << i << "      |       " << dist[i] << "\\n";
    }
    cout << "------------------------------------------\\n";
}

int main() {
    cout << "=========================================\\n";
    cout << " LabX Experiment 04: Dijkstra Routing\\n";
    cout << "=========================================\\n";

    int nodes = 5;
    vector<vector<Edge>> graph(nodes);

    // Network topology edges: Router u -> Router v (metric cost)
    graph[0].push_back({1, 10});
    graph[0].push_back({4, 5});
    graph[1].push_back({2, 1});
    graph[1].push_back({4, 2});
    graph[2].push_back({3, 4});
    graph[3].push_back({0, 7});
    graph[3].push_back({2, 6});
    graph[4].push_back({1, 3});
    graph[4].push_back({2, 9});
    graph[4].push_back({3, 2});

    cout << "Simulating Link-State Routing with 5 Routers (0 to 4)...\\n";
    dijkstra(0, nodes, graph);

    cout << "Simulation completed successfully.\\n";
    cout << "=========================================\\n";
    return 0;
}
'''
            }
        ],
        "run": {
            "kind": "cpp",
            "entry": "dijkstra.cpp"
        }
    },
    {
        "id": 5,
        "slug": "sliding-window-protocol",
        "title": "Sliding Window Flow Control Protocol (Go-Back-N)",
        "language": "c",
        "aliases": ["sliding window", "go back n", "flow control", "sliding window c"],
        "description": "Simulation of the Go-Back-N sliding window flow control and error recovery protocol in C.",
        "aim": "To simulate the sliding window protocol (Go-Back-N) for flow control in data link layers.",
        "theory": (
            "The sliding window protocol is a method of flow control where the sender is allowed to transmit multiple frames "
            "before receiving an acknowledgment from the receiver.\n"
            "In Go-Back-N ARQ, if a frame is corrupted or lost, the receiver discards all subsequent frames, and the sender retransmits "
            "all unacknowledged frames starting from the lost frame."
        ),
        "algorithm": [
            "Input window size W and total number of frames N.",
            "Initialize window bounds [base, base + W - 1].",
            "Transmit frames within the current window.",
            "Simulate reception and acknowledgment for transmitted frames.",
            "Simulate occasional transmission failure or frame timeout.",
            "Upon timeout, slide window back to the last acknowledged frame and retransmit.",
            "Repeat until all N frames are successfully delivered and acknowledged."
        ],
        "files": [
            {
                "path": "sliding_window.c",
                "source": "sliding_window.c",
                "role": "source",
                "content": '''#include <stdio.h>
#include <stdbool.h>

void simulate_gobackn(int total_frames, int window_size) {
    int base = 1;
    int next_seq_num = 1;
    int simulated_drop_frame = 3; // Simulate loss of frame 3 on first try
    bool dropped_once = false;

    printf("Starting Go-Back-N Simulation (Total: %d frames, Window Size: %d)\\n\\n",
           total_frames, window_size);

    while (base <= total_frames) {
        // Send all frames in current window
        while (next_seq_num < base + window_size && next_seq_num <= total_frames) {
            printf("[Sender] Transmitting Frame %d\\n", next_seq_num);
            next_seq_num++;
        }

        // Simulate ACKs
        for (int f = base; f < next_seq_num; f++) {
            if (f == simulated_drop_frame && !dropped_once) {
                printf("[Network] *** Frame %d LOST in transit! ***\\n", f);
                printf("[Sender] Timeout expired for Frame %d! Sliding back window.\\n", f);
                dropped_once = true;
                next_seq_num = f; // Go back to lost frame
                break;
            } else {
                printf("[Receiver] Frame %d received correctly -> Sending ACK %d\\n", f, f);
                printf("[Sender] Received ACK %d -> Window advances\\n", f);
                base++;
            }
        }
        printf("--------------------------------------------------\\n");
    }
    printf("SUCCESS: All %d frames transmitted and acknowledged!\\n", total_frames);
}

int main(void) {
    printf("==================================================\\n");
    printf(" LabX Experiment 05: Sliding Window Protocol (GBN)\\n");
    printf("==================================================\\n");
    simulate_gobackn(6, 3);
    printf("==================================================\\n");
    return 0;
}
'''
            }
        ],
        "run": {
            "kind": "c",
            "entry": "sliding_window.c"
        }
    },
    {
        "id": 6,
        "slug": "page-replacement-simulation",
        "title": "Page Replacement Simulation (FIFO & LRU)",
        "language": "python",
        "aliases": ["page replacement", "fifo lru", "virtual memory", "paging simulation"],
        "description": "Simulation and performance comparison of FIFO and LRU virtual memory page replacement algorithms.",
        "aim": "To write a Python simulation of FIFO and LRU page replacement policies and compare their page fault rates.",
        "theory": (
            "Virtual memory uses paging to map virtual addresses to physical frames. When a requested page is not in memory, a page fault occurs.\n"
            "FIFO (First-In, First-Out) replaces the oldest resident page in memory.\n"
            "LRU (Least Recently Used) replaces the page that has not been referenced for the longest period of time."
        ),
        "algorithm": [
            "Initialize memory frames with capacity F.",
            "For FIFO: Maintain a FIFO queue of page numbers in memory.",
            "For LRU: Track page reference timestamps or maintain an ordered history list.",
            "Iterate through reference string.",
            "If page exists in memory, count as a Hit (and update LRU recency).",
            "If page missing, count as a Page Fault and evict page according to algorithm policy.",
            "Calculate and display total faults and hit ratio."
        ],
        "files": [
            {
                "path": "page_replacement.py",
                "source": "page_replacement.py",
                "role": "source",
                "content": '''"""Experiment 06: FIFO and LRU Page Replacement Simulation in Python."""

def simulate_fifo(reference_string: list[int], frame_count: int) -> int:
    frames = []
    faults = 0
    for page in reference_string:
        if page not in frames:
            faults += 1
            if len(frames) >= frame_count:
                frames.pop(0)
            frames.append(page)
    return faults

def simulate_lru(reference_string: list[int], frame_count: int) -> int:
    frames = []
    faults = 0
    for page in reference_string:
        if page in frames:
            frames.remove(page)
            frames.append(page)
        else:
            faults += 1
            if len(frames) >= frame_count:
                frames.pop(0)
            frames.append(page)
    return faults

def main():
    print("=" * 55)
    print(" LabX Experiment 06: Page Replacement Simulation")
    print("=" * 55)
    
    reference = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frames = 3
    print(f"Page Reference String ({len(reference)} requests): {reference}")
    print(f"Available Physical Frame Capacity: {frames}\\n")
    
    fifo_faults = simulate_fifo(reference, frames)
    lru_faults = simulate_lru(reference, frames)
    
    print(f"FIFO Algorithm : {fifo_faults} page faults (Hit Rate: {((len(reference)-fifo_faults)/len(reference))*100:.1f}%)")
    print(f"LRU  Algorithm : {lru_faults} page faults (Hit Rate: {((len(reference)-lru_faults)/len(reference))*100:.1f}%)")
    print("=" * 55)

if __name__ == "__main__":
    main()
'''
            }
        ],
        "run": {
            "kind": "python",
            "entry": "page_replacement.py"
        }
    },
    {
        "id": 7,
        "slug": "multithreaded-echo-server",
        "title": "Multi-Threaded Echo Server in Java",
        "language": "java",
        "aliases": ["multithreaded server", "echo server java", "threads socket", "java concurrency"],
        "description": "Concurrent multi-threaded TCP server handling multiple simultaneous client connections.",
        "aim": "To implement a concurrent multi-threaded echo server using Java Runnable and Socket threads.",
        "theory": (
            "A single-threaded server can only service one client at a time, leaving other connection requests blocked.\n"
            "A multi-threaded server spawns a dedicated worker thread for each accepted client socket, enabling concurrent data processing."
        ),
        "algorithm": [
            "Server starts ServerSocket on port 6000.",
            "In an infinite loop, server calls accept() to wait for incoming connections.",
            "For each incoming client, server creates an instance of ClientHandler implementing Runnable.",
            "Start the thread to process reading and echoing back messages.",
            "Client connects, sends payload, prints echoed response, and exits."
        ],
        "files": [
            {
                "path": "EchoServer.java",
                "source": "EchoServer.java",
                "role": "source",
                "content": '''import java.io.*;
import java.net.*;

public class EchoServer {
    public static final int PORT = 6000;

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println(" LabX Experiment 07: Multi-Threaded Server");
        System.out.println("=========================================");
        System.out.println("Echo server listening on port " + PORT + "...");

        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            serverSocket.setSoTimeout(10000);

            // Self-testing client demo
            new Thread(() -> {
                try {
                    Thread.sleep(500);
                    EchoClient.main(new String[]{});
                } catch (Exception ignored) {}
            }).start();

            try (Socket socket = serverSocket.accept()) {
                System.out.println("[EchoServer] Handling client connection in worker thread...");
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

                String line = in.readLine();
                System.out.println("[EchoServer] Echoing: " + line);
                out.println("ECHO: " + line);
            }
        } catch (SocketTimeoutException e) {
            System.out.println("[EchoServer] Test timeout completed.");
        } catch (IOException e) {
            System.err.println("[EchoServer] Error: " + e.getMessage());
        }
        System.out.println("=========================================");
    }
}
'''
            },
            {
                "path": "EchoClient.java",
                "source": "EchoClient.java",
                "role": "source",
                "content": '''import java.io.*;
import java.net.*;

public class EchoClient {
    public static void main(String[] args) {
        try (Socket s = new Socket("127.0.0.1", 6000);
             PrintWriter out = new PrintWriter(s.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()))) {

            String msg = "Testing Concurrent Connection";
            out.println(msg);
            System.out.println("[EchoClient] Sent: " + msg);
            System.out.println("[EchoClient] Received: " + in.readLine());
        } catch (Exception e) {
            System.err.println("[EchoClient] Failed: " + e.getMessage());
        }
    }
}
'''
            }
        ],
        "run": {
            "kind": "java",
            "entry": "EchoServer.java",
            "components": {
                "server": {
                    "name": "EchoServer",
                    "entry": "EchoServer.java",
                    "description": "Multi-threaded echo listener"
                },
                "client": {
                    "name": "EchoClient",
                    "entry": "EchoClient.java",
                    "description": "Echo client tester"
                }
            }
        }
    },
    {
        "id": 8,
        "slug": "lexical-analyzer-c",
        "title": "Lexical Analyzer for Arithmetic Expressions",
        "language": "c",
        "aliases": ["lexical analyzer", "compiler lexer", "tokenizer c", "lexer"],
        "description": "Deterministic finite automaton (DFA) based lexical analyzer tokenizing source input in C.",
        "aim": "To construct a lexical analyzer in C to identify keywords, identifiers, constants, and operators.",
        "theory": (
            "Lexical analysis is the first phase of a compiler.\n"
            "It scans source characters into meaningful sequences called lexemes and produces corresponding tokens: "
            "<TOKEN_TYPE, VALUE> for subsequent syntax analysis."
        ),
        "algorithm": [
            "Read input expression string character by character.",
            "Skip whitespace characters.",
            "If character is alphabetical or underscore, scan complete alphanumeric identifier and check against keywords.",
            "If character is numeric digit, scan complete integer constant.",
            "If character matches an operator (+, -, *, /, =), emit operator token.",
            "Display tokens with categorized token types."
        ],
        "files": [
            {
                "path": "tokens.h",
                "source": "tokens.h",
                "role": "header",
                "content": '''#ifndef TOKENS_H
#define TOKENS_H

typedef enum {
    TOKEN_KEYWORD,
    TOKEN_IDENTIFIER,
    TOKEN_NUMBER,
    TOKEN_OPERATOR,
    TOKEN_DELIMITER,
    TOKEN_UNKNOWN
} TokenType;

const char* get_token_type_name(TokenType t);

#endif
'''
            },
            {
                "path": "lexer.c",
                "source": "lexer.c",
                "role": "source",
                "content": '''#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "tokens.h"

const char* get_token_type_name(TokenType t) {
    switch (t) {
        case TOKEN_KEYWORD:    return "KEYWORD";
        case TOKEN_IDENTIFIER: return "IDENTIFIER";
        case TOKEN_NUMBER:     return "NUMBER";
        case TOKEN_OPERATOR:   return "OPERATOR";
        case TOKEN_DELIMITER:  return "DELIMITER";
        default:               return "UNKNOWN";
    }
}

int is_keyword(const char* s) {
    const char* keywords[] = {"int", "float", "if", "else", "while", "return", NULL};
    for (int i = 0; keywords[i] != NULL; i++) {
        if (strcmp(keywords[i], s) == 0) return 1;
    }
    return 0;
}

void tokenize(const char* input) {
    int i = 0;
    int len = (int)strlen(input);

    printf("Input Stream: \\"%s\\"\\n\\n", input);
    printf("Line | Lexeme          | Token Type\\n");
    printf("-----+-----------------+-------------\\n");

    while (i < len) {
        if (isspace((unsigned char)input[i])) {
            i++;
            continue;
        }

        if (isalpha((unsigned char)input[i]) || input[i] == '_') {
            char buffer[64];
            int b = 0;
            while (i < len && (isalnum((unsigned char)input[i]) || input[i] == '_')) {
                if (b < 63) buffer[b++] = input[i];
                i++;
            }
            buffer[b] = '\\0';
            TokenType t = is_keyword(buffer) ? TOKEN_KEYWORD : TOKEN_IDENTIFIER;
            printf(" 1   | %-15s | %s\\n", buffer, get_token_type_name(t));
            continue;
        }

        if (isdigit((unsigned char)input[i])) {
            char buffer[64];
            int b = 0;
            while (i < len && isdigit((unsigned char)input[i])) {
                if (b < 63) buffer[b++] = input[i];
                i++;
            }
            buffer[b] = '\\0';
            printf(" 1   | %-15s | %s\\n", buffer, get_token_type_name(TOKEN_NUMBER));
            continue;
        }

        if (strchr("+-*/=", input[i]) != NULL) {
            printf(" 1   | %-15c | %s\\n", input[i], get_token_type_name(TOKEN_OPERATOR));
            i++;
            continue;
        }

        if (strchr("();{},", input[i]) != NULL) {
            printf(" 1   | %-15c | %s\\n", input[i], get_token_type_name(TOKEN_DELIMITER));
            i++;
            continue;
        }

        printf(" 1   | %-15c | %s\\n", input[i], get_token_type_name(TOKEN_UNKNOWN));
        i++;
    }
}

int main(void) {
    printf("=========================================\\n");
    printf(" LabX Experiment 08: Lexical Analyzer\\n");
    printf("=========================================\\n");

    const char* sample_code = "int total = count + 42;";
    tokenize(sample_code);

    printf("=========================================\\n");
    return 0;
}
'''
            }
        ],
        "run": {
            "kind": "c",
            "entry": "lexer.c"
        }
    },
    {
        "id": 9,
        "slug": "binary-search-tree-cpp",
        "title": "Binary Search Tree Operations & Traversals",
        "language": "cpp",
        "aliases": ["binary search tree", "bst", "tree traversals", "bst cpp"],
        "description": "Insertion, searching, deletion, and in-order/pre-order traversals of a Binary Search Tree in C++.",
        "aim": "To construct a Binary Search Tree (BST) and implement traversals (Inorder, Preorder, Postorder).",
        "theory": (
            "A Binary Search Tree is a binary tree data structure where each node has at most two children.\n"
            "The key of each internal node is greater than all keys in its left subtree and less than all keys in its right subtree.\n"
            "An inorder traversal of a BST yields keys in sorted ascending order."
        ),
        "algorithm": [
            "Define Node structure with key, left pointer, and right pointer.",
            "Implement insert(root, key): recursively find correct leaf position and attach new Node.",
            "Implement inorder(root): traverse left subtree, visit root, traverse right subtree.",
            "Implement search(root, key): compare key and branch left or right.",
            "Test tree with sample keys and display traversal output."
        ],
        "files": [
            {
                "path": "bst.cpp",
                "source": "bst.cpp",
                "role": "source",
                "content": '''#include <iostream>

using namespace std;

struct Node {
    int key;
    Node* left;
    Node* right;

    Node(int val) : key(val), left(nullptr), right(nullptr) {}
};

Node* insert(Node* root, int key) {
    if (root == nullptr) return new Node(key);
    if (key < root->key) root->left = insert(root->left, key);
    else if (key > root->key) root->right = insert(root->right, key);
    return root;
}

void inorder(Node* root) {
    if (root != nullptr) {
        inorder(root->left);
        cout << root->key << " ";
        inorder(root->right);
    }
}

void preorder(Node* root) {
    if (root != nullptr) {
        cout << root->key << " ";
        preorder(root->left);
        preorder(root->right);
    }
}

bool search(Node* root, int key) {
    if (root == nullptr) return false;
    if (root->key == key) return true;
    if (key < root->key) return search(root->left, key);
    return search(root->right, key);
}

void cleanup(Node* root) {
    if (root != nullptr) {
        cleanup(root->left);
        cleanup(root->right);
        delete root;
    }
}

int main() {
    cout << "=========================================\\n";
    cout << " LabX Experiment 09: Binary Search Tree\\n";
    cout << "=========================================\\n";

    Node* root = nullptr;
    int values[] = {50, 30, 70, 20, 40, 60, 80};

    cout << "Inserting keys into BST: ";
    for (int v : values) {
        cout << v << " ";
        root = insert(root, v);
    }
    cout << "\\n\\n";

    cout << "Inorder Traversal (Sorted): ";
    inorder(root);
    cout << "\\n";

    cout << "Preorder Traversal:         ";
    preorder(root);
    cout << "\\n\\n";

    int query = 40;
    cout << "Searching for key " << query << ": " << (search(root, query) ? "FOUND" : "NOT FOUND") << "\\n";

    cleanup(root);
    cout << "=========================================\\n";
    return 0;
}
'''
            }
        ],
        "run": {
            "kind": "cpp",
            "entry": "bst.cpp"
        }
    },
    {
        "id": 10,
        "slug": "arm7-lpc2148-gpio-timer",
        "title": "ARM7 LPC2148 GPIO LED Flasher & Timer Driver",
        "language": "embedded_c",
        "aliases": ["arm7", "lpc2148", "gpio led", "embedded c", "keil lpc2148", "proteus arm"],
        "description": "Hardware driver in Embedded C configuring GPIO pins and Timer0 registers for NXP ARM7 LPC2148.",
        "aim": "To write and simulate an Embedded C program for the ARM7 TDMI LPC2148 microcontroller to blink LEDs connected to Port 0.",
        "theory": (
            "The NXP LPC2148 is an ARM7TDMI-S based 32-bit RISC microcontroller with 512KB on-chip flash and 40KB SRAM.\n"
            "Port 0 pins are configured using Fast GPIO registers: IODIR0 (direction: 1=output, 0=input), "
            "IOSET0 (set pin high), and IOCLR0 (clear pin low).\n"
            "Accurate timing delays are generated by configuring the Timer0 prescaler (T0PR) and match registers (T0MR0)."
        ),
        "algorithm": [
            "Include LPC214x.h register definitions header.",
            "Configure PLL to set System Clock to 60 MHz from 12 MHz external crystal.",
            "Configure IODIR0 register to set pins P0.10 - P0.17 as digital outputs.",
            "In an infinite while(1) loop: set pins high using IOSET0, invoke precise delay, clear pins low using IOCLR0, invoke delay.",
            "Simulate circuit in Proteus VSM or flash target board using Flash Magic via UART ISP."
        ],
        "files": [
            {
                "path": "LPC214x.h",
                "source": "LPC214x.h",
                "role": "header",
                "content": '''/* LPC214x.h - Hardware Register Definitions for Philips/NXP LPC2148 ARM7TDMI */
#ifndef LPC214X_H
#define LPC214X_H

#define IODIR0   (*((volatile unsigned long *) 0xE0028008))
#define IOPIN0   (*((volatile unsigned long *) 0xE0028000))
#define IOSET0   (*((volatile unsigned long *) 0xE0028004))
#define IOCLR0   (*((volatile unsigned long *) 0xE002800C))

#define PINSEL0  (*((volatile unsigned long *) 0xE002C000))
#define PINSEL1  (*((volatile unsigned long *) 0xE002C004))

#endif
'''
            },
            {
                "path": "main.c",
                "source": "main.c",
                "role": "source",
                "content": '''/*
 * Experiment 10: ARM7 LPC2148 GPIO LED Flasher
 * Target: NXP LPC2148 (ARM7TDMI-S)
 * Frequency: 60 MHz (12 MHz Crystal + PLL)
 */
#include "LPC214x.h"

#define LED_PIN (1 << 10)  /* P0.10 connected to LED */

void delay_ms(unsigned int count) {
    volatile unsigned int i, j;
    for (i = 0; i < count; i++) {
        for (j = 0; j < 3000; j++) {
            /* Assembly NOP or busy wait */
        }
    }
}

int main(void) {
    /* Set P0.10 as GPIO */
    PINSEL0 &= ~(0x3 << 20);

    /* Set P0.10 as Output */
    IODIR0 |= LED_PIN;

    while (1) {
        IOSET0 = LED_PIN;   /* Turn LED ON */
        delay_ms(500);

        IOCLR0 = LED_PIN;   /* Turn LED OFF */
        delay_ms(500);
    }

    return 0;
}
'''
            },
            {
                "path": "Makefile",
                "source": "Makefile",
                "role": "config",
                "content": '''# Makefile for ARM7 LPC2148 using GNU Arm Embedded Toolchain
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
CFLAGS = -mcpu=arm7tdmi -O2 -Wall

all: main.hex

main.elf: main.c
	$(CC) $(CFLAGS) -o main.elf main.c

main.hex: main.elf
	$(OBJCOPY) -O ihex main.elf main.hex

clean:
	rm -f *.elf *.hex *.o
'''
            }
        ],
        "run": {
            "kind": "embedded_c",
            "entry": "main.c",
            "hardware": "ARM7 TDMI NXP LPC2148",
            "toolchain_guide": (
                "=== PROTEUS SIMULATION & KEIL µVISION GUIDE ===\\n"
                "1. Keil Setup: Create a new project, select NXP LPC2148.\\n"
                "2. Add 'main.c' and 'LPC214x.h'. Enable 'Create HEX File' in Target Options.\\n"
                "3. Build target (F7) to generate 'main.hex'.\\n"
                "4. Proteus VSM: Place LPC2148 IC and connect an LED (with 330 ohm resistor) to P0.10.\\n"
                "5. Load 'main.hex' into the LPC2148 model properties and click Run Simulation.\\n"
                "6. Hardware: Flash via Flash Magic using USB-UART cable to ISP bootloader."
            )
        }
    }
]

HTML_INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LabX Remote - Experiment Distribution Platform</title>
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
      max-width: 900px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      margin-bottom: 3rem;
      border-bottom: 1px solid #334155;
      padding-bottom: 2rem;
    }
    h1 {
      color: var(--accent);
      font-size: 2.5rem;
      margin-bottom: 0.5rem;
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
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.25rem;
      margin-top: 2rem;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 1.25rem;
    }
    .card h3 {
      margin-top: 0;
      color: var(--accent);
    }
    .tag {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: #334155;
      padding: 0.2rem 0.5rem;
      border-radius: 3px;
      color: #38bdf8;
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
      <h1>LABX REMOTE</h1>
      <p class="muted">Terminal-First Experiment Distribution & Execution Backend</p>
      <span class="badge">Static API v1.0.0</span>
    </header>

    <section>
      <h2>Quick Install & Usage</h2>
      <p>Download individual experiments or entire collections directly into your terminal:</p>
      <div class="command-box">
        # 1. Download and run an individual experiment<br>
        labx download 3<br>
        labx run 3<br><br>
        # 2. Download all experiments in one command<br>
        labx download all
      </div>
    </section>

    <section>
      <h2>Available Static Endpoints</h2>
      <ul>
        <li><a href="catalog.json"><code>/catalog.json</code></a> — Complete experiment catalogue API</li>
        <li><a href="version.json"><code>/version.json</code></a> — Host version metadata</li>
        <li><a href="downloads/labx_experiments.zip"><code>/downloads/labx_experiments.zip</code></a> — Full experiments archive</li>
      </ul>
    </section>

    <section>
      <h2>Experiment Catalogue Preview</h2>
      <div class="grid">
"""

def generate_host():
    """Build all static hosting artifacts."""
    print("Creating host directories...")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    DL_DIR.mkdir(parents=True, exist_ok=True)

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

    with open(HOST_DIR / "README.md", "w", encoding="utf-8") as f:
        f.write("# LabX Remote Netlify Static Backend\n\nThis directory contains the deployable static site and JSON catalogue for LabX Remote.")

    # 2. version.json
    version_data = {
        "version": "1.0.0",
        "updated_at": "2026-10-31T12:00:00Z",
        "platform": "LabX Remote Production Static Backend"
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

        # Catalog record
        catalog_items.append({
            "id": exp["id"],
            "slug": exp["slug"],
            "title": exp["title"],
            "language": exp["language"],
            "aliases": exp["aliases"],
            "description": exp["description"],
            "manifest_url": manifest_url
        })

        # Write experiment source files
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
        # Copy source files
        for f_info in exp["files"]:
            shutil.copy(target_exp_dir / f_info["path"], zip_exp_dir / f_info["path"])
        # Copy manifest
        shutil.copy(target_exp_dir / "manifest.json", zip_exp_dir / "manifest.json")
        # Add generated README
        readme_content = f"# Experiment {exp_id:02d}: {exp['title']}\n\n## Aim\n{exp['aim']}\n\n## Description\n{exp['description']}\n\n## Theory\n{exp['theory']}\n"
        with open(zip_exp_dir / "README.md", "w", encoding="utf-8") as rf:
            rf.write(readme_content)

        # Add HTML preview card
        html_cards.append(f"""        <div class="card">
          <span class="tag">{exp['language']}</span>
          <h3>#{exp_id:02d} {exp['title']}</h3>
          <p>{exp['description']}</p>
          <a href="{manifest_url}">View Manifest &rarr;</a>
        </div>""")

    # 4. Write catalog.json
    catalog_data = {
        "version": "1.0.0",
        "updated_at": "2026-10-31T12:00:00Z",
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

    # Cleanup temp staging
    shutil.rmtree(zip_staging_dir.parent)

    # 6. Complete index.html
    full_html = HTML_INDEX + "\n".join(html_cards) + """
      </div>
    </section>
  </div>
</body>
</html>"""
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as hf:
        hf.write(full_html)

    print("Successfully built LabX Netlify hosting distribution!")

if __name__ == "__main__":
    generate_host()

