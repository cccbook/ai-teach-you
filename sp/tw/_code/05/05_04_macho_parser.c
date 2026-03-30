#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define FAT_MAGIC 0xcafebabe
#define MH_MAGIC 0xfeedface
#define MH_MAGIC_64 0xfeedfacf

int parse_macho_header(const uint8_t *data, size_t size) {
    if (size < 4) {
        printf("File too small\n");
        return -1;
    }
    
    uint32_t magic = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3];
    
    if (magic == FAT_MAGIC) {
        printf("Fat Binary (Universal Binary)\n");
        return 0;
    }
    
    if (magic == MH_MAGIC) {
        printf("32-bit Mach-O\n");
        return 0;
    }
    
    if (magic == MH_MAGIC_64) {
        printf("64-bit Mach-O\n");
        return 0;
    }
    
    printf("Unknown Mach-O format\n");
    return -1;
}

int main() {
    uint8_t macho_64[] = {0xfe, 0xed, 0xfa, 0xcf};
    parse_macho_header(macho_64, sizeof(macho_64));
    
    uint8_t fat[] = {0xca, 0xfe, 0xba, 0xbe};
    parse_macho_header(fat, sizeof(fat));
    
    return 0;
}
