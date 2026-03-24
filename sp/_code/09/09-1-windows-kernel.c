// Windows 核心概念

/*
Windows 核心架構：
+-------------------+
|   User Mode       |  <- 應用程式、Win32 API
+-------------------+
        |
+-------------------+
|   Executive       |  <- 核心服務（I/O、程序、記憶體）
+-------------------+
+-------------------+
|   Kernel          |  <- 核心（排程、Synchronization）
+-------------------+
+-------------------+
|   HAL             |  <- 硬體抽象層
+-------------------+
*/

// Windows API 範例
#include <windows.h>

int main() {
    // 建立程序
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));
    
    CreateProcess(
        "C:\\Windows\\System32\\notepad.exe",
        NULL, NULL, NULL, FALSE,
        0, NULL, NULL, &si, &pi
    );
    
    // 執行緒
    DWORD tid;
    HANDLE thread = CreateThread(
        NULL, 0,
        (LPTHREAD_START_ROUTINE)thread_func,
        NULL, 0, &tid
    );
    
    // 記憶體配置
    LPVOID mem = VirtualAlloc(
        NULL, 4096,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_READWRITE
    );
    
    // 檔案操作
    HANDLE file = CreateFile(
        "test.txt",
        GENERIC_WRITE, 0, NULL,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL, NULL
    );
    
    CloseHandle(file);
    return 0;
}
