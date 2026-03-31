#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    char value[32];
    int child_count;
    struct Node** children;
} Node;

Node* make_node(const char* value) {
    Node* n = (Node*)malloc(sizeof(Node));
    snprintf(n->value, 32, "%s", value);
    n->child_count = 0;
    n->children = NULL;
    return n;
}

void add_child(Node* parent, Node* child) {
    parent->child_count++;
    parent->children = realloc(parent->children, 
                              parent->child_count * sizeof(Node*));
    parent->children[parent->child_count - 1] = child;
}

void free_node(Node* n) {
    if (!n) return;
    for (int i = 0; i < n->child_count; i++) {
        free_node(n->children[i]);
    }
    free(n->children);
    free(n);
}

void traverse_preorder(Node* node, int depth) {
    if (!node) return;
    for (int i = 0; i < depth; i++) printf("  ");
    printf("Pre: %s\n", node->value);
    for (int i = 0; i < node->child_count; i++) {
        traverse_preorder(node->children[i], depth + 1);
    }
}

void traverse_postorder(Node* node, int depth) {
    if (!node) return;
    for (int i = 0; i < node->child_count; i++) {
        traverse_postorder(node->children[i], depth + 1);
    }
    for (int i = 0; i < depth; i++) printf("  ");
    printf("Post: %s\n", node->value);
}

void traverse_inorder(Node* node, int depth) {
    if (!node) return;
    if (node->child_count > 0) traverse_inorder(node->children[0], depth + 1);
    for (int i = 0; i < depth; i++) printf("  ");
    printf("In: %s\n", node->value);
    if (node->child_count > 1) traverse_inorder(node->children[1], depth + 1);
}

int main() {
    Node* root = make_node("root");
    Node* left = make_node("left");
    Node* right = make_node("right");
    Node* ll = make_node("left-left");
    Node* lr = make_node("left-right");
    
    add_child(root, left);
    add_child(root, right);
    add_child(left, ll);
    add_child(left, lr);
    
    printf("Preorder traversal:\n");
    traverse_preorder(root, 0);
    printf("\nPostorder traversal:\n");
    traverse_postorder(root, 0);
    printf("\nInorder traversal:\n");
    traverse_inorder(root, 0);
    
    free_node(root);
    return 0;
}
