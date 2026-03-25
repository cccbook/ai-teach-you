#include <stdio.h>
#include <string.h>

typedef struct {
    int pid;
    char name[32];
    char state[16];
    int priority;
} Process;

typedef struct {
    int syscall_number;
    char name[32];
    char description[128];
} SyscallEntry;

void print_process(Process* p) {
    printf("Process: PID=%d, Name=%s, State=%s, Priority=%d\n", 
           p->pid, p->name, p->state, p->priority);
}

void print_syscall_table() {
    printf("\nSystem Call Table:\n");
    printf("%-6s %-20s %s\n", "Num", "Name", "Description");
    printf("%-6s %-20s %s\n", "---", "----", "-----------");
    
    SyscallEntry table[] = {
        {0, "exit", "Terminate process"},
        {1, "fork", "Create new process"},
        {2, "read", "Read from file descriptor"},
        {3, "write", "Write to file descriptor"},
        {4, "open", "Open file"},
        {5, "close", "Close file descriptor"},
        {9, "mmap", "Map memory"},
        {60, "exit_group", "Exit all threads"},
    };
    
    for (int i = 0; i < 8; i++) {
        printf("%-6d %-20s %s\n", 
               table[i].syscall_number, 
               table[i].name, 
               table[i].description);
    }
}

int main() {
    printf("=== Kernel Concepts Demo ===\n\n");
    
    Process p1 = {1, "init", "RUNNING", 0};
    Process p2 = {2, "shell", "READY", 1};
    Process p3 = {3, "logger", "BLOCKED", 2};
    
    print_process(&p1);
    print_process(&p2);
    print_process(&p3);
    
    print_syscall_table();
    
    return 0;
}
