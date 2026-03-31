#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

typedef struct {
    int tid;
    char name[32];
    void* (*target)(void*);
} Thread;

typedef struct {
    int process_id;
    Thread threads[10];
    int thread_count;
} Process;

Thread* thread_create(Process* proc, void* (*target)(void*)) {
    Thread* t = &proc->threads[proc->thread_count++];
    t->tid = proc->thread_count;
    t->target = target;
    sprintf(t->name, "Thread-%d", t->tid);
    return t;
}

void* worker(void* arg) {
    char* name = (char*)arg;
    for (int i = 0; i < 3; i++) {
        printf("  Thread %s: iteration %d\n", name, i + 1);
    }
    return NULL;
}

int main() {
    printf("=== Thread Implementation ===\n\n");
    
    printf("Thread class representation:\n");
    printf("  typedef struct {\n");
    printf("      int tid;              // Thread ID\n");
    printf("      char name[32];        // Thread name\n");
    printf("      pthread_t handle;      // POSIX thread handle\n");
    printf("      void* stack;          // Stack pointer\n");
    printf("      void* (*target)();    // Entry function\n");
    printf("  } Thread;\n\n");
    
    printf("Process vs Thread:\n");
    printf("+------------------+------------------+\n");
    printf("|     Process       |     Thread       |\n");
    printf("+------------------+------------------+\n");
    printf("| Separate address  | Shared address   |\n");
    printf("| space            | space            |\n");
    printf("| Higher overhead  | Lower overhead   |\n");
    printf("| IPC required     | Direct sharing   |\n");
    printf("+------------------+------------------+\n\n");
    
    printf("Simulating thread creation:\n");
    Process main_proc = {.thread_count = 0};
    
    for (int i = 0; i < 3; i++) {
        Thread* t = thread_create(&main_proc, worker);
        printf("  Created: %s\n", t->name);
    }
    
    printf("\nSimulating thread execution:\n");
    for (int i = 0; i < main_proc.thread_count; i++) {
        worker(main_proc.threads[i].name);
    }
    
    printf("\nAll threads completed.\n");
    
    return 0;
}
