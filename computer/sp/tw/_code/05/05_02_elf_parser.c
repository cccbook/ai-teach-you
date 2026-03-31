#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    uint8_t magic[4];
    uint16_t type;
    uint16_t machine;
    uint64_t entry;
    uint64_t phoff;
    uint64_t shoff;
} ELFHeader;

int parse_elf_header(ELFHeader *header, const uint8_t *data, size_t size) {
    if (size < 64) {
        printf("File too small\n");
        return -1;
    }
    
    if (data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
        printf("Not a valid ELF file\n");
        return -1;
    }
    
    memcpy(header->magic, data, 4);
    header->type = (data[16]) | (data[17] << 8);
    header->machine = (data[18]) | (data[19] << 8);
    header->entry = 0;
    for (int i = 0; i < 8; i++) {
        header->entry |= ((uint64_t)data[24 + i]) << (i * 8);
    }
    
    printf("ELF Type: %d\n", header->type);
    printf("Target Machine: %d\n", header->machine);
    printf("Entry Point: 0x%lx\n", header->entry);
    
    return 0;
}

int main() {
    uint8_t dummy_elf[64] = {
        0x7f, 'E', 'L', 'F',
        2, 0,
        0x3e, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0x10, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    };
    
    ELFHeader header;
    return parse_elf_header(&header, dummy_elf, sizeof(dummy_elf));
}
