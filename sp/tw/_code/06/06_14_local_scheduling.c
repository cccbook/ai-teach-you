#include <stdio.h>
#include <stdlib.h>

#define MAX_NODES 20
#define MAX_EDGES 40

typedef struct {
    int id;
    int depth;
    int scheduled;
} Node;

typedef struct {
    int from;
    int to;
} Edge;

int has_all_preds_scheduled(Node nodes[], int node_id, Edge edges[], int edge_count, int scheduled_count) {
    for (int i = 0; i < edge_count; i++) {
        if (edges[i].to == node_id) {
            int pred_scheduled = 0;
            for (int j = 0; j < scheduled_count; j++) {
                if (nodes[j].id == edges[i].from) {
                    pred_scheduled = 1;
                    break;
                }
            }
            if (!pred_scheduled) return 0;
        }
    }
    return 1;
}

int compute_depth(Node nodes[], int node_id, Edge edges[], int edge_count, Node result_nodes[]) {
    int max_pred_depth = -1;
    
    for (int i = 0; i < edge_count; i++) {
        if (edges[i].to == node_id) {
            for (int j = 0; j < MAX_NODES; j++) {
                if (result_nodes[j].id == edges[i].from) {
                    if (result_nodes[j].depth > max_pred_depth) {
                        max_pred_depth = result_nodes[j].depth;
                    }
                    break;
                }
            }
        }
    }
    
    if (max_pred_depth < 0) return 0;
    return max_pred_depth + 1;
}

void local_scheduling(Node nodes[], int n, Edge edges[], int e, int issue_width) {
    printf("=== Local Scheduling (Issue Width = %d) ===\n\n", issue_width);
    
    Node result_nodes[MAX_NODES];
    int result_count = 0;
    
    for (int i = 0; i < n; i++) {
        result_nodes[i].id = nodes[i].id;
        result_nodes[i].depth = 0;
        result_nodes[i].scheduled = 0;
    }
    
    for (int i = 0; i < n; i++) {
        result_nodes[i].depth = compute_depth(result_nodes, nodes[i].id, edges, e, result_nodes);
    }
    
    printf("Node depths (critical path lengths):\n");
    for (int i = 0; i < n; i++) {
        printf("  Node %c: depth = %d\n", 'A' + result_nodes[i].id, result_nodes[i].depth);
    }
    
    printf("\nScheduling:\n");
    int clock = 0;
    
    while (result_count < n) {
        Node ready[MAX_NODES];
        int ready_count = 0;
        
        for (int i = 0; i < n; i++) {
            if (result_nodes[i].scheduled) continue;
            if (has_all_preds_scheduled(result_nodes, result_nodes[i].id, edges, e, result_count)) {
                ready[ready_count++] = result_nodes[i];
            }
        }
        
        if (ready_count == 0) {
            printf("  Clock %d: No ready instructions (cycle detected)\n", clock);
            break;
        }
        
        for (int i = 0; i < ready_count && result_count < n; i++) {
            for (int j = 0; j < n; j++) {
                if (result_nodes[j].id == ready[i].id && !result_nodes[j].scheduled) {
                    result_nodes[j].scheduled = 1;
                    printf("  Clock %d: Execute Node %c\n", clock, 'A' + result_nodes[j].id);
                    result_count++;
                    break;
                }
            }
        }
        clock++;
    }
    
    printf("\nTotal schedule length: %d cycles\n", clock);
}

int main() {
    Node nodes[] = {
        {0, 0, 0},
        {1, 0, 0},
        {2, 0, 0},
        {3, 0, 0}
    };
    int n = 4;
    
    Edge edges[] = {
        {0, 2},
        {1, 2},
        {2, 3}
    };
    int e = 3;
    
    printf("DAG:\n");
    printf("    A\n");
    printf("   / \\\n");
    printf("  B   C\n");
    printf("   \\ /\n");
    printf("    D\n\n");
    
    local_scheduling(nodes, n, edges, e, 2);
    
    printf("\nAlgorithm:\n");
    printf("  1. Build DAG from block instructions\n");
    printf("  2. Compute depth (critical path) for each node\n");
    printf("  3. Sort by depth (highest first)\n");
    printf("  4. Schedule up to issue_width instructions per cycle\n");
    
    return 0;
}
