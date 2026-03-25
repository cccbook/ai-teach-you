// C 效能分析範例

#include <stdio.h>
#include <time.h>

// 手動計時
void manual_timing() {
    clock_t start = clock();
    
    // 要測量的程式碼
    for (int i = 0; i < 1000000; i++) {
        // 做一些工作
    }
    
    clock_t end = clock();
    printf("花費時間: %.3f 秒\n", 
           (double)(end - start) / CLOCKS_PER_SEC);
}

// 使用 gettimeofday
#include <sys/time.h>

void timing_with_gettimeofday() {
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    // 測量程式碼
    
    gettimeofday(&end, NULL);
    double elapsed = (end.tv_sec - start.tv_sec) + 
                    (end.tv_usec - start.tv_usec) / 1000000.0;
    printf("花費時間: %.6f 秒\n", elapsed);
}
