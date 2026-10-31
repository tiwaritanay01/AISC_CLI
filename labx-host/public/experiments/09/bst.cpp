#include <iostream>

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
    cout << "=========================================\n";
    cout << " LabX Experiment 09: Binary Search Tree\n";
    cout << "=========================================\n";

    Node* root = nullptr;
    int values[] = {50, 30, 70, 20, 40, 60, 80};

    cout << "Inserting keys into BST: ";
    for (int v : values) {
        cout << v << " ";
        root = insert(root, v);
    }
    cout << "\n\n";

    cout << "Inorder Traversal (Sorted): ";
    inorder(root);
    cout << "\n";

    cout << "Preorder Traversal:         ";
    preorder(root);
    cout << "\n\n";

    int query = 40;
    cout << "Searching for key " << query << ": " << (search(root, query) ? "FOUND" : "NOT FOUND") << "\n";

    cleanup(root);
    cout << "=========================================\n";
    return 0;
}
