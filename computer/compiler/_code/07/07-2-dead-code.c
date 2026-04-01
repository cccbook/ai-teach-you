int dead_code_elimination() {
    int x = 10;
    int y = 20;
    int unused = 100;
    if (x < y) {
        return x + y;
    }
    return unused;
}

int main() {
    return dead_code_elimination();
}
