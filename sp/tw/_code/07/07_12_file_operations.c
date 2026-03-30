#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <dirent.h>

void file_operations() {
    printf("=== File System Operations ===\n\n");
    
    printf("Creating directories:\n");
    printf("  mkdir(\"test_dir\", 0755);\n");
    printf("  mkdir(\"test_dir/sub_dir\", 0755);\n");
    
    printf("\nWriting to file:\n");
    printf("  FILE* f = fopen(\"test_dir/file.txt\", \"w\");\n");
    printf("  fputs(\"Hello, File System!\", f);\n");
    printf("  fclose(f);\n");
    
    printf("\nReading from file:\n");
    printf("  FILE* f = fopen(\"test_dir/file.txt\", \"r\");\n");
    printf("  char buffer[256];\n");
    printf("  fgets(buffer, sizeof(buffer), f);\n");
    printf("  printf(\"%%s\", buffer);\n");
    
    printf("\nListing directory:\n");
    printf("  DIR* d = opendir(\"test_dir\");\n");
    printf("  struct dirent* entry;\n");
    printf("  while ((entry = readdir(d)) != NULL) {\n");
    printf("      printf(\"%%s\\n\", entry->d_name);\n");
    printf("  }\n");
    
    printf("\nFile statistics:\n");
    printf("  struct stat st;\n");
    printf("  stat(\"test_dir/file.txt\", &st);\n");
    printf("  printf(\"Size: %%ld bytes\\n\", st.st_size);\n");
    printf("  printf(\"Modified: %%ld\\n\", st.st_mtime);\n");
    
    printf("\nRemoving files:\n");
    printf("  unlink(\"test_dir/file.txt\");\n");
    printf("  rmdir(\"test_dir/sub_dir\");\n");
    printf("  rmdir(\"test_dir\");\n");
}

int main() {
    printf("Simulated File Operations in C:\n\n");
    
    printf("Common POSIX file operations:\n");
    printf("  mkdir()    - Create directory\n");
    printf("  rmdir()    - Remove directory\n");
    printf("  open()     - Open file\n");
    printf("  read()     - Read from file\n");
    printf("  write()    - Write to file\n");
    printf("  unlink()   - Remove file\n");
    printf("  stat()     - Get file metadata\n");
    printf("  opendir()  - Open directory\n");
    printf("  readdir()  - Read directory entry\n\n");
    
    file_operations();
    
    printf("\nFile descriptor vs FILE*:\n");
    printf("  File descriptor: int fd = open(\"file\", O_RDONLY);\n");
    printf("  FILE* stream:   FILE* f = fopen(\"file\", \"r\");\n");
    printf("  Both can be used for file I/O\n");
    
    return 0;
}
