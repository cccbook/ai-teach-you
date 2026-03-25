#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_FRAMES 16
#define NUM_PAGES 64

typedef struct {
    int frame;
    int valid;
    int last_used;
} PageEntry;

int frames[NUM_FRAMES];
PageEntry page_table[NUM_PAGES];
int frame_counter = 0;
int page_faults = 0;
int accesses = 0;

void init_memory() {
    for (int i = 0; i < NUM_FRAMES; i++) {
        frames[i] = -1;
    }
    for (int i = 0; i < NUM_PAGES; i++) {
        page_table[i].valid = 0;
        page_table[i].last_used = -1;
    }
}

int find_free_frame() {
    for (int i = 0; i < NUM_FRAMES; i++) {
        if (frames[i] == -1) return i;
    }
    return -1;
}

int find_lru_frame() {
    int lru = 0;
    int oldest = page_table[frames[0]].last_used;
    
    for (int i = 1; i < NUM_FRAMES; i++) {
        if (page_table[frames[i]].last_used < oldest) {
            oldest = page_table[frames[i]].last_used;
            lru = i;
        }
    }
    return lru;
}

int access_page(int page_num) {
    accesses++;
    
    if (page_table[page_num].valid) {
        page_table[page_num].last_used = accesses;
        return page_table[page_num].frame;
    }
    
    page_faults++;
    printf("  Page fault for page %d\n", page_num);
    
    int frame = find_free_frame();
    
    if (frame < 0) {
        frame = find_lru_frame();
        int old_page = frames[frame];
        printf("  Evicting page %d from frame %d\n", old_page, frame);
        page_table[old_page].valid = 0;
    }
    
    frames[frame] = page_num;
    page_table[page_num].frame = frame;
    page_table[page_num].valid = 1;
    page_table[page_num].last_used = accesses;
    
    return frame;
}

void print_memory_state() {
    printf("Frame allocation: [");
    for (int i = 0; i < NUM_FRAMES; i++) {
        if (frames[i] >= 0) {
            printf("%d", frames[i]);
        } else {
            printf("-");
        }
        if (i < NUM_FRAMES - 1) printf(" ");
    }
    printf("]\n");
}

int main() {
    printf("=== Virtual Memory and Page Replacement Demo ===\n\n");
    
    init_memory();
    
    printf("Memory configuration:\n");
    printf("  Frames: %d\n", NUM_FRAMES);
    printf("  Pages: %d\n", NUM_PAGES);
    
    printf("\n=== FIFO Page Replacement ===\n");
    
    int access_sequence[] = {1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5};
    int seq_len = sizeof(access_sequence) / sizeof(access_sequence[0]);
    
    printf("Access sequence: ");
    for (int i = 0; i < seq_len; i++) {
        printf("%d ", access_sequence[i]);
    }
    printf("\n\n");
    
    for (int i = 0; i < seq_len; i++) {
        printf("Access %d: page %d -> ", i + 1, access_sequence[i]);
        int frame = access_page(access_sequence[i]);
        printf("frame %d\n", frame);
        print_memory_state();
    }
    
    printf("\n=== Statistics ===\n");
    printf("Total accesses: %d\n", accesses);
    printf("Page faults: %d\n", page_faults);
    printf("Hit rate: %.1f%%\n", 100.0 * (accesses - page_faults) / accesses);
    
    printf("\n=== LRU Page Replacement ===\n");
    
    init_memory();
    page_faults = 0;
    accesses = 0;
    
    int access_sequence2[] = {0, 1, 2, 3, 0, 1, 4, 0, 1, 2, 3, 4};
    seq_len = sizeof(access_sequence2) / sizeof(access_sequence2[0]);
    
    printf("Access sequence: ");
    for (int i = 0; i < seq_len; i++) {
        printf("%d ", access_sequence2[i]);
    }
    printf("\n\n");
    
    for (int i = 0; i < seq_len; i++) {
        printf("Access %d: page %d -> ", i + 1, access_sequence2[i]);
        int frame = access_page(access_sequence2[i]);
        printf("frame %d\n", frame);
        print_memory_state();
    }
    
    printf("\n=== Statistics ===\n");
    printf("Total accesses: %d\n", accesses);
    printf("Page faults: %d\n", page_faults);
    printf("Hit rate: %.1f%%\n", 100.0 * (accesses - page_faults) / accesses);
    
    return 0;
}
