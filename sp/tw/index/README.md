# 專有名詞索引

本書籍涵蓋系統程式的核心領域，包含編譯器、作業系統、網路與雲端技術、AI 加速器等。以下是本書中出現的重要專有名詞：

## 程式語言

* [Fortran](fortran.md) : 最早的科學計算高階語言，1957 年由 IBM 開發。
* [C 語言](c.md) : 1972 年由 Dennis Ritchie 發明的系統程式設計語言，是 Unix 作業系統的開發語言。
* [C++](cpp.md) : 1985 年由 Bjarne Stroustrup 發明的物件導向程式語言，是 C 的超集。
* [Java](java.md) : 1995 年由 Sun Microsystems 開發的「一次編寫，到處執行」語言，運行於 JVM。
* [Python](python.md) : 1991 年由 Guido van Rossum 發明的直譯式腳本語言，以簡潔語法著稱。
* [LISP](lisp.md) : 1958 年由 John McCarthy 發明的函數式語言，是最古老的高階語言之一。
* [Haskell](haskell.md) : 1990 年發表的純函數式程式語言，以靜態類型與惰性求值著稱。
* [Prolog](prolog.md) : 1972 年發明的邏輯式程式語言，用於人工智慧與專家系統。
* [Rust](rust.md) : 2010 年由 Mozilla 開發的系統程式語言，提供記憶體安全保證。
* [Go](go.md) : 2009 年由 Google 開發的並發導向程式語言。

## 編譯器與直譯器

* [編譯器 (Compiler)](compiler.md) : 將原始碼翻譯為機器碼或位元組碼的工具。
* [直譯器 (Interpreter)](interpreter.md) : 直接執行原始碼的程式，不需預先編譯。
* [JIT 編譯器](jit.md) : Just-In-Time 編譯，執行時動態將程式碼編譯為機器碼。
* [Bytecode](bytecode.md) : 虛擬機執行的中介程式碼，如 Java bytecode、Python bytecode。
* [虛擬機 (VM)](virtual-machine.md) : 軟體模擬的計算機，如 JVM、CPython VM。

## 語法與語意分析

* [正則表達式 (Regex)](regex.md) : 描述字串模式的表示法。
* [有限自動機 (Finite Automaton)](finite-automaton.md) : 正則表達式的數學模型，分為 DFA 與 NFA。
* [文法 (Grammar)](grammar.md) : 描述語言語法的規則集合，如 CFG。
* [Tokenizer / Lexer](tokenizer.md) : 詞法分析器，將字元流轉換為 Token 序列。
* [Parser](parser.md) : 語法分析器，驗證語法並建立語法樹。
* [AST](ast.md) : 抽象語法樹，僅保留語意必要的資訊。
* [LL Parser](ll-parser.md) : 由上而下遞迴下降的語法分析方法。
* [LR Parser](lr-parser.md) : 由下而上移入歸約的語法分析方法。

## 中間表示與目的檔

* [IR](ir.md) : 中間表示，編譯器內部的程式碼表示形式。
* [TAC](tac.md) : 三位址碼，常用的 IR 形式。
* [SSA](ssa.md) : 靜態單一賦值 form，一種有利於最佳化的 IR。
* [ELF](elf.md) : Linux/Unix 可執行檔格式。
* [PE](pe.md) : Windows 可執行檔格式。
* [Mach-O](mach-o.md) : macOS/iOS 可執行檔格式。

## 處理器架構

* [x86/x64](x86.md) : Intel/AMD 處理器架構，個人電腦主流。
* [ARM](arm.md) : Advanced RISC Machines，行動裝置與嵌入式系統主流。
* [RISC-V](riscv.md) : 開放指令集架構，適用於學術與嵌入式場景。
* [ABI](abi.md) : 應用程式二進制介面，定義軟體模組間的呼叫約定。

## 記憶體管理

* [記憶體管理單元 (MMU)](mmu.md) : 硬體單元，負責虛擬記憶體到實體記憶體的轉換。
* [分頁 (Paging)](paging.md) : 記憶體管理技術，將記憶體劃分為固定大小的頁面。
* [分段 (Segmentation)](segmentation.md) : 記憶體管理技術，根據程式邏輯划分記憶體。
* [虛擬記憶體](virtual-memory.md) : 讓程式可以使用比實體記憶體更大位址空間的技術。
* [頁面置換演算法](page-replacement.md) : 當記憶體不足時，決定置換哪些頁面的演算法。
* [垃圾回收 (GC)](garbage-collection.md) : 自動回收不再使用的記憶體。

## 作業系統核心

* [Kernel](kernel.md) : 作業系統核心，管理硬體資源與提供系統服務。
* [程序 (Process)](process.md) : 作業系統調度的執行單位，擁有獨立的位址空間。
* [執行緒 (Thread)](thread.md) : 程序內的執行單位，共享程序的位址空間。
* [行程排程 (Scheduling)](scheduling.md) : 決定程序/執行緒執行順序的機制。
* [程序間通訊 (IPC)](ipc.md) : 程序間交換資料的機制，如 pipe、message queue、shared memory。
* [系統呼叫 (System Call)](system-call.md) : 使用者程式請求作業系統服務的介面。
* [檔案系統](filesystem.md) : 組織與存取儲存資料的軟體層。

## 即時作業系統

* [RTOS](rtos.md) : 即時作業系統，保證任務在時限內完成。
* [FreeRTOS](freertos.md) : 開放原始碼的輕量級 RTOS。
* [RT-Thread](rtthread.md) : 中國開發的開源 RTOS。

## 網路協定

* [OSI 模型](osi-model.md) : 網路通訊的七層參考模型。
* [TCP/IP](tcp-ip.md) : 網路通訊的事實標準，包含 TCP、UDP、IP 等協定。
* [TCP](tcp.md) : 可靠的連接導向傳輸協定。
* [UDP](udp.md) : 不可靠但快速的無連接傳輸協定。
* [Socket](socket.md) : 網路程式設計的 API，分為 Unix domain socket 與 network socket。
* [HTTP](http.md) : 超文字傳輸協定，Web 的基礎。
* [HTTPS](https.md) : HTTP 的安全版本，使用 TLS/SSL 加密。
* [DNS](dns.md) : 網域名稱系統，將網域名称轉換為 IP 位址。

## Web 技術

* [Web Server](web-server.md) : 處理 HTTP 請求的伺服器軟體，如 Nginx、Apache。
* [Load Balancer](load-balancer.md) : 分配流量到多台伺服器的元件。
* [CDN](cdn.md) : 內容傳遞網路，用於加速靜態內容分發。
* [反向代理](reverse-proxy.md) : 代表伺服器處理客戶端請求的代理伺服器。

## 雲端技術

* [虛擬化 (Virtualization)](virtualization.md) : 在單一硬體上模擬多個獨立環境的技術。
* [Docker](docker.md) : 容器化平台，將應用及其相依封裝為輕量級容器。
* [Kubernetes](kubernetes.md) : 容器編排平台，自動化容器部署與管理。
* [IaaS](iaas.md) : 基礎設施即服務，如 AWS EC2。
* [PaaS](paas.md) : 平台即服務，如 Heroku、AWS Elastic Beanstalk。
* [SaaS](saas.md) : 軟體即服務，如 Gmail、Google Docs。

## AI 加速器

* [GPU](gpu.md) : 圖形處理器，擅長平行運算，廣泛用於 AI 訓練與推論。
* [TPU](tpu.md) : Google 開發的張量處理器，專為機器學習設計。
* [NPU](npu.md) : 神經網路處理器，專注於 AI 推論的低功耗晶片。
* [FPGA](fpga.md) : 可程式化陣列，介於 GPU 與 ASIC 之間。
* [ASIC](asic.md) : 專用積體電路，為特定任務設計的客製化晶片。

## 機器學習框架

* [TensorFlow](tensorflow.md) : Google 開源的機器學習框架。
* [PyTorch](pytorch.md) : Facebook 開源的深度學習框架。
* [ONNX](onnx.md) : 開放神經網路交換格式，用於跨框架模型交換。

## 效能優化

* [SIMD](simd.md) : 單指令流多資料流，透過單一指令處理多筆資料。
* [向量化 (Vectorization)](vectorization.md) : 將運算表達為向量運算以利用 SIMD。
* [管線化 (Pipelining)](pipelining.md) : 將指令執行分為多個階段，重疊執行。
* [資料流分析 (Data Flow Analysis)](dataflow-analysis.md) : 分析程式資料流動以進行最佳化。
