# LabX Remote: CN Exp 10 (Experiment 10 – Dijkstra's Shortest Path Routing Algorithm)
$filename = "dijkstra.c"
$code = @'
/*
 * Computer Networks Laboratory - Routing Algorithms
 * Experiment 10: Dijkstra's Shortest Path Routing Algorithm
 * Demonstrates Link State Routing (OSPF) to find minimum-cost routes
 */

#include <stdio.h>
#include <stdbool.h>

#define INFINITY 9999
#define MAX_NODES 20

void printPath(int parent[], int j) {
    if (parent[j] == -1) {
        printf("%d", j);
        return;
    }
    printPath(parent, parent[j]);
    printf(" -> %d", j);
}

void dijkstra(int cost[MAX_NODES][MAX_NODES], int n, int source) {
    int distance[MAX_NODES];
    bool visited[MAX_NODES];
    int parent[MAX_NODES];

    for (int i = 0; i < n; i++) {
        distance[i] = cost[source][i];
        visited[i] = false;
        parent[i] = (cost[source][i] != INFINITY && i != source) ? source : -1;
    }

    distance[source] = 0;
    visited[source] = true;
    parent[source] = -1;

    for (int count = 1; count < n - 1; count++) {
        int min_dist = INFINITY;
        int next_node = -1;

        for (int i = 0; i < n; i++) {
            if (!visited[i] && distance[i] < min_dist) {
                min_dist = distance[i];
                next_node = i;
            }
        }

        if (next_node == -1) break;
        visited[next_node] = true;

        for (int i = 0; i < n; i++) {
            if (!visited[i] && cost[next_node][i] != INFINITY) {
                if (distance[next_node] + cost[next_node][i] < distance[i]) {
                    distance[i] = distance[next_node] + cost[next_node][i];
                    parent[i] = next_node;
                }
            }
        }
    }

    printf("\n===============================================================\n");
    printf(" Routing Table for Source Router: %d (Link-State Shortest Path)\n", source);
    printf("===============================================================\n");
    printf(" Destination | Minimum Cost | Shortest Path\n");
    printf("-------------|--------------|----------------------------------\n");

    for (int i = 0; i < n; i++) {
        if (i == source) {
            printf("      %2d     |      %2d      | [Local Node]\n", i, 0);
        } else if (distance[i] == INFINITY) {
            printf("      %2d     |   Unreachable| No Path\n", i);
        } else {
            printf("      %2d     |      %2d      | ", i, distance[i]);
            printPath(parent, i);
            printf("\n");
        }
    }
    printf("===============================================================\n");
}

int main() {
    int n, source;
    int cost[MAX_NODES][MAX_NODES];

    printf("=====================================================\n");
    printf("   Dijkstra's Shortest Path Routing Algorithm (CN)   \n");
    printf("=====================================================\n");
    printf("Enter number of network nodes/routers: ");
    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX_NODES) {
        printf("Invalid input or non-interactive console. Using default 5-node topology.\n");
        n = 5;
        int default_cost[5][5] = {
            {0, 4, 2, INFINITY, INFINITY},
            {4, 0, 1, 5, INFINITY},
            {2, 1, 0, 8, 10},
            {INFINITY, 5, 8, 0, 2},
            {INFINITY, INFINITY, 10, 2, 0}
        };
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                cost[i][j] = default_cost[i][j];
        source = 0;
    } else {
        printf("Enter routing cost matrix (%dx%d, 0 for self, 9999 for infinity):\n", n, n);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                scanf("%d", &cost[i][j]);
                if (i != j && cost[i][j] == 0) cost[i][j] = INFINITY;
            }
        }
        printf("Enter source router (0 to %d): ", n - 1);
        if (scanf("%d", &source) != 1 || source < 0 || source >= n) {
            source = 0;
        }
    }

    dijkstra(cost, n, source);
    return 0;
}

/*
============================================================================
HOW TO RUN THIS EXPERIMENT:
============================================================================
Prerequisites: GCC compiler (`gcc --version`).

1. Compile the C code:
   gcc dijkstra.c -o dijkstra

2. Run the executable:
   ./dijkstra

3. Interactive Sample Run:
   Enter number of network nodes/routers: 5
   Enter routing cost matrix (5x5):
   0 4 2 9999 9999
   4 0 1 5 9999
   2 1 0 8 10
   9999 5 8 0 2
   9999 9999 10 2 0
   Enter source router (0 to 4): 0

   Output:
   Destination | Minimum Cost | Shortest Path
        0      |       0      | [Local Node]
        1      |       3      | 0 -> 2 -> 1
        2      |       2      | 0 -> 2
        3      |       8      | 0 -> 2 -> 1 -> 3
        4      |      10      | 0 -> 2 -> 1 -> 3 -> 4
============================================================================
EXPERIMENT THEORY (Computer Networks - Dijkstra's Link-State Routing):
============================================================================
Dijkstra's Algorithm is a greedy single-source shortest path algorithm used
widely in computer networking for unicast routing protocols, notably Open
Shortest Path First (OSPF) and Intermediate System to Intermediate System
(IS-IS) in the Link State Routing domain.

Key Principles:
1. Global Topology Knowledge:
   Every router floods Link State Advertisements (LSAs) containing the state
   and metric of its directly connected links to all routers via Dijkstra's
   algorithm so that each router builds an identical link-state database (LSDB).

2. Forward Search Tree (SPT):
   The router places itself as the root and iteratively builds a Shortest
   Path Tree (SPT) by maintaining:
   - Visited Set (Permanent nodes with confirmed minimal cost).
   - Tentative Set (Candidate neighbors evaluated through relaxation).

3. Edge Relaxation:
   If traversing via node 'u' to 'v' produces a strictly lower cumulative
   path cost:
   dist[v] = min(dist[v], dist[u] + cost[u][v])

4. Forwarding Table Generation:
   From the completed SPT, the router extracts the next-hop IP address and
   outgoing interface for each destination subnet, achieving loop-free routing
   with O(V^2) or O(E + V log V) convergence time.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White
