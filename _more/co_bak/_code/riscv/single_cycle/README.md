# Single Cycle RISC-V 處理器

本目錄包含一個支援 RV32I 基礎指令集的 **Single Cycle (單周期) RISC-V 處理器** 的 Verilog 實作，以及測試框架。

---

## 目錄結構

```
single_cycle/
├── README.md          本說明文件
├── program.asm       組合語言測試程式（含機器碼註解）
├── program.txt       機器碼（HEX 格式，供 imem 載入）
├── defs.v            全域參數定義（指令碼、ALU 操作碼等）
├── alu.v             算術邏輯單元
├── regfile.v         暫存器檔案（32 個 x0~x31）
├── imem.v            指令記憶體
├── dmem.v            資料記憶體
├── imm_gen.v         立即數產生器
├── control.v         控制單元（解碼指令、產生控制訊號）
├── datapath.v        資料路徑（連接所有模組）
├── top.v             頂層模組
├── tb_top.v          測試平台
└── Makefile          編譯與執行腳本
```

---

## 支援的指令

| 指令類型 | 支援的指令 |
|---------|-----------|
| **立即數運算** | `addi`, `slli`, `slti`, `sltiu`, `xori`, `srli`, `srai`, `ori`, `andi` |
| **暫存器運算** | `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `sra`, `or`, `and` |
| **載入/儲存** | `lw`, `sw` |
| **分支** | `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu` |
| **跳躍** | `jal`, `jalr` |
| **上半部載入** | `lui`, `auipc` |

---

## 模組說明

### `defs.v` — 全域參數
定義所有常數：資料寬度 (`WORD_WIDTH=32`)、指令碼 (`OPCODE_*`)、funct3/funct7 值、以及 ALU 操作碼 (`ALU_OP_*`)。

### `alu.v` — 算術邏輯單元
接收兩個 32 位元輸入 `a`、`b` 和 4 位元 `alu_op`，輸出 32 位元結果。支援加、減、邏輯移位、算術移位、比較等 10 種操作。

### `regfile.v` — 暫存器檔案
32 個 32 位元暫存器 (x0~x31)，其中 **x0 永遠為零**。支援雙口讀取 (非同步) 和單口寫入 (同步)。

### `imem.v` — 指令記憶體
256 個 word 的 ROM，由 `program.txt` 初始化。每條指令 32 位元，8 位元位址索引 (即 byte 位址除以 4)。

### `dmem.v` — 資料記憶體
256 個 word 的 RAM，支援同步寫入、非同步讀取。用於 `lw`/`sw` 指令。

### `imm_gen.v` — 立即數產生器
根據指令的 opcode 欄位，自動生成正確的符號延伸立即數：
- **I-type**（load/addi）：`imm[31:0] = {20{inst[31]}, inst[31:20]}`
- **S-type**（store）：`imm = {20{inst[31]}, inst[31:25], inst[11:7]}`
- **B-type**（branch）：`imm = {19{inst[31]}, inst[31], inst[7], inst[30:25], inst[11:8], 1'b0}`
- **U-type**（lui/auipc）：`imm = {inst[31:12], 12'b0}`
- **J-type**（jal）：`imm = {11{inst[31]}, inst[31], inst[19:12], inst[20], inst[30:21], 1'b0}`

### `control.v` — 控制單元
純組合邏輯，解碼 7 位元 opcode、3 位元 funct3、7 位元 funct7，產生所有控制訊號：
- `reg_write`：寫回暫存器
- `mem_read`/`mem_write`：記憶體讀寫
- `branch`：分支指令
- `alu_op`：ALU 操作碼
- `alu_src_b_sel`：第二運算元選擇 (rs2 / imm / lui 立即數)

### `datapath.v` — 資料路徑
連接所有模組，實作單周期處理器的五大階段（在同一週期內完成）：
1. **Instruction Fetch**：從 imem 取出指令，PC + 4
2. **Instruction Decode**：讀取暫存器、產生立即數
3. **Execute**：ALU 運算或位址計算
4. **Memory Access**：記憶體讀寫
5. **Write Back**：結果寫回暫存器檔案

### `top.v` — 頂層模組
實例化 `datapath` 和 `control`，是對外接口。

---

## 測試程式 `program.asm`

### 結構
```
第一段 (22 條 ADDI)：x1=0, x2=1, x3=2, ... x20=19, x10=28
第二段 (234 條 ADD)：x11 = x10+x5, x12 = x11+x6, ...  (累加鏈)
```

### 為什麼用這種設計？
- **ADDI 段**：建立費伯那契-like 序列的初始值，測試立即數載入
- **ADD 段**：234 條 `add rd, rs1, rs2` 形成滾動累加鏈，每條指令都依賴前一個結果，大量 ALU 運算，適合驗證資料路徑正確性
- 迴圈使用 x1~x31 滾動寫入，避免單一暫存器溢出
- 最後沒有 `ebreak`/`nop`，遇 `0x00000013` (addi x0, x0, 0) 自然停止

### 執行後的預期暫存器狀態（Single Cycle）

執行 256 個週期後，x1~x31 會累積費伯那契-like 的數值：
- `x1 = 0`  (仍是第一個加數，因為 x31→x26 的滾動最終回到 x1)
- `x2 = 1`
- `x3 = 2`
- ...
- `x9 = 8`
- `x10 = 9`  (被 ADD 鏈最後幾步更新)
- `x20 = 110` (0x6e)
- `x28 = 152` (0x98)
- `x31 = 155` (0x9b)

---

## 編譯與執行

### 必要工具
- **Icarus Verilog** (`iverilog`) 和 **VVP** (`vvp`)

在 macOS 上可透過 Homebrew 安裝：
```bash
brew install icarus-verilog
```

### 編譯
```bash
iverilog -o tb_top.vvp -s tb_top \
    tb_top.v top.v datapath.v control.v alu.v \
    regfile.v imem.v dmem.v imm_gen.v defs.v
```

### 執行模擬
```bash
vvp tb_top.vvp
```

### 使用 Makefile
```bash
make          # 編譯
make run      # 執行模擬
make clean    # 清除產出檔案
```

---

## 與 Pipeline 版本的差異

| 特性 | Single Cycle | 5-Stage Pipeline |
|------|-------------|-----------------|
| 時脈頻率 | 最低（取最慢階段） | 較高（各階段流水） |
| CPI | 1 | 1（理想）/ >1（有 hazards） |
| 每指令延遲 | 長（所有階段串聯） | 短（每級延遲 = 總延遲/5） |
| 面積 | 較小（無暫存器） | 較大（5 組 pipeline register） |
| Control hazards | 立即處理 | 需要 flush |
| Data hazards | 不需要 forwarding | 需要 forwarding + stall |
| Verilog 檔案 | 10 個模組 | 更多模組（hazard, forwarding 等） |
