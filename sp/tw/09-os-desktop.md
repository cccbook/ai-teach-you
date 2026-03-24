# 9. 高階作業系統

## 9.1 Windows 核心結構

[程式檔案：09-1-windows-kernel.c](../_code/09/09-1-windows-kernel.c)
```c
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
```

```python
"""
Windows 核心結構模擬
"""

class WindowsKernel:
    """Windows 核心模擬"""
    
    def __init__(self):
        self.objects = {}  # 核心物件
        self.process_list = []
```

[程式檔案：09-3-macos-xnu.c](../_code/09/09-3-macos-xnu.c)
```c
// macOS / XNU 核心概念

/*
XNU 核心架構：
+-------------------+
|   IOKit           |  <- 物件導向驅動框架
+-------------------+
+-------------------+
|   BSD Layer       |  <- Unix 相容（程序、檔案、網路）
+-------------------+
+-------------------+
|   Mach            |  <- 微核心（IPC、虛擬記憶體）
+-------------------+
*/

// Mach 訊息傳遞
#include <mach/mach.h>

kern_return_t inter_process_comm() {
    mach_port_t port;
    mach_port_allocate(mach_task_self(), 
                      MACH_PORT_RIGHT_RECEIVE, &port);
    
    // 傳送訊息
    struct {
        mach_msg_header_t header;
        char data[256];
    } msg;
    
    mach_msg(&msg, MACH_SEND_MSG, sizeof(msg), 0, port, 0, 0);
}

// BSD 系統呼叫
#include <sys/syscall.h>

int main() {
    // fork()
    pid_t pid = fork();
    
    // execve()
    execve("/bin/ls", argv, envp);
    
    // mmap()
    void *mem = mmap(NULL, 4096, 
                    PROT_READ | PROT_WRITE,
                    MAP_ANONYMOUS, -1, 0);
    
    return 0;
}
```

[程式檔案：09-4-macos-xnu.py](../_code/09/09-4-macos-xnu.py)
```python
"""
macOS XNU 核心模擬
"""

class XNUKernel:
    """XNU 核心模擬"""
    
    def __init__(self):
        self.mach_ports = {}  # Mach 連接埠
        self.bsd_processes = {}
    
    def mach_port_allocate(self):
        """配置 Mach 連接埠"""
        port = len(self.mach_ports)
        self.mach_ports[port] = {'rights': ['receive']}
        print(f"配置 Mach 連接埠: {port}")
        return port
    
    def ipc_send(self, port, message):
        """IPC 訊息傳遞"""
        print(f"傳送訊息到連接埠 {port}: {message[:20]}...")
    
    def bsd_process_create(self):
        """建立 BSD 程序"""
        pid = len(self.bsd_processes) + 1
        self.bsd_processes[pid] = {'status': 'running'}
        print(f"建立 BSD 程序: PID {pid}")
        return pid

# IOKit 概念
class IOKitDriver:
    """IOKit 驅動框架"""
    
    def __init__(self):
        self.services = []
    
    def register_service(self, name):
        """註冊服務"""
        service = {'name': name, 'properties': {}}
        self.services.append(service)
        print(f"IOKit 服務註冊: {name}")
    
    def match(self, name):
        """配對裝置"""
        for service in self.services:
            if service['name'] == name:
                print(f"找到匹配的 IOKit 服務")
                return service
        return None

# XNU 特色
print("""
=== XNU 核心特色 ===

1. Mach 層
   - 微核心設計
   - 訊息傳遞 IPC
   - 虛擬記憶體管理
   - 巢狀任務（Task）

2. BSD 層
   - Unix 相容性
   - POSIX 介面
   - 檔案系統（APFS、HFS+）
   - 網路堆疊（BSD）

3. IOKit
   - 物件導向（C++）
   - 熱插拔支援
   - 電源管理

4. 安全性
   - SIP（System Integrity Protection）
   - Sandbox
   - Code Signing
""")
```

## 9.3 桌面系統的行程與記憶體管理

[程式檔案：09-4-memory-management.py](../_code/09/09-4-memory-management.py)
```python
"""
桌面系統的記憶體管理
"""

class DesktopMemoryManager:
    """桌面系統記憶體管理器"""
    
    def __init__(self):
        self.processes = {}
        self.swap_space = {}
        self.page_size = 4096
    
    def allocate_virtual(self, size):
        """配置虛擬記憶體"""
        pages_needed = (size + self.page_size - 1) // self.page_size
        return pages_needed * self.page_size
    
    def page_fault_handler(self, process_id, address):
        """頁缺失處理"""
        # 1. 檢查區段表
        # 2. 從磁碟載入頁面（或分配新頁）
        # 3. 更新分頁表
        print(f"頁缺失: 程序 {process_id}, 位址 {address}")
        return True
    
    def swap_out(self, process_id):
        """換出"""
        print(f"換出程序 {process_id} 到 swap")
    
    def swap_in(self, process_id):
        """換入"""
        print(f"換入程序 {process_id} 從 swap")

# Windows 記憶體管理
class WindowsMemoryManager:
    """Windows 記憶體管理"""
    
    def __init__(self):
        self.working_sets = {}
        self.page_priority = {}
    
    def set_working_set(self, pid, min_size, max_size):
        """設定工作集"""
        self.working_sets[pid] = {'min': min_size, 'max': max_size}
        print(f"程序 {pid} 工作集: {min_size}-{max_size} KB")
    
    def memory_manager_features(self):
        """記憶體管理特性"""
        print("""
=== Windows 記憶體管理 ===

1. 分頁管理
   - 請求式分頁
   - 工作集管理
   - 硬碟傾印

2. 虛擬記憶體
   - 4GB 虛擬位址空間（32位）
   - 分頁檔動態調整

3. 記憶體傾印
   - 完整傾印
   - 核心傾印
   - 主動態傾印
""")

# macOS 記憶體管理
class MacOSMemoryManager:
    """macOS 記憶體管理"""
    
    def __init__(self):
        self.compressed_memory = {}
    
    def compress_memory(self, process_id):
        """記憶體壓縮"""
        print(f"壓縮程序 {process_id} 的記憶體")
    
    def vm_features(self):
        """VM 特性"""
        print("""
=== macOS 虛擬記憶體 ===

1. 分頁
   - 延遲分頁
   - 壓縮記憶體（vm_compressor）

2. 共享記憶體
   - Zero-fill 頁面共享
   - Copy-on-write

3. 安全性
   - ASLR
   - DEP/NX
""")
```

## 9.4 圖形介面與視窗系統

[程式檔案：09-6-xwindow.c](../_code/09/09-6-xwindow.c)
```c
// X Window System 範例

#include <X11/Xlib.h>

int main() {
    Display *display = XOpenDisplay(NULL);
    Window window = XCreateSimpleWindow(
        display, DefaultRootWindow(display),
        100, 100, 400, 300,
        1, BlackPixel(display, 0), WhitePixel(display, 0)
    );
    
    XSelectInput(display, window, ExposureMask | KeyPressMask);
    XMapWindow(display, window);
    
    XEvent event;
    while (1) {
        XNextEvent(display, &event);
        if (event.type == Expose) {
            GC gc = DefaultGC(display, 0);
            XDrawString(display, window, gc, 50, 50, "Hello X!", 8);
        }
    }
    
    XCloseDisplay(display);
    return 0;
}

// Wayland 範例（較新）
/*
Wayland 協定：
- Compositor 負責合成
- 用戶端直接與 compositor 通訊
- 少了 X Server 這層
*/
```

[程式檔案：09-7-window-system.py](../_code/09/09-7-window-system.py)
```python
"""
視窗系統模擬
"""

class XWindowSystem:
    """X Window 系統模擬"""
    
    def __init__(self):
        self.displays = {}
        self.windows = {}
        self.events = []
    
    def open_display(self):
        """開啟顯示器"""
        display_id = len(self.displays)
        self.displays[display_id] = {'screens': [0]}
        print(f"開啟顯示器 :{display_id}")
        return f":{display_id}"
    
    def create_window(self, display, x, y, width, height):
        """建立視窗"""
        window_id = len(self.windows)
        self.windows[window_id] = {
            'display': display,
            'x': x, 'y': y,
            'width': width, 'height': height,
            'visible': True
        }
        print(f"建立視窗 {window_id}: {width}x{height}")
        return window_id
    
    def draw_text(self, window, text):
        """繪製文字"""
        print(f"在視窗 {window} 繪製: {text}")

# Wayland 概念
class WaylandCompositor:
    """Wayland 合成器"""
    
    def __init__(self):
        self.surfaces = []
        self.clients = []
    
    def register_client(self, client):
        """註冊客戶端"""
        self.clients.append(client)
        print(f"Wayland 客戶端註冊: {client}")
    
    def composite(self):
        """合成畫面"""
        print("合成所有表面到最終畫面")
    
    def wayland_features(self):
        """Wayland 特性"""
        print("""
=== Wayland vs X11 ===

Wayland:
- 直接與 compositor 通訊
- 無 server/client 分離
- 更簡單的協定
- 更好的 3D 整合

X11:
- 網路透明
- 向後相容
- 成熟的工具生態
""")

# 測試
x = XWindowSystem()
display = x.open_display()
window = x.create_window(display, 100, 100, 800, 600)
x.draw_text(window, "Hello, World!")
```