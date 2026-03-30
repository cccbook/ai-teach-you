#include <stdio.h>
#include <string.h>

#define MAX_BLOCKS 15
#define BLOCK_SIZE 512

typedef enum { FILE_TYPE, DIR_TYPE, SYMLINK_TYPE } FileType;

typedef struct {
    int inumber;
    FileType type;
    int size;
    int blocks[MAX_BLOCKS];
    int block_count;
    short permissions;
    int links;
    int uid;
    int gid;
    long atime;
    long mtime;
    long ctime;
} Inode;

void inode_init(Inode* inode, int inumber) {
    inode->inumber = inumber;
    inode->type = FILE_TYPE;
    inode->size = 0;
    inode->block_count = 0;
    inode->permissions = 0644;
    inode->links = 1;
    inode->uid = 1000;
    inode->gid = 1000;
}

void inode_add_block(Inode* inode, int block_num) {
    if (inode->block_count < MAX_BLOCKS) {
        inode->blocks[inode->block_count++] = block_num;
        inode->size += BLOCK_SIZE;
    }
}

void inode_print(Inode* inode) {
    const char* type_str[] = {"file", "directory", "symlink"};
    printf("Inode %d:\n", inode->inumber);
    printf("  Type: %s\n", type_str[inode->type]);
    printf("  Size: %d bytes\n", inode->size);
    printf("  Permissions: %04o\n", inode->permissions);
    printf("  Links: %d\n", inode->links);
    printf("  Blocks: [");
    for (int i = 0; i < inode->block_count; i++) {
        printf("%d%s", inode->blocks[i], i < inode->block_count - 1 ? ", " : "");
    }
    printf("]\n");
}

int main() {
    printf("=== i-node Structure ===\n\n");
    
    printf("i-node structure in C:\n");
    printf("  typedef struct {\n");
    printf("      int inumber;           // Inode number\n");
    printf("      FileType type;         // File type\n");
    printf("      int size;              // File size in bytes\n");
    printf("      int blocks[15];        // Direct block pointers\n");
    printf("      short permissions;     // Access permissions\n");
    printf("      int links;             // Hard link count\n");
    printf("      int uid, gid;          // Owner IDs\n");
    printf("      long atime, mtime;    // Access/modify times\n");
    printf("  } Inode;\n\n");
    
    printf("Demo:\n");
    Inode myfile;
    inode_init(&myfile, 42);
    
    for (int i = 0; i < 5; i++) {
        inode_add_block(&myfile, 1000 + i * 10);
    }
    
    inode_print(&myfile);
    
    printf("\nDirectory structure:\n");
    printf("  Directory file content:\n");
    printf("  +--------+--------------------+\n");
    printf("  | Name   | i-node pointer     |\n");
    printf("  +--------+--------------------+\n");
    printf("  | \".\"    | -> This directory  |\n");
    printf("  | \"..\"   | -> Parent directory|\n");
    printf("  | \"a.txt\"| -> i-node 101     |\n");
    printf("  | \"b.dat\"| -> i-node 205     |\n");
    printf("  +--------+--------------------+\n");
    
    return 0;
}
