# 41. 系統程式的未來——eBPF 與 WebAssembly

## 41.1 eBPF (extended Berkeley Packet Filter)

### 41.1.1 什麼是 eBPF？

eBPF 是 Linux 核心的高效能追蹤框架：
- 在核心空間執行位元組碼
- 安全（經過驗證）
- 即時編譯（JIT）

### 41.1.2 應用場景

- **效能分析**：追蹤系統呼叫、熱點函式
- **網路**：封包過濾、負載平衡
- **安全**：異常偵測、存取控制

### 41.1.3 範例

```c
// 使用 bpftrace 追蹤系統呼叫
bpftrace -e 'tracepoint:syscalls:sys_enter_open { printf("%s\n", comm); }'
```

### 41.1.4 工具

| 工具 | 用途 |
|------|------|
| bpftrace | 高階追蹤語言 |
| BCC | C 框架 |
| bpftool | 管理和除錯 |

## 41.2 WebAssembly

### 41.2.1 什麼是 WebAssembly？

WebAssembly (Wasm) 是一種二進位指令格式：
- 可在任何環境執行
- 高效能
- 安全（記憶體隔離）

### 41.2.2 為何重要？

- **跨平台**：一次編譯，到處執行
- **高效能**：接近原生速度
- **安全**：沙箱執行

### 41.2.3 範例

```c
// C 程式碼
int add(int a, int b) {
    return a + b;
}
```

編譯：
```bash
# 編譯到 WebAssembly
emcc add.c -s WASM=1 -o add.js
```

使用：
```javascript
const result = Module.cwrap('add', 'number', ['number', 'number']);
console.log(result(1, 2));  // 3
```

## 41.3 比較

| 特性 | eBPF | WebAssembly |
|------|------|-------------|
| 執行環境 | Linux 核心空間 | 瀏覽器/伺服器 |
| 語言 | C/Go/Rust | C/C++/Rust/Go |
| 用途 | 系統追蹤、網路 | 跨平台執行 |
| 效能 | 極高 | 高 |

## 41.4 趨勢

### 41.4.1 eBPF 在系統程式的應用

- **Cilium**：基於 eBPF 的容器網路
- **Falco**：安全監控
- **Katran**：負載平衡

### 41.4.2 WebAssembly 的擴展

- **WASI**：WebAssembly 系統介面
- **WasmEdge**：邊緣運算
- **Extism**：插件系統

## 41.5 學習路徑

1. **系統程式基礎**：記憶體、排程、I/O
2. **Linux 核心**：系統呼叫、驅動程式
3. **虛擬化**：容器、VM
4. **現代工具**：eBPF、WebAssembly

## 41.6 小結

本章節我們學習了：
- eBPF 的概念和應用
- WebAssembly 的基礎
- 兩種技術的比較
- 系統程式的未來趨勢

## 41.7 習題

1. 使用 bpftrace 分析一個程式
2. 將 C 程式編譯到 WebAssembly
3. 研究 WASI 的系統介面
4. 探索 eBPF 的實際應用
5. 比較 Wasm 和 native 的效能差異
