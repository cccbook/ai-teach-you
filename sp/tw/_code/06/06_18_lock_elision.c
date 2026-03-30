#include <stdio.h>
#include <stdbool.h>

typedef struct {
    char name[32];
    bool is_thread_local;
    bool escapes;
} LockObject;

typedef enum {
    LOCK_ACQUIRE,
    LOCK_RELEASE,
    NO_LOCK
} LockOp;

void eliminate_lock(const char* lock_name) {
    printf("  ELIMINATED: Lock on %s (thread-local object)\n", lock_name);
}

bool is_thread_local(LockObject* obj) {
    return obj->is_thread_local;
}

bool escapes_to_other_threads(LockObject* obj) {
    return obj->escapes;
}

void process_lock_op(LockObject* obj, LockOp op) {
    if (op == LOCK_ACQUIRE) {
        if (is_thread_local(obj) && !escapes_to_other_threads(obj)) {
            eliminate_lock(obj->name);
        } else {
            printf("  KEEP: Lock on %s (may be accessed by multiple threads)\n", obj->name);
        }
    }
}

int main() {
    printf("=== Lock Elision ===\n\n");
    
    LockObject local_obj = {"local_obj", true, false};
    LockObject shared_obj = {"shared_obj", false, true};
    LockObject escaped_obj = {"escaped_obj", true, true};
    
    printf("Test 1: Thread-local object\n");
    printf("  Object: %s (thread_local=%d, escapes=%d)\n",
           local_obj.name, local_obj.is_thread_local, local_obj.escapes);
    process_lock_op(&local_obj, LOCK_ACQUIRE);
    
    printf("\nTest 2: Shared object\n");
    printf("  Object: %s (thread_local=%d, escapes=%d)\n",
           shared_obj.name, shared_obj.is_thread_local, shared_obj.escapes);
    process_lock_op(&shared_obj, LOCK_ACQUIRE);
    
    printf("\nTest 3: Escaped object\n");
    printf("  Object: %s (thread_local=%d, escapes=%d)\n",
           escaped_obj.name, escaped_obj.is_thread_local, escaped_obj.escapes);
    process_lock_op(&escaped_obj, LOCK_ACQUIRE);
    
    printf("\nLock Elision Principle:\n");
    printf("  If an object is only visible to a single thread,\n");
    printf("  locks on that object are unnecessary and can be removed.\n");
    
    printf("\nBenefits:\n");
    printf("  - Eliminates lock overhead\n");
    printf("  - Reduces contention\n");
    printf("  - Enables more optimizations\n");
    
    return 0;
}
