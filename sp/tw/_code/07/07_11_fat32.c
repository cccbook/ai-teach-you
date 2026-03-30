#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FAT_FREE 0
#define FAT_EOF 0xFFFFFFFF
#define CLUSTER_SIZE 512

typedef struct {
    unsigned int* fat;
    int fat_size;
    unsigned int root_dir_cluster;
} FAT;

typedef struct {
    char filename[13];
    unsigned int start_cluster;
    int size;
    unsigned int* fat;
} FileEntry;

int fat_allocate_cluster(FAT* fat) {
    for (int i = 2; i < fat->fat_size; i++) {
        if (fat->fat[i] == FAT_FREE) {
            fat->fat[i] = FAT_EOF;
            return i;
        }
    }
    return -1;
}

unsigned int* fat_allocate_chain(FAT* fat, int num_clusters) {
    unsigned int* chain = malloc(sizeof(unsigned int) * num_clusters);
    
    for (int i = 0; i < num_clusters; i++) {
        chain[i] = fat_allocate_cluster(fat);
        if (chain[i] == -1) {
            chain[i] = FAT_EOF;
            break;
        }
        printf("  Allocated cluster %u\n", chain[i]);
    }
    
    return chain;
}

void fat_write_file(FAT* fat, FileEntry* entry, const char* data, int size) {
    int clusters_needed = (size + CLUSTER_SIZE - 1) / CLUSTER_SIZE;
    
    printf("Writing file: %s (%d bytes, needs %d clusters)\n",
           entry->filename, size, clusters_needed);
    
    unsigned int* chain = fat_allocate_chain(fat, clusters_needed);
    
    entry->start_cluster = chain[0];
    entry->size = size;
    
    printf("  File cluster chain: [");
    for (int i = 0; i < clusters_needed && chain[i] != FAT_EOF; i++) {
        printf("%u%s", chain[i], i < clusters_needed - 1 ? ", " : "");
    }
    printf("]\n");
    
    free(chain);
}

int main() {
    printf("=== FAT32 File System ===\n\n");
    
    printf("FAT32 Structure:\n");
    printf("  +------------------+\n");
    printf("  | Reserved Region  |\n");
    printf("  +------------------+\n");
    printf("  | FAT (File        |\n");
    printf("  | Allocation Table)|\n");
    printf("  +------------------+\n");
    printf("  | Data Region      |\n");
    printf("  | (Clusters)       |\n");
    printf("  +------------------+\n\n");
    
    FAT fat;
    fat.fat_size = 100;
    fat.fat = calloc(fat.fat_size, sizeof(unsigned int));
    fat.fat[0] = FAT_FREE;
    fat.fat[1] = FAT_FREE;
    
    printf("FAT initialization:\n");
    printf("  FAT[0] = %u (reserved)\n", fat.fat[0]);
    printf("  FAT[1] = %u (reserved)\n", fat.fat[1]);
    printf("  FAT[2..99] = 0 (free)\n\n");
    
    FileEntry files[] = {
        {.filename = "README.TXT"},
        {.filename = "DATA.BIN"}
    };
    
    printf("File allocation demo:\n");
    fat_write_file(&fat, &files[0], "Hello FAT32!", 12);
    fat_write_file(&fat, &files[1], "Binary data here", 16);
    
    printf("\nCluster allocation:\n");
    printf("  Each cluster = 512 bytes\n");
    printf("  FAT entry values:\n");
    printf("    0x00000000 = Free cluster\n");
    printf("    0xFFFFFFFF = EOF\n");
    printf("    0x0000000x = Next cluster in chain\n");
    
    free(fat.fat);
    
    return 0;
}
