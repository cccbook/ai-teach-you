#include <stdio.h>
#include <stdint.h>

#define FAT_MAGIC 0xcafebabe
#define FAT_MAGIC_64 0xcafebabefacebabe
#define MH_MAGIC 0xfeedface
#define MH_MAGIC_64 0xfeedfacf

typedef struct {
    uint32_t magic;
    uint32_t cputype;
    uint32_t cpusubtype;
    uint32_t filetype;
    uint32_t ncmds;
    uint32_t sizeofcmds;
    uint32_t flags;
} MachHeader;

const char* get_macho_type_str(uint32_t type) {
    switch(type) {
        case 0x1: return "MH_OBJECT (Relocatable)";
        case 0x2: return "MH_EXECUTE (Executable)";
        case 0x3: return "MH_FVMLIB (Fixed VM Library)";
        case 0x4: return "MH_CORE (Core Dump)";
        case 0x5: return "MH_PRELOAD (Preloaded Executable)";
        case 0x6: return "MH_DYLIB (Dynamic Library)";
        case 0x7: return "MH_DYLINKER (Dynamic Linker)";
        case 0x8: return "MH_BUNDLE (Bundle)";
        case 0x9: return "MH_DYLIB_STUB (Stub Library)";
        case 0xa: return "MH_DSYM (Debug Symbols)";
        default: return "Unknown";
    }
}

const char* get_cpu_type_str(uint32_t cputype) {
    switch(cputype) {
        case 7: return "x86";
        case 0x01000007: return "x86_64";
        case 12: return "ARM";
        case 0x0100000C: return "ARM64";
        default: return "Unknown";
    }
}

int parse_macho_header(MachHeader *header, const uint8_t *data) {
    header->magic = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24);
    
    printf("Magic: 0x%08X - ", header->magic);
    
    if (header->magic == FAT_MAGIC) {
        printf("Fat Binary (32-bit)\n");
        return 0;
    } else if (header->magic == FAT_MAGIC_64) {
        printf("Fat Binary (64-bit)\n");
        return 0;
    } else if (header->magic == MH_MAGIC) {
        printf("32-bit Mach-O\n");
    } else if (header->magic == MH_MAGIC_64) {
        printf("64-bit Mach-O\n");
    } else {
        printf("Unknown format\n");
        return -1;
    }
    
    header->cputype = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7];
    header->filetype = (data[16] << 24) | (data[17] << 16) | (data[18] << 8) | data[19];
    
    printf("CPU Type: %d (%s)\n", header->cputype, get_cpu_type_str(header->cputype));
    printf("File Type: %d (%s)\n", header->filetype, get_macho_type_str(header->filetype));
    
    return 0;
}

int main() {
    uint8_t macho_64[32] = {
        0xcf, 0xfa, 0xed, 0xfe,
        0x07, 0x00, 0x00, 0x01,
        0x03, 0x00, 0x00, 0x00,
        0x02, 0x00, 0x00, 0x00,
        0x01, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    };
    
    printf("=== Mach-O Parser Demo ===\n");
    MachHeader header;
    parse_macho_header(&header, macho_64);
    
    return 0;
}
