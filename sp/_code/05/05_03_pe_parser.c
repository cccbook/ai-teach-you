#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define DOS_SIGNATURE 0x5A4D
#define PE_SIGNATURE 0x00004550

int parse_pe_header(const uint8_t *data) {
    uint16_t dos_sig = data[0] | (data[1] << 8);
    if (dos_sig != DOS_SIGNATURE) {
        printf("Not a valid PE file (DOS signature mismatch)\n");
        return -1;
    }
    printf("Valid DOS signature: MZ\n");
    
    uint32_t e_lfanew = data[60] | (data[61] << 8) | 
                        (data[62] << 16) | (data[63] << 24);
    
    if (e_lfanew < 64 || e_lfanew > 4096) {
        printf("Invalid e_lfanew offset: %u\n", e_lfanew);
        return -1;
    }
    
    uint32_t pe_sig = data[e_lfanew] | (data[e_lfanew+1] << 8) | 
                      (data[e_lfanew+2] << 16) | (data[e_lfanew+3] << 24);
    
    if (pe_sig != PE_SIGNATURE) {
        printf("Invalid PE signature: 0x%08X\n", pe_sig);
        return -1;
    }
    
    printf("Valid PE file, PE header at: %u\n", e_lfanew);
    printf("PE Signature: PE\\0\\0 (0x%08X)\n", PE_SIGNATURE);
    
    return 0;
}

int main() {
    uint8_t valid_pe[1024] = {0};
    valid_pe[0] = 'M';
    valid_pe[1] = 'Z';
    
    uint32_t e_lfanew = 0x80;
    valid_pe[60] = e_lfanew & 0xFF;
    valid_pe[61] = (e_lfanew >> 8) & 0xFF;
    valid_pe[62] = (e_lfanew >> 16) & 0xFF;
    valid_pe[63] = (e_lfanew >> 24) & 0xFF;
    
    valid_pe[e_lfanew] = 'P';
    valid_pe[e_lfanew + 1] = 'E';
    valid_pe[e_lfanew + 2] = 0;
    valid_pe[e_lfanew + 3] = 0;
    
    printf("=== PE Parser Demo ===\n");
    parse_pe_header(valid_pe);
    
    return 0;
}
