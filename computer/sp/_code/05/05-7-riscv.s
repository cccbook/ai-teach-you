# add 函數
add:
    add    a0, a0, a1            # a0 = a0 + a1
    ret

# main 函數
    addi   a1, zero, 2           # a1 = 2
    addi   a0, zero, 1           # a0 = 1
    jal    ra, add               # 呼叫 add
    # a0 現在是結果