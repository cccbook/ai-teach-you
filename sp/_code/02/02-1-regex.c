#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>

int main() {
    const char *text = "年齡是 25 歲，體重 65 公斤";
    regex_t re;
    regmatch_t match;
    
    printf("文字: %s\n\n", text);
    
    if (regcomp(&re, "[0-9]+", REG_EXTENDED) != 0) {
        fprintf(stderr, "正則表達式編譯失敗\n");
        return 1;
    }
    
    printf("找到的數字: ");
    const char *p = text;
    while (regexec(&re, p, 1, &match, 0) == 0) {
        int len = match.rm_eo - match.rm_so;
        char num[32] = {0};
        strncpy(num, p + match.rm_so, len);
        printf("%s ", num);
        p += match.rm_eo;
    }
    printf("\n\n");
    
    if (regcomp(&re, "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", 
                REG_EXTENDED) == 0) {
        const char *emails = "聯絡: user@example.com 或 admin@test.org";
        printf("文字: %s\n", emails);
        printf("找到的 email: ");
        p = emails;
        while (regexec(&re, p, 1, &match, 0) == 0) {
            int len = match.rm_eo - match.rm_so;
            char email[128] = {0};
            strncpy(email, p + match.rm_so, len);
            printf("%s ", email);
            p += match.rm_eo;
        }
        printf("\n");
    }
    
    regfree(&re);
    return 0;
}
