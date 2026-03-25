#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define DOS_SIGNATURE 0x5A4D
#define PE_SIGNATURE 0x00004550

typedef struct {
    uint16_t e_magic;
    uint16_t e_lfanew;
} DOSHeader;

int parse_pe_header(const uint8_t *data, size_t size) {
    if (size < 64) {
        printf("File too small\n");
        return -1;
    }
    
    uint16_t dos_sig = data[0] | (data[1] << 8);
    if (dos_sig != DOS_SIGNATURE) {
        printf("Not a valid PE file (no DOS header)\n");
        return -1;
    }
    
    uint32_t e_lfanew = data[60] | (data[61] << 8) | (data[62] << 16) | (data[63] << 24);
    
    if (e_lfanew + 4 > size) {
        printf("Invalid PE offset\n");
        return -1;
    }
    
    uint32_t pe_sig = data[e_lfanew] | (data[e_lfanew+1] << 8) | 
                      (data[e_lfanew+2] << 16) | (data[e_lfanew+3] << 24);
    
    if (pe_sig != PE_SIGNATURE) {
        printf("Invalid PE signature\n");
        return -1;
    }
    
    printf("Valid PE file, PE header at offset: %u\n", e_lfanew);
    return 0;
}

int main() {
    uint8_t dummy_pe[128] = {0};
    dummy_pe[0] = 0x4D;
    dummy_pe[1] = 0x5A;
    dummy_pe[60] = 0x80;
    
    dummy_pe[0x80] = 'P';
    dummy_pe[0x81] = 'E';
    dummy_pe[0x82] = 0;
    dummy_pe[0x83] = 0;
    
    return parse_pe_header(dummy_pe, sizeof(dummy_pe));
}
