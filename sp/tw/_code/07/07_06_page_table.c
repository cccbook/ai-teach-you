#include <stdio.h>
#include <stdlib.h>

#define PAGE_SIZE 4096
#define MAX_PAGES 1024

typedef struct {
    int valid;
    int frame_number;
} PageTableEntry;

typedef struct {
    PageTableEntry entries[MAX_PAGES];
    int page_size;
} PageTable;

void pt_init(PageTable *pt) {
    pt->page_size = PAGE_SIZE;
    for (int i = 0; i < MAX_PAGES; i++) {
        pt->entries[i].valid = 0;
    }
}

int pt_translate(PageTable *pt, int virtual_addr) {
    int vpn = virtual_addr / pt->page_size;
    int offset = virtual_addr % pt->page_size;
    
    if (vpn >= MAX_PAGES || !pt->entries[vpn].valid) {
        printf("Page fault: VPN %d\n", vpn);
        return -1;
    }
    
    return pt->entries[vpn].frame_number * pt->page_size + offset;
}

int main() {
    PageTable pt;
    pt_init(&pt);
    
    pt.entries[10].valid = 1;
    pt.entries[10].frame_number = 5;
    
    int virt_addr = 10 * PAGE_SIZE + 100;
    int phys_addr = pt_translate(&pt, virt_addr);
    
    printf("Virtual: 0x%x -> Physical: 0x%x\n", virt_addr, phys_addr);
    
    return 0;
}
