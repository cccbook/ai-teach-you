#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char* value;
    struct Node** children;
    int child_count;
} Node;

Node* node_create(const char* value) {
    Node* n = (Node*)malloc(sizeof(Node));
    n->value = strdup(value);
    n->children = NULL;
    n->child_count = 0;
    return n;
}

void node_add_child(Node* parent, Node* child) {
    parent->child_count++;
    parent->children = realloc(parent->children, 
                               parent->child_count * sizeof(Node*));
    parent->children[parent->child_count - 1] = child;
}

void traverse_preorder(Node* node, int depth) {
    if (!node) return;
    for (int i = 0; i < depth; i++) printf("  ");
    printf("[Pre] %s\n", node->value);
    for (int i = 0; i < node->child_count; i++) {
        traverse_preorder(node->children[i], depth + 1);
    }
    for (int i = 0; i < depth; i++) printf("  ");
    printf("[Post] %s\n", node->value);
}

void traverse_inorder(Node* node, int depth, int is_root) {
    if (!node) return;
    if (node->child_count > 0) {
        traverse_inorder(node->children[0], depth + 1, 0);
    }
    for (int i = 0; i < depth; i++) printf("  ");
    printf("[In] %s\n", node->value);
    for (int i = 1; i < node->child_count; i++) {
        traverse_inorder(node->children[i], depth + 1, 0);
    }
}

void node_destroy(Node* node) {
    if (!node) return;
    free(node->value);
    for (int i = 0; i < node->child_count; i++) {
        node_destroy(node->children[i]);
    }
    free(node->children);
    free(node);
}

int main() {
    Node* root = node_create("root");
    Node* child1 = node_create("child1");
    Node* child2 = node_create("child2");
    Node* grand1 = node_create("grandchild1");
    Node* grand2 = node_create("grandchild2");
    
    node_add_child(root, child1);
    node_add_child(root, child2);
    node_add_child(child1, grand1);
    node_add_child(child1, grand2);
    
    printf("Preorder/Postorder Traversal:\n");
    traverse_preorder(root, 0);
    
    printf("\nInorder Traversal:\n");
    traverse_inorder(root, 0, 1);
    
    node_destroy(root);
    return 0;
}
