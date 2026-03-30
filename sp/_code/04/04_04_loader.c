#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    void *exec_data;
    size_t exec_size;
    void *entry_point;
    void *text_section;
    void *data_section;
    void *bss_section;
} Program;

typedef struct {
    Program *program;
    void *memory;
    size_t mem_size;
} Loader;

int load(Loader *l, Program *p) {
    printf("=== Loader Steps ===\n");
    
    printf("1. Reading executable header\n");
    printf("   Entry point: %p\n", p->entry_point);
    
    printf("2. Mapping sections to memory\n");
    printf("   .text: %p\n", p->text_section);
    printf("   .data: %p\n", p->data_section);
    printf("   .bss: %p\n", p->bss_section);
    
    printf("3. Setting program counter\n");
    printf("   PC set to: %p\n", p->entry_point);
    
    printf("4. Jumping to entry point\n");
    
    l->program = p;
    l->memory = malloc(1024 * 1024);
    l->mem_size = 1024 * 1024;
    
    printf("Program loaded successfully\n");
    return 0;
}

int main() {
    Loader l;
    memset(&l, 0, sizeof(Loader));
    
    Program prog = {
        .entry_point = (void *)0x401000,
        .text_section = (void *)0x401000,
        .data_section = (void *)0x404000,
        .bss_section = (void *)0x405000
    };
    
    load(&l, &prog);
    
    free(l.memory);
    return 0;
}
