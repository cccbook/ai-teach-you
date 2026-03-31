#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

typedef enum { TYPE_NUM, TYPE_SYM, TYPE_CONS, TYPE_FUNC, TYPE_NIL } ValueType;

typedef struct Value {
    ValueType type;
    int num;
    char sym[32];
    struct Value *car;
    struct Value *cdr;
    struct Value *params;
    struct Value *body;
} Value;

Value* make_num(int n) { 
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_NUM; v->num = n; 
    v->car = v->cdr = v->params = v->body = NULL;
    return v; 
}

Value* make_sym(const char* s) { 
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_SYM; strcpy(v->sym, s); 
    v->car = v->cdr = v->params = v->body = NULL;
    return v; 
}

Value* make_cons(Value* car, Value* cdr) { 
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_CONS; v->car = car; v->cdr = cdr; 
    v->params = v->body = NULL;
    return v; 
}

Value* make_nil() {
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_NIL;
    v->car = v->cdr = v->params = v->body = NULL;
    return v;
}

int is_list(Value* v) {
    while (v && v->type == TYPE_CONS) v = v->cdr;
    return v && v->type == TYPE_NIL;
}

Value* eval_expr(Value* expr);
Value* eval_list(Value* list);
Value* lookup_var(const char* name);
void define_var(const char* name, Value* val);

Value* env[26];
int env_count = 0;

Value* lookup_var(const char* name) {
    for (int i = 0; i < env_count; i++) {
        if (strcmp(name, env[i]->sym) == 0) return env[i];
    }
    return NULL;
}

void define_var(const char* name, Value* val) {
    Value* existing = lookup_var(name);
    if (existing) {
        existing->num = val->num;
        return;
    }
    Value* v = make_sym(name);
    v->num = val->num;
    env[env_count++] = v;
}

Value* eval_expr(Value* expr) {
    if (!expr) return make_nil();
    
    if (expr->type == TYPE_NUM) return expr;
    
    if (expr->type == TYPE_SYM) {
        Value* v = lookup_var(expr->sym);
        return v ? v : expr;
    }
    
    if (expr->type == TYPE_CONS) {
        Value* op = expr->car;
        Value* args = expr->cdr;
        
        if (op->type == TYPE_SYM) {
            if (strcmp(op->sym, "+") == 0) {
                int sum = 0;
                Value* p = args;
                while (p && p->type == TYPE_CONS) {
                    sum += eval_expr(p->car)->num;
                    p = p->cdr;
                }
                return make_num(sum);
            }
            if (strcmp(op->sym, "-") == 0) {
                int diff = 0;
                Value* p = args;
                if (p && p->type == TYPE_CONS) {
                    diff = eval_expr(p->car)->num;
                    p = p->cdr;
                }
                while (p && p->type == TYPE_CONS) {
                    diff -= eval_expr(p->car)->num;
                    p = p->cdr;
                }
                return make_num(diff);
            }
            if (strcmp(op->sym, "*") == 0) {
                int prod = 1;
                Value* p = args;
                while (p && p->type == TYPE_CONS) {
                    prod *= eval_expr(p->car)->num;
                    p = p->cdr;
                }
                return make_num(prod);
            }
            if (strcmp(op->sym, "/") == 0) {
                Value* p = args;
                if (!p || p->type != TYPE_CONS) return make_num(0);
                int result = eval_expr(p->car)->num;
                p = p->cdr;
                while (p && p->type == TYPE_CONS) {
                    result /= eval_expr(p->car)->num;
                    p = p->cdr;
                }
                return make_num(result);
            }
        }
    }
    
    return make_nil();
}

Value* list(int count, ...) {
    va_list args;
    va_start(args, count);
    Value* head = make_nil();
    Value* tail = NULL;
    for (int i = 0; i < count; i++) {
        Value* v = va_arg(args, Value*);
        Value* cell = make_cons(v, make_nil());
        if (tail) tail->cdr = cell;
        else head = cell;
        tail = cell;
    }
    va_end(args);
    return head;
}

int main() {
    Value* expr = make_cons(make_sym("+"), 
        make_cons(make_num(2), make_cons(make_num(3), make_nil())));
    Value* result = eval_expr(expr);
    printf("(+ 2 3) => %d\n", result->num);
    
    define_var("x", make_num(10));
    define_var("y", make_num(20));
    
    Value* expr2 = make_cons(make_sym("+"), 
        make_cons(make_sym("x"), make_cons(make_sym("y"), make_nil())));
    result = eval_expr(expr2);
    printf("(+ x y) => %d\n", result->num);
    
    Value* expr3 = make_cons(make_sym("*"),
        make_cons(make_num(3), 
            make_cons(make_cons(make_sym("+"), 
                make_cons(make_num(4), make_cons(make_num(5), make_nil()))), 
                make_nil())));
    result = eval_expr(expr3);
    printf("(* 3 (+ 4 5)) => %d\n", result->num);
    
    return 0;
}
