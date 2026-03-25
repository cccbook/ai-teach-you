#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INSTR 20

typedef struct {
    char name[16];
    int latency;
    int depth;
    int scheduled;
    int deps[MAX_INSTR];
    int dep_count;
} Instruction;

typedef struct {
    Instruction instrs[MAX_INSTR];
    int count;
    int scheduled[MAX_INSTR];
    int sched_count;
    int clock;
} Scheduler;

void add_dep(Scheduler *s, int from, int to) {
    s->instrs[to].deps[s->instrs[to].dep_count++] = from;
}

int can_schedule(Scheduler *s, int idx) {
    if (s->instrs[idx].scheduled) return 0;
    for (int i = 0; i < s->instrs[idx].dep_count; i++) {
        if (!s->instrs[s->instrs[idx].deps[i]].scheduled) {
            return 0;
        }
    }
    return 1;
}

void compute_depths(Scheduler *s) {
    for (int i = 0; i < s->count; i++) {
        int max_dep_depth = 0;
        for (int j = 0; j < s->instrs[i].dep_count; j++) {
            int dep_idx = s->instrs[i].deps[j];
            if (s->instrs[dep_idx].depth > max_dep_depth) {
                max_dep_depth = s->instrs[dep_idx].depth;
            }
        }
        s->instrs[i].depth = max_dep_depth + s->instrs[i].latency;
    }
}

void schedule_list(Scheduler *s) {
    compute_depths(s);
    s->sched_count = 0;
    s->clock = 0;
    
    while (s->sched_count < s->count) {
        int best_idx = -1;
        int best_depth = -1;
        
        for (int i = 0; i < s->count; i++) {
            if (can_schedule(s, i) && s->instrs[i].depth > best_depth) {
                best_depth = s->instrs[i].depth;
                best_idx = i;
            }
        }
        
        if (best_idx >= 0) {
            s->instrs[best_idx].scheduled = 1;
            s->scheduled[s->sched_count++] = best_idx;
            s->clock += s->instrs[best_idx].latency;
        }
    }
}

int main() {
    Scheduler s;
    memset(&s, 0, sizeof(s));
    
    strcpy(s.instrs[0].name, "load"); s.instrs[0].latency = 1;
    strcpy(s.instrs[1].name, "mul"); s.instrs[1].latency = 2;
    strcpy(s.instrs[2].name, "add"); s.instrs[2].latency = 1;
    strcpy(s.instrs[3].name, "store"); s.instrs[3].latency = 1;
    
    add_dep(&s, 0, 1);
    add_dep(&s, 1, 2);
    add_dep(&s, 2, 3);
    
    s.count = 4;
    schedule_list(&s);
    
    printf("Scheduled order:\n");
    for (int i = 0; i < s.sched_count; i++) {
        printf("%s ", s.instrs[s.scheduled[i]].name);
    }
    printf("\n");
    
    return 0;
}
