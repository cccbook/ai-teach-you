# LISP

## 概述

LISP（LISt Processor）是一種歷史悠久的函數式程式語言，由 John McCarthy 於 1958 年在麻省理工學院（MIT）發明。它是僅次於 Fortran 的第二古老高階語言，至今仍在人工智慧領域广泛使用。

## 歷史

- **1958 年**：John McCarthy 在 MIT 發明 LISP
- **1960 年**：發表經典論文 "Recursive Functions of Symbolic Expressions and Their Computation by Machine"
- **1984 年**：Common Lisp 標準化
- **1990 年**：Scheme 語言誕生
- **2001 年**：Clojure 基於 JVM 的現代 LISP 方言

## 核心特性

### 1. S-表達式（S-Expressions）

LISP 使用「S-表達式」作為基本語法結構，所有程式碼和資料都是列表：

```lisp
; 這是一個列表
'(1 2 3)

; 這也是一個列表（函數調用）
(+ 1 2)

; 巢狀列表
'(+ (* 2 3) (/ 10 2))
```

### 2. 函數為一等公民

函數可以作為參數傳遞、回傳值、存入變數：

```lisp
; 定義函數
(defun square (x)
  (* x x))

; 將函數作為參數傳遞
(mapcar #'square '(1 2 3 4 5))
; => (1 4 9 16 25)

; lambda 匿名函數
(mapcar #'(lambda (x) (* x x)) '(1 2 3 4 5))
```

### 3. 遞迴思維

LISP 天然支持遞迴，適合處理樹狀結構：

```lisp
; 計算列表長度
(defun my-length (lst)
  (if (null lst)
      0
      (+ 1 (my-length (cdr lst)))))

; 計算列表總和
(defun sum (lst)
  (if (null lst)
      0
      (+ (car lst) (sum (cdr lst)))))

; 菲波那契數列
(defun fib (n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (t (+ (fib (- n 1)) (fib (- n 2))))))
```

### 4. 垃圾回收

現代 LISP 實現都內建垃圾回收，自動管理記憶體。

### 5. 程式即資料

LISP 的「程式即資料」特性讓你可以輕鬆操作和生成程式碼（巨集）：

```lisp
; 定義一個巨集
(defmacro when (condition &body body)
  `(if ,condition (progn ,@body)))

; 使用巨集
(when (> x 0)
  (print "x is positive")
  (setf result (* x x)))
```

## 常見方言

### Common Lisp

最完整的 LISP 標準，配有豐富的標準庫：

```lisp
; Hello World
(print "Hello, World!")

; 定義變數
(defvar *name* "World")
(format t "Hello, ~A!~%" *name*)

; 結構體
(defstruct person
  name
  age
  (address nil))

; 物件導向
(defmethod greet ((p person))
  (format t "Hello, ~A!~%" (person-name p)))
```

### Scheme

簡潔優雅的 LISP 方言，重視語言設計的優美性：

```scheme
; Hello World
(display "Hello, World!")
(newline)

; 高階函數
(define (map proc lst)
  (if (null? lst)
      '()
      (cons (proc (car lst))
            (map proc (cdr lst)))))

; 閉包
(define make-counter
  (lambda ()
    (let ((count 0))
      (lambda ()
        (set! count (+ count 1))
        count))))
```

### Clojure

運行於 JVM 的現代 LISP，方便與 Java 生態系統整合：

```clojure
; Hello World
(println "Hello, World!")

; 持久化資料結構
(def nums [1 2 3 4 5])
; => [1 2 3 4 5]

; 並發支援
(def future (future (do-something)))
; @future ; 獲取結果
```

## 經典範例：簡易 LISP 直譯器

```lisp
;; 簡易 LISP 直譯器
(defun eval-expr (expr env)
  (cond
    ; 數字直接返回
    (numberp expr expr)
    
    ; 符號查詢環境
    (symbolp (cdr (assoc expr env :test #'eq)))
    
    ; 列表：函數調用
    (t (let ((fn (eval-expr (car expr) env))
             (args (mapcar #'(lambda (e) (eval-expr e env))
                          (cdr expr))))
        (apply fn args)))))

;; 測試
(eval-expr '(+ 1 2) nil)        ; => 3
(eval-expr '(* 3 4) nil)         ; => 12
(eval-expr '(+ (* 2 3) 4) nil)   ; => 10
```

## 應用領域

1. **人工智慧**：早期 AI 研究的主要語言
2. **符號計算**：數學公式處理、 Computer Algebra System
3. **劇本編寫**：Emacs Lisp 用於擴展編輯器
4. **金融**：KDB+、Lisp 衍生語言用於高頻交易
5. **遊戲開發**：Gameblink 等遊戲引擎使用 LISP

## 為什麼學習 LISP？

1. **理解計算本質**：S-表達式揭示了程式語言的抽象本质
2. **提升程式思維**：函數式編程思維有助於解決複雜問題
3. **巨集能力**：強大的程式生成能力
4. **歷史價值**：理解程式語言設計的演化歷程

## 參考資源

- "Structure and Interpretation of Computer Programs" (SICP)
- "Common Lisp" by Guy L. Steele
- "Practical Common Lisp" by Peter Seibel
- ANSI X3J13 Common Lisp 標準
