#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_ARGS 32
#define MAX_HISTORY 100

typedef struct {
    char cmd[64];
    char* args[MAX_ARGS];
    int argc;
} Command;

Command history[MAX_HISTORY];
int history_count = 0;

void add_to_history(const char* cmd) {
    if (history_count < MAX_HISTORY) {
        strncpy(history[history_count++].cmd, cmd, 63);
    }
}

void print_history() {
    printf("Command History:\n");
    for (int i = 0; i < history_count; i++) {
        printf("  %d: %s\n", i + 1, history[i].cmd);
    }
}

int parse_command(const char* input, Command* cmd) {
    static char buf[256];
    strncpy(buf, input, 255);
    buf[255] = '\0';
    
    cmd->argc = 0;
    char* token = strtok(buf, " \t\n");
    
    while (token && cmd->argc < MAX_ARGS - 1) {
        cmd->args[cmd->argc++] = token;
        token = strtok(NULL, " \t\n");
    }
    cmd->args[cmd->argc] = NULL;
    
    if (cmd->argc > 0) {
        strncpy(cmd->cmd, cmd->args[0], 63);
    }
    
    return cmd->argc;
}

int execute_command(Command* cmd) {
    if (strcmp(cmd->cmd, "exit") == 0 || strcmp(cmd->cmd, "quit") == 0) {
        return 0;
    }
    
    if (strcmp(cmd->cmd, "history") == 0) {
        print_history();
        return 1;
    }
    
    if (strcmp(cmd->cmd, "echo") == 0) {
        for (int i = 1; i < cmd->argc; i++) {
            printf("%s ", cmd->args[i]);
        }
        printf("\n");
        return 1;
    }
    
    if (strcmp(cmd->cmd, "ls") == 0) {
        printf("file1.txt  file2.txt  main.c  Makefile\n");
        return 1;
    }
    
    if (strcmp(cmd->cmd, "pwd") == 0) {
        printf("/home/user\n");
        return 1;
    }
    
    if (strcmp(cmd->cmd, "date") == 0) {
        printf("Wed Mar 25 06:00:00 UTC 2026\n");
        return 1;
    }
    
    if (strcmp(cmd->cmd, "help") == 0) {
        printf("Available commands: echo, ls, pwd, date, history, exit\n");
        return 1;
    }
    
    if (cmd->argc > 0) {
        printf("Command not found: %s\n", cmd->cmd);
    }
    
    return 1;
}

int main() {
    printf("Simple Shell Simulation\n");
    printf("Commands: echo, ls, pwd, date, history, exit\n\n");
    
    char line[256];
    Command cmd;
    
    while (1) {
        printf("$ ");
        
        if (fgets(line, sizeof(line), stdin) == NULL) {
            break;
        }
        
        line[strcspn(line, "\n")] = '\0';
        
        if (strlen(line) == 0) continue;
        
        add_to_history(line);
        
        parse_command(line, &cmd);
        
        if (!execute_command(&cmd)) {
            printf("Goodbye!\n");
            break;
        }
    }
    
    return 0;
}
