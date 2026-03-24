// x86-64 System V ABI
// 參數傳遞: rdi, rsi, rdx, rcx, r8, r9
// 返回值: rax
// 被呼叫者保存: rbx, rbp, r12, r13, r14, r15
// 呼叫者保存: rax, rcx, rdx, rsi, rdi, r8, r9, r10, r11

// 棧框架
void function(int a, int b) {
    // a -> rdi, b -> rsi
    int local = a + b;  // local 在棧上
    // 返回值在 rax
}