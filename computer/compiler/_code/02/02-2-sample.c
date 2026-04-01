int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int y = 20;
    int z = add(x, y);
    if (z > 5) {
        return z;
    }
    return 0;
}
