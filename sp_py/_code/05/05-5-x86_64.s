# add 函數
add:
    lea    (%rdi,%rsi,1), %rax   # rax = rdi + rsi
    ret

# main 函數
main:
    push   %rbp
    mov    %rsp, %rbp
    mov    $2, %esi               # 第二個參數
    mov    $1, %edi               # 第一個參數
    call   add
    pop    %rbp
    ret