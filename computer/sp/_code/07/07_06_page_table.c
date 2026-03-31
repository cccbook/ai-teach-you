#include <stdio.h>
#include <stdlib.h>

#define PAGE_SIZE 4096
#define PAGE_BITS 12
#define VPN_BITS 20
#define NUM_FRAMES 1024
#define NUM_PAGES (1 << VPN_BITS)

typedef struct {
    int frame_number;
    int valid;
    int dirty;
    int referenced;
} PageTableEntry;

typedef struct {
    PageTableEntry entries[NUM_PAGES];
} PageTable;

unsigned int extract_vpn(unsigned int virtual_addr) {
    return virtual_addr >> PAGE_BITS;
}

unsigned int extract_offset(unsigned int virtual_addr) {
    return virtual_addr & ((1 << PAGE_BITS) - 1);
}

int translate(PageTable* pt, unsigned int virtual_addr) {
    unsigned int vpn = extract_vpn(virtual_addr);
    unsigned int offset = extract_offset(virtual_addr);
    
    if (!pt->entries[vpn].valid) {
        printf("Page fault! VPN=%u\n", vpn);
        return -1;
    }
    
    unsigned int frame = pt->entries[vpn].frame_number;
    unsigned int physical = (frame << PAGE_BITS) | offset;
    
    return physical;
}

void init_page_table(PageTable* pt) {
    for (int i = 0; i < NUM_PAGES; i++) {
        pt->entries[i].valid = 0;
        pt->entries[i].dirty = 0;
        pt->entries[i].referenced = 0;
    }
}

int allocate_page(PageTable* pt, unsigned int vpn, int frame) {
    if (vpn >= NUM_PAGES) return -1;
    pt->entries[vpn].frame_number = frame;
    pt->entries[vpn].valid = 1;
    return 0;
}

void print_page_info(PageTable* pt, unsigned int vpn) {
    printf("VPN %u: ", vpn);
    if (pt->entries[vpn].valid) {
        printf("Frame %d, dirty=%d, ref=%d\n",
               pt->entries[vpn].frame_number,
               pt->entries[vpn].dirty,
               pt->entries[vpn].referenced);
    } else {
        printf("Not mapped (page fault)\n");
    }
}

int main() {
    printf("=== Page Table and Address Translation Demo ===\n\n");
    
    PageTable* pt = (PageTable*)malloc(sizeof(PageTable));
    init_page_table(pt);
    
    printf("Page size: %d bytes (2^%d)\n", PAGE_SIZE, PAGE_BITS);
    printf("VPN bits: %d, Offset bits: %d\n", VPN_BITS, PAGE_BITS);
    printf("Number of pages: %d\n\n", NUM_PAGES);
    
    allocate_page(pt, 0, 100);
    allocate_page(pt, 1, 200);
    allocate_page(pt, 10, 300);
    allocate_page(pt, 0xFFFFF, 500);
    
    printf("=== Translation Examples ===\n");
    
    unsigned int test_addrs[] = {
        0x00001000,
        0x00001100,
        0x00005000,
        0xFFFF0000,
        0x00002000
    };
    
    for (int i = 0; i < 5; i++) {
        unsigned int vaddr = test_addrs[i];
        unsigned int vpn = extract_vpn(vaddr);
        unsigned int offset = extract_offset(vaddr);
        
        printf("\nVirtual addr: 0x%08X\n", vaddr);
        printf("  VPN: %u (0x%X), Offset: %u (0x%X)\n", 
               vpn, vpn, offset, offset);
        
        print_page_info(pt, vpn);
        
        int phys = translate(pt, vaddr);
        if (phys >= 0) {
            printf("  Physical addr: 0x%08X\n", phys);
        }
    }
    
    free(pt);
    return 0;
}
