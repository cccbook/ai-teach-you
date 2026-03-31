#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_FRAMES 16

typedef struct {
    int page;
    int last_used;
    int valid;
} Frame;

typedef struct {
    Frame frames[NUM_FRAMES];
    int page_table[NUM_FRAMES];
    int page_faults;
    int accesses;
} VirtualMemory;

void vm_init(VirtualMemory *vm) {
    vm->page_faults = 0;
    vm->accesses = 0;
    for (int i = 0; i < NUM_FRAMES; i++) {
        vm->frames[i].valid = 0;
        vm->frames[i].last_used = 0;
        vm->page_table[i] = -1;
    }
}

int lru_replace(VirtualMemory *vm) {
    int lru = 0;
    int min_time = vm->frames[0].last_used;
    for (int i = 1; i < NUM_FRAMES; i++) {
        if (vm->frames[i].last_used < min_time) {
            min_time = vm->frames[i].last_used;
            lru = i;
        }
    }
    return lru;
}

int vm_access(VirtualMemory *vm, int page) {
    vm->accesses++;
    
    if (page < NUM_FRAMES && vm->page_table[page] >= 0) {
        vm->frames[vm->page_table[page]].last_used = vm->accesses;
        return vm->page_table[page];
    }
    
    vm->page_faults++;
    
    int frame = -1;
    for (int i = 0; i < NUM_FRAMES; i++) {
        if (!vm->frames[i].valid) {
            frame = i;
            break;
        }
    }
    
    if (frame < 0) {
        frame = lru_replace(vm);
    }
    
    vm->frames[frame].valid = 1;
    vm->frames[frame].page = page;
    vm->frames[frame].last_used = vm->accesses;
    vm->page_table[page] = frame;
    
    return frame;
}

int main() {
    VirtualMemory vm;
    vm_init(&vm);
    
    vm_access(&vm, 1);
    vm_access(&vm, 2);
    vm_access(&vm, 3);
    vm_access(&vm, 1);
    
    printf("Page faults: %d / %d\n", vm.page_faults, vm.accesses);
    printf("Hit rate: %.2f%%\n", 100.0 * (vm.accesses - vm.page_faults) / vm.accesses);
    
    return 0;
}
