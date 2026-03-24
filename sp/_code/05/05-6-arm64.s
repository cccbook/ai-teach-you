# add 函數
add:
    add    w0, w0, w1            # w0 = w0 + w1
    ret

# main 函數
main:
    stp    x29, x30, [sp, -16]!  # 保存 frame pointer
    mov    w1, 2                 # 第二個參數
    mov    w0, 1                 # 第一個參數
    bl     add                   # 呼叫 add
    ldp    x29, x30, [sp], 16    # 恢復
    ret