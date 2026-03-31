# 第 1 章：計算理論導論

## 概述

計算理論（Theory of Computation）是計算機科學的基石，它回答一個看似簡單卻深刻的問題：**什麼是計算？什麼可以計算？什麼不能計算？**

本章將介紹計算理論的基本概念、發展歷史，以及這門學問為何如此重要。

## 1.1 從算盤到量子電腦

人類使用計算工具的歷史可追溯至四千年前的美索不達米亞。那時的書記官使用泥板和算術進行記錄與計算。然而，真正意義上的「計算機」概念，要到二十世紀才逐漸成形。

### 1.1.1 機械計算的時代

1822年，英國數學家查爾斯·巴貝奇（Charles Babbage）設計了差分機（Difference Engine），這是第一台能夠自動計算多項式值的機械裝置。十年後，他開始設計更雄心勃勃的分析機（Analytical Engine），這台機器已經具備了現代電腦的核心概念：

- **儲存裝置**（相當於記憶體）
- **運算裝置**（相當於CPU）
- **控制系統**（使用打孔卡片，相當於程式）

巴貝奇的朋友，詩人拜倫的女兒愛達·勒芙蕾絲（Ada Lovelace）為分析機寫下了第一個演算法，被後世尊稱為「世界上第一位程式設計師」。

[程式檔案：01-1-analytical-engine.py](../_code/01/01-1-analytical-engine.py)

```python
"""
模擬巴貝奇分析機的基本概念
這不是完整的實現，只是展示其核心思想
"""

class AnalyticalEngine:
    """巴貝奇分析機的簡化模擬"""
    
    def __init__(self):
        self.store = [0] * 1000  # 儲存裝置：1000個暫存器
        self.mill = 0            # 運算裝置：類似累加器
        self.program = []         # 程式：操作序列
    
    def load(self, register, value):
        """將值載入指定暫存器"""
        self.store[register] = value
    
    def add(self, target, source):
        """將 source 暫存器的值加到 target"""
        self.store[target] += self.store[source]
    
    def sub(self, target, source):
        """從 target 減去 source"""
        self.store[target] -= self.store[source]
    
    def print_register(self, register):
        """輸出暫存器內容"""
        print(f"寄存器[{register}] = {self.store[register]}")


# 範例：計算 1 + 2 + 3 + ... + 10
engine = AnalyticalEngine()
n = 10

# 初始化
engine.load(0, n)        # R0 = 10
engine.load(1, 1)        # R1 = 1 (累加器)
engine.load(2, 0)        # R2 = 0 (結果)
engine.load(3, 1)        # R3 = 1 (遞增常數)

# 計算 sum = 1 + 2 + ... + 10
for i in range(1, 11):
    engine.store[0] = i      # R0 = i
    engine.add(2, 0)         # R2 = R2 + R0
    engine.add(0, 3)         # R0 = R0 + 1 (準備下一個 i)

engine.print_register(2)  # 輸出結果：55
```

### 1.1.2 圖靈機的誕生

1936年，英國數學家艾倫·圖靈（Alan Turing）發表了划時代的論文《論可計算數及其在判定問題上的應用》（On Computable Numbers, with an Application to the Entscheidungsproblem）。這篇論文提出了**圖靈機**的概念，這是一個抽象的計算模型。

圖靈的想法源自一個簡單的問題：**人類數學家在進行計算時，大腦在做什麼？**

圖靈觀察到，數學家在計算時會在紙上寫下符號，並根據當前的心智狀態和看到的符號，決定下一步行動。這個過程是：

1. **寫下或擦除符號**
2. **移動注意力（紙上的位置）**
3. **進入新的心智狀態**

圖靈將這種過程抽象化，發明了著名的「圖靈機」。這個看似簡單的模型，後來被證明與任何現代電腦具有相同的計算能力——這就是著名的**邱奇-圖靈論題**（Church-Turing Thesis）。

## 1.2 計算理論的三大領域

計算理論通常分為三個相互關聯的領域：

```
┌─────────────────────────────────────────────────────────────┐
│                      計算理論                                │
├─────────────────┬─────────────────┬─────────────────────────┤
│   自動機理論     │   可計算性理論    │      複雜度理論          │
│  (Automata)    │  (Computability) │    (Complexity)         │
├─────────────────┼─────────────────┼─────────────────────────┤
│ 研究計算的數學模型│  研究什麼能計算    │  研究計算的效率          │
│ 正規語言         │  圖靈機          │  P vs NP               │
│ 上下文無關語言    │  停機問題        │  NP-完全性              │
│ 喬姆斯基層級      │  遞歸函數        │  密碼學                 │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### 1.2.1 自動機理論

自動機理論研究抽象計算機器的數學模型。這些模型有不同的「能力層級」：

| 模型 | 能力 | 對應語言類型 |
|------|------|-------------|
| 有限自動機 (DFA/NFA) | 有限記憶體 | 正規語言 |
| 下推自動機 (PDA) | 堆疊記憶體 | 上下文無關語言 |
| 圖靈機 | 無限記憶體 | 遞歸枚舉語言 |

### 1.2.2 可計算性理論

可計算性理論回答「什麼問題可以被機器解決」這個根本問題。

關鍵問題包括：
- **停機問題**：能否寫一個程式，判斷任意程式是否會停機？
- **拓撲學家判定問題**：看似簡單，實際上不可計算
- **打字機理論**：某些問題本質上比另一些問題更「難以計算」

### 1.2.3 複雜度理論

複雜度理論研究計算的效率，包括：

- **時間複雜度**：需要多少計算步驟？
- **空間複雜度**：需要多少記憶體？
- **P vs NP**：這個百萬美元問題至今未解

## 1.3 為什麼要學習計算理論？

也許你會問：這些抽象的理論與實際的軟體開發有何關聯？

答案是：**關聯極為深遠。**

### 1.3.1 理解語言的極限

如果你開發一個程式語言或正規表示式引擎，了解喬姆斯基層級能幫助你：

- 理解為什麼某些正規表示式無法匹配某些模式
- 知道何時需要更強大的語法分析器
- 避免設計出不完整或有缺陷的語言

### 1.3.2 評估問題的難度

當老闆說「這個NP問題很小，我們可以用暴力法解決」時，了解計算複雜度能讓你：

- 識別真正可解決的問題規模
- 選擇合適的近似演算法或啟發式方法
- 設計能在合理時間內運作的系統

### 1.3.3 欣賞電腦科學的美

計算理論是人類智力的偉大成就之一。從希爾伯特的夢想到哥德爾的震撼，從圖靈的直覺到邱奇的抽象，這段歷史充滿了戲劇性和深刻見解。

## 1.4 計算理論的簡史

```
時間線：計算理論的發展

1900  ──────────────────────────────────────────────────────
       │
       ▼
  希爾伯特提出23個數學問題
  (第10問題：判定問題)
       │
       │
       ▼
1928  ──────────────────────────────────────────────────────
       │
       ▼
  希爾伯特提出「判定問題」
  (Entscheidungsproblem)
       │
       │
       ▼
1931  ──────────────────────────────────────────────────────
       │
       ▼
  哥德爾不完備定理
  震撼整個數學界
       │
       │
       ▼
1936  ──────────────────────────────────────────────────────
       │
       ▼
  邱奇：λ演算
  圖靈：圖靈機
  兩種等价的計算模型
       │
       │
       ▼
1956  ──────────────────────────────────────────────────────
       │
       ▼
  喬姆斯基：語言層級
       │
       │
       ▼
1971  ──────────────────────────────────────────────────────
       │
       ▼
  Cook：NP-完全性
       │
       │
       ▼
2000  ──────────────────────────────────────────────────────
       │
       ▼
  P vs NP 問題
  成為千禧年難題
       │
       │
       ▼
Today ──────────────────────────────────────────────────────
```

## 1.5 本書的學習路徑

本書將帶你走過計算理論的完整旅程：

| 章節 | 主題 | 核心問題 |
|------|------|---------|
| 第2章 | 希爾伯特與判定問題 | 數學能否完全形式化？ |
| 第3章 | 哥德爾不完備定理 | 數學真理能否被證明？ |
| 第4章 | 丘奇λ演算 | 如何用函數表達一切計算？ |
| 第5章 | λ演算實作 | 用Python解譯函數式程式 |
| 第6章 | 圖靈機理論 | 什麼是計算的機械模型？ |
| 第7章 | 圖靈機模擬器 | 用程式模擬計算機器的行為 |
| 第8章 | 丘奇-圖靈論題 | 所有計算模型都一樣嗎？ |
| 第9章 | 喬姆斯基層級 | 語言有多少種複雜度？ |
| 第10章 | 自動機實作 | 用程式實作正規語言處理 |
| 第11章 | NP-完全理論 | 為什麼有些問題特別難？ |
| 第12章 | 現代發展 | 量子計算、複雜度突破 |

## 1.6 第一個計算模型：狀態機

在我們深入研究圖靈機之前，讓我們從一個簡單的計算模型開始——**有限狀態機**（Finite State Machine, FSM）。

狀態機是現實中最常見的計算模型：

- 交通燈：綠→黃→紅→綠（循環）
- 自動販賣機：等待投幣→選擇商品→出貨→找零
- 文字編輯器的開關：insert模式↔overwrite模式

[程式檔案：01-2-state-machine.py](../_code/01/01-2-state-machine.py)

```python
"""
狀態機的Python實作
以自動販賣機為例
"""

from enum import Enum
from typing import Callable, Dict, Optional

class State(Enum):
    IDLE = "idle"                    # 等待投幣
    COIN_INSERTED = "coin_inserted"  # 已投幣
    PRODUCT_SELECTED = "selected"    # 已選商品
    DISPENSING = "dispensing"        # 出貨中
    CHANGE_DUE = "change_due"        # 找零中
    ERROR = "error"                  # 錯誤

class Event(Enum):
    INSERT_COIN = "insert_coin"
    SELECT_PRODUCT = "select_product"
    CONFIRM = "confirm"
    DISPENSE_COMPLETE = "dispense_complete"
    CANCEL = "cancel"
    TIMEOUT = "timeout"

class VendingMachine:
    """
    自動販賣機狀態機
    
    狀態轉換圖：
    
    IDLE ──[投幣]──▶ COIN_INSERTED
    │                    │
    │ [取消]              │ [取消]
    ▼                    ▼
  IDLE ◀──[退幣]────── IDLE
                          │
                          │ [選商品]
                          ▼
                    PRODUCT_SELECTED
                          │
                          │ [確認]
                          ▼
                      DISPENSING ──[完成]──▶ IDLE (或 CHANGE_DUE)
    """
    
    def __init__(self):
        self.current_state = State.IDLE
        self.balance = 0
        self.price = 50  # 商品價格（分）
        self.transitions: Dict[tuple, Callable] = {
            # (當前狀態, 事件) -> (新狀態, 動作函數)
            (State.IDLE, Event.INSERT_COIN): 
                (State.COIN_INSERTED, self._handle_coin),
            (State.COIN_INSERTED, Event.SELECT_PRODUCT):
                (State.PRODUCT_SELECTED, self._handle_select),
            (State.COIN_INSERTED, Event.CANCEL):
                (State.IDLE, self._handle_cancel),
            (State.PRODUCT_SELECTED, Event.CONFIRM):
                (State.DISPENSING, self._handle_confirm),
            (State.PRODUCT_SELECTED, Event.CANCEL):
                (State.IDLE, self._handle_cancel),
            (State.DISPENSING, Event.DISPENSE_COMPLETE):
                (State.CHANGE_DUE, self._handle_dispense),
            (State.CHANGE_DUE, Event.TIMEOUT):
                (State.IDLE, self._handle_timeout),
        }
    
    def _handle_coin(self, coin: int):
        self.balance += coin
        print(f"投幣成功：${coin/100:.2f}，餘額：${self.balance/100:.2f}")
    
    def _handle_select(self):
        print(f"選擇商品，價格：${self.price/100:.2f}")
    
    def _handle_confirm(self):
        if self.balance >= self.price:
            print(f"扣款：${self.price/100:.2f}")
            self.balance -= self.price
        else:
            print(f"餘額不足！需要 ${self.price/100:.2f}")
            self.current_state = State.ERROR
    
    def _handle_dispense(self):
        print("商品出貨中...")
        print("商品掉落！")
    
    def _handle_cancel(self):
        if self.balance > 0:
            print(f"退還 ${self.balance/100:.2f}")
        self.balance = 0
    
    def _handle_timeout(self):
        if self.balance > 0:
            print(f"超時，自動退還 $${self.balance/100:.2f}")
        self.balance = 0
    
    def send_event(self, event: Event, data: Optional[int] = None) -> bool:
        """發送事件，觸發狀態轉換"""
        key = (self.current_state, event)
        
        if key in self.transitions:
            new_state, handler = self.transitions[key]
            if data is not None:
                handler(data)
            else:
                handler()
            self.current_state = new_state
            return True
        else:
            print(f"無效轉換：{self.current_state.value} + {event.value}")
            return False
    
    def get_state(self) -> State:
        return self.current_state


# 測試：完整的購買流程
def test_vending_machine():
    print("=== 自動販賣機測試 ===\n")
    
    vm = VendingMachine()
    
    print("步驟1: 投幣 $1")
    vm.send_event(Event.INSERT_COIN, 100)
    
    print("\n步驟2: 選擇商品")
    vm.send_event(Event.SELECT_PRODUCT)
    
    print("\n步驟3: 確認購買")
    vm.send_event(Event.CONFIRM)
    
    print("\n步驟4: 出貨完成")
    vm.send_event(Event.DISPENSE_COMPLETE)
    
    print(f"\n最終狀態: {vm.get_state().value}")
    print(f"餘額: ${vm.balance/100:.2f}")

test_vending_machine()
```

執行結果：

```
=== 自動販賣機測試 ===

步驟1: 投幣 $1
投幣成功：$1.00，餘額：$1.00

步驟2: 選擇商品
選擇商品，價格：$0.50

步驟3: 確認購買
扣款：$0.50

步驟4: 出貨完成
商品出貨中...
商品掉落！

最終狀態: change_due
餘額: $0.50
```

## 1.7 小結

本章我們：

1. **回顧了計算工具的歷史**：從巴貝奇的分析機到現代電腦
2. **介紹了計算理論的三大領域**：自動機理論、可計算性理論、複雜度理論
3. **理解了學習計算理論的價值**：無論是實際應用還是智力探索
4. **實作了第一個計算模型**：狀態機

在下一章，我們將回到1900年，探索大衛·希爾伯特的偉大夢想，以及這個夢想如何引發了一連串深刻的思想革命。

## 練習題

1. **狀態機設計**：設計一個簡單的文字編輯器狀態機，包含「普通模式」和「命令模式」，支援 i 鍵進入插入模式，Esc 鍵返回普通模式，:wq 保存退出。

2. **思考題**：自動販賣機的狀態機有哪些局限性？例如，如何處理庫存不足的情況？

3. **延伸閱讀**：查閱巴貝奇和分析機的歷史，思考為什麼這台機器在當時無法完成建造。
