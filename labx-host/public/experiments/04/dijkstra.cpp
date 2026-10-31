#include <iostream>
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

    cout << "\nRouting Table from Router " << source << ":\n";
    cout << "------------------------------------------\n";
    cout << "Destination Router | Minimum Metric (Cost)\n";
    cout << "------------------------------------------\n";
    for (int i = 0; i < n; i++) {
        cout << "      Router " << i << "      |       " << dist[i] << "\n";
    }
    cout << "------------------------------------------\n";
}

int main() {
    cout << "=========================================\n";
    cout << " LabX Experiment 04: Dijkstra Routing\n";
    cout << "=========================================\n";

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

    cout << "Simulating Link-State Routing with 5 Routers (0 to 4)...\n";
    dijkstra(0, nodes, graph);

    cout << "Simulation completed successfully.\n";
    cout << "=========================================\n";
    return 0;
}
