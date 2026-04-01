int constant_fold() {
    int a = 2 + 3;
    int b = a * 4;
    int c = b - 5;
    int d = 10 / 2;
    return c + d;
}

int main() {
    return constant_fold();
}
