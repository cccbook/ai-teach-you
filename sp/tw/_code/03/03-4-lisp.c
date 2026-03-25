#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_ENV 100
#define MAX_STACK 50

typedef enum { TYPE_NUM, TYPE_SYM, TYPE_CONS, TYPE_FUNC, TYPE_NIL } ValueType;

typedef struct Value {
    ValueType type;
    int num;
    char sym[32];
    struct Value* car;
    struct Value* cdr;
    struct Value* params;
    struct Value* body;
} Value;

Value* nil;

Value* make_num(int n) {
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_NUM;
    v->num = n;
    return v;
}

Value* make_sym(const char* s) {
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_SYM;
    strcpy(v->sym, s);
    return v;
}

Value* make_cons(Value* car, Value* cdr) {
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_CONS;
    v->car = car;
    v->cdr = cdr;
    return v;
}

Value* make_func(Value* params, Value* body) {
    Value* v = (Value*)malloc(sizeof(Value));
    v->type = TYPE_FUNC;
    v->params = params;
    v->body = body;
    return v;
}

Value* env[MAX_ENV];
int env_size = 0;

void env_set(const char* name, Value* v) {
    for (int i = 0; i < env_size; i++) {
        if (strcmp(env[i]->sym, name) == 0) {
            env[i] = v;
            return;
        }
    }
    Value* sym = make_sym(name);
    env[env_size++] = sym;
    env[env_size++] = v;
}

Value* env_get(const char* name) {
    for (int i = 0; i < env_size; i++) {
        if (strcmp(env[i]->sym, name) == 0)
            return env[i + 1];
    }
    return NULL;
}

Value* eval(Value* expr);

Value* eval_list(Value* list) {
    if (!list || list->type == TYPE_NIL) return list;
    return make_cons(eval(list->car), eval_list(list->cdr));
}

Value* eval_prim(const char* op, Value* args) {
    int a = args->car->num;
    int b = args->cdr->car->num;
    if (strcmp(op, "+") == 0) return make_num(a + b);
    if (strcmp(op, "-") == 0) return make_num(a - b);
    if (strcmp(op, "*") == 0) return make_num(a * b);
    if (strcmp(op, "/") == 0) return make_num(a / b);
    if (strcmp(op, "=") == 0) return make_sym(a == b ? "t" : "nil");
    if (strcmp(op, "<") == 0) return make_sym(a < b ? "t" : "nil");
    return NULL;
}

Value* eval_lambda(Value* params, Value* args) {
    if (!params || params->type == TYPE_NIL) return eval(args->car);
    env_set(params->car->sym, args->car);
    return eval_lambda(params->cdr, args->cdr);
}

Value* eval(Value* expr) {
    if (!expr) return NULL;
    
    if (expr->type == TYPE_NUM) return expr;
    
    if (expr->type == TYPE_SYM) {
        if (strcmp(expr->sym, "t") == 0) return expr;
        if (strcmp(expr->sym, "nil") == 0) return NULL;
        Value* v = env_get(expr->sym);
        return v ? v : expr;
    }
    
    if (expr->type == TYPE_CONS) {
        Value* op = expr->car;
        Value* args = expr->cdr;
        
        if (op->type == TYPE_SYM) {
            if (strcmp(op->sym, "quote") == 0) return args->car;
            if (strcmp(op->sym, "if") == 0) {
                Value* cond = eval(args->car);
                if (cond && cond->type != TYPE_NIL)
                    return eval(args->cdr->car);
                return args->cdr->cdr->car ? eval(args->cdr->cdr->car) : NULL;
            }
            if (strcmp(op->sym, "def") == 0) {
                Value* val = eval(args->cdr->car);
                env_set(args->car->sym, val);
                return NULL;
            }
            if (strcmp(op->sym, "lambda") == 0)
                return make_func(args->car, args->cdr->car);
            if (strcmp(op->sym, "+") == 0 || strcmp(op->sym, "-") == 0 ||
                strcmp(op->sym, "*") == 0 || strcmp(op->sym, "/") == 0 ||
                strcmp(op->sym, "=") == 0 || strcmp(op->sym, "<") == 0)
                return eval_prim(op->sym, eval_list(args));
        }
        
        Value* fn = eval(op);
        if (fn && fn->type == TYPE_FUNC)
            return eval_lambda(fn->params, eval_list(args));
        
        return NULL;
    }
    
    return expr;
}

void print_value(Value* v) {
    if (!v) { printf("nil"); return; }
    if (v->type == TYPE_NUM) { printf("%d", v->num); return; }
    if (v->type == TYPE_SYM) { printf("%s", v->sym); return; }
    if (v->type == TYPE_CONS) {
        printf("(");
        print_value(v->car);
        while (v->cdr && v->cdr->type == TYPE_CONS) {
            v = v->cdr;
            printf(" ");
            print_value(v->car);
        }
        printf(")");
        return;
    }
    if (v->type == TYPE_FUNC) { printf("<function>"); return; }
}

Value* parse_number(const char* s) {
    return make_num(atoi(s));
}

Value* parse(const char* s) {
    static char buf[256];
    static int pos = 0;
    if (s) { strcpy(buf, s); pos = 0; }
    while (buf[pos] == ' ') pos++;
    if (buf[pos] == '(') {
        pos++; Value* car = parse(NULL);
        Value* cdr = make_cons(car, parse(NULL));
        while (buf[pos] == ' ') pos++;
        if (buf[pos] == ')') pos++;
        return cdr;
    }
    if (buf[pos] == ')') { pos++; return NULL; }
    int i = 0;
    while (buf[pos] && buf[pos] != ' ' && buf[pos] != ')') 
        buf[i++] = buf[pos++];
    buf[i] = 0;
    if (isdigit(buf[0]) || (buf[0] == '-' && isdigit(buf[1])))
        return make_num(atoi(buf));
    return make_sym(buf);
}

int main() {
    nil = make_sym("nil");
    
    // (+ 2 3)
    Value* expr = make_cons(make_sym("+"), 
                           make_cons(make_num(2),
                           make_cons(make_num(3), NULL)));
    printf("(+ 2 3) = "); print_value(eval(expr)); printf("\n");
    
    // (def x 10)
    env_set("x", make_num(10));
    printf("(def x 10) = nil\n");
    
    // (+ x 5)
    Value* x = make_sym("x");
    expr = make_cons(make_sym("+"), make_cons(x, make_cons(make_num(5), NULL)));
    printf("(+ x 5) = "); print_value(eval(expr)); printf("\n");
    
    return 0;
}
