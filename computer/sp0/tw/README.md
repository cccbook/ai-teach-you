# 讓 AI 教你系統程式

> 用 c4 理解編譯器，用 mini-riscv-os 理解作業系統，用 xv6 理解 UNIX

---

## 目錄

### 第一部分：C 語言與記憶體模型

* [1. 從高階語言到機器碼——C 語言的本質](01-c_basics.md)
* [2. 記憶體模型——堆疊、堆積與靜態記憶體](02-memory_model.md)
* [3. 指針與指標算術——C 語言的核心](03-pointers.md)
* [4. 指標的應用——陣列、字串與函式指標](04-pointer_applications.md)

### 第二部分：從 C 到組語——編譯器基礎

* [5. c4：僅用四個函式打造的 C 編譯器](05-c4_overview.md)
* [6. 詞彙分析——如何將原始碼轉為 Token](06-lexer.md)
* [7. 語法分析——表達式與優先順序](07-parser.md)
* [8. 程式碼生成——從語法樹到虛擬機指令](08-codegen.md)
* [9. 虛擬機——堆疊式指令集架構](09-virtual_machine.md)

### 第三部分：自製編譯器工具鏈 cpy0

* [10. cpy0 工具鏈總覽——從原始碼到 RISC-V 執行檔](10-cpy0_overview.md)
* [11. Clang 前端——C 語言到 LLVM IR](11-clang_frontend.md)
* [12. ll0 後端——LLVM IR 到 RISC-V 組語](12-ll0_backend.md)
* [13. rv0 組譯器——組語到目標檔](13-rv0_assembler.md)
* [14. rv0 虛擬機——RISC-V 指令集模擬器](14-rv0_vm.md)
* [15. py0 編譯器——Python 到 qd0 位元組碼](15-py0_compiler.md)
* [16. qd0c 轉換器——qd0 位元組碼到 LLVM IR](16-qd0_to_llvm.md)

### 第四部分：RISC-V 處理器架構

* [17. RISC-V 指令集——精簡指令的設計哲學](17-riscv_instructions.md)
* [18. 組譯與反組譯——閱讀機器的語言](18-assembly.md)
* [19. 函式呼叫約定——堆疊框架與暫存器使用](19-call_convention.md)
* [20. LLVM IR——現代編譯器的中間表示](20-llvm_ir.md)

### 第五部分：用 mini-riscv-os 從零打造作業系統

* [21. 第一個 OS——UART 與 Hello World](21-helloos.md)
* [22. 從特權模式切換——Context Switch 基礎](22-context_switch.md)
* [23. 多工系統——任務切換與排程](23-multitasking.md)
* [24. 計時器中斷——Preemptive Scheduling](24-timer_interrupt.md)

### 第六部分：xv6 深度解析

* [25. xv6 架構總覽——UNIX v6 的 RISC-V 移植](25-xv6_overview.md)
* [26. 開機程序——從 BIOS 到核心](26-boot.md)
* [27. 行程管理——fork、exec 與 wait](27-process.md)
* [28. 檔案系統——inode 與日誌](28-filesystem.md)
* [29. 虛擬檔案系統——VFS 抽象層](29-vfs.md)
* [30. 記憶體管理——分頁與交換](30-memory.md)
* [31. 排程器——CFS 與實時排程](31-scheduler.md)

### 第七部分：現代工具鏈實踐

* [32. GCC 工具鏈——從原始碼到執行檔](32-gcc_toolchain.md)
* [33. LLVM/Clang——模組化編譯器框架](33-llvm_clang.md)
* [34. 交叉編譯——在 x86 上編譯 RISC-V 程式](34-cross_compile.md)
* [35. 除錯工具——GDB 與 LLDB](35-debugging.md)
* [36. 效能分析——perf 與火焰圖](36-profiling.md)

### 第八部分：進階主題

* [37. 連結腳本——控制記憶體佈局](37-linker_script.md)
* [38. 靜態分析——連結器如何解析符號](38-linking.md)
* [39. 作業系統虛擬化——從 xv6 到現代 kernel](39-os_virtualization.md)
* [40. 容器技術——namespace 與 cgroup](40-containers.md)
* [41. 系統程式的未來——eBPF 與 WebAssembly](41-future.md)

---

## 核心程式碼

### 參考來源

* [c4](https://github.com/rswier/c4) - 四函式 C 編譯器與堆疊式虛擬機
* [mini-riscv-os](https://github.com/cccriscv/mini-riscv-os) - 自製 RISC-V 作業系統（10 階段）
* [xv6-riscv](https://github.com/mit-pdos/xv6-riscv) - MIT 教學用 UNIX v6 (RISC-V 版)
* [cpy0/c0computer](https://github.com/ccc-c/c0computer) - 陳鍾誠自製編譯器工具鏈
* [riscv2os](https://github.com/riscv2os/riscv2os) - RISC-V 處理器到 OS 學習專案

### 本書範例程式碼

* [_code/c4/](_code/c4/) - c4 編譯器原始碼
* [_code/c4/hello.c](_code/c4/hello.c) - c4 測試範例
* [_code/mini-riscv-os/](_code/mini-riscv-os/) - 10 階段作業系統
* [_code/xv6/](_code/xv6/) - xv6-riscv 原始碼
* [_code/cpy0/](_code/cpy0/) - 自製編譯器工具鏈
* [_code/riscv2os/](_code/riscv2os/) - RISC-V 學習專案
* [_code/examples/](_code/examples/) - 本書額外範例程式

---

*最後更新：2026-03-22*
