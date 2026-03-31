#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    uint8_t magic[4];
    uint16_t type;
    uint16_t machine;
    uint32_t version;
    uint64_t entry;
    uint64_t phoff;
    uint64_t shoff;
    uint32_t flags;
    uint16_t ehsize;
    uint16_t phentsize;
    uint16_t phnum;
    uint16_t shentsize;
    uint16_t shnum;
    uint16_t shstrndx;
} ELFHeader;

int parse_elf_header(ELFHeader *header, const uint8_t *data) {
    if (data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
        printf("Not a valid ELF file\n");
        return -1;
    }
    
    printf("Valid ELF magic: %c%c%c%c\n", data[1], data[2], data[3], data[4]);
    
    header->type = (data[16]) | (data[17] << 8);
    header->machine = (data[18]) | (data[19] << 8);
    
    printf("ELF Type: %d (", header->type);
    switch(header->type) {
        case 1: printf("ET_REL - Relocatable"); break;
        case 2: printf("ET_EXEC - Executable"); break;
        case 3: printf("ET_DYN - Shared Object"); break;
        case 4: printf("ET_CORE - Core Dump"); break;
        default: printf("Unknown"); break;
    }
    printf(")\n");
    
    printf("Target Machine: %d (", header->machine);
    switch(header->machine) {
        case 62: printf("x86_64"); break;
        case 3: printf("i386"); break;
        case 183: printf("AArch64"); break;
        case 243: printf("RISC-V"); break;
        default: printf("Unknown"); break;
    }
    printf(")\n");
    
    return 0;
}

int main() {
    uint8_t valid_elf[64] = {
        0x7f, 'E', 'L', 'F',
        0x02, 0x01, 0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x02, 0x00,
        0x3E, 0x00,
        0x01, 0x00, 0x00, 0x00,
        0x78, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00
    };
    
    ELFHeader header;
    printf("=== ELF Parser Demo ===\n");
    parse_elf_header(&header, valid_elf);
    
    return 0;
}
