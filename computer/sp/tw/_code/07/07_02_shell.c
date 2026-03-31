#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CMD_BUFFER 256

typedef struct {
    char name[32];
    int (*func)(char **args, int arg_count);
} Command;

typedef struct {
    char buffer[CMD_BUFFER];
    int running;
} Shell;

void shell_init(Shell *s) {
    s->running = 1;
}

int execute_command(Shell *s, char *cmd) {
    char *args[20];
    int arg_count = 0;
    
    char *token = strtok(cmd, " \n");
    while (token && arg_count < 20) {
        args[arg_count++] = token;
        token = strtok(NULL, " \n");
    }
    
    if (arg_count == 0) return 0;
    
    if (strcmp(args[0], "exit") == 0) {
        s->running = 0;
        return 0;
    }
    
    if (strcmp(args[0], "echo") == 0) {
        for (int i = 1; i < arg_count; i++) {
            printf("%s ", args[i]);
        }
        printf("\n");
        return 0;
    }
    
    if (strcmp(args[0], "ls") == 0) {
        printf("file1.txt  file2.txt  dir/\n");
        return 0;
    }
    
    printf("Unknown command: %s\n", args[0]);
    return -1;
}

int main() {
    Shell shell;
    shell_init(&shell);
    
    printf("Simple Shell - type 'exit' to quit\n");
    
    while (shell.running) {
        printf("$ ");
        if (fgets(shell.buffer, CMD_BUFFER, stdin) != NULL) {
            execute_command(&shell, shell.buffer);
        }
    }
    
    return 0;
}
