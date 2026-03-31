# Prolog

## 概述

Prolog（Programming in Logic）是一種邏輯程式語言，由 Alain Colmerauer 於 1972 年在法國馬賽大學發明。Prolog 基於一階邏輯，透過事實和規則描述問題，自動進行邏輯推導。常用於人工智慧、專家系統、自然語言處理等領域。

## 歷史

- **1972 年**：Alain Colmerauer 發明 Prolog
- **1977 年**：David Warren 發明 Warren Abstract Machine
- **1986 年**：ISO 標準化 Prolog
- **1995 年**：Prolog 標準修訂
- **現在**：主要實現有 SWI-Prolog、Gnu Prolog

## 核心特性

### 1. 事實與規則

```prolog
% 事實
likes(john, mary).
likes(mary, john).
likes(john, pizza).

% 規則
friend(X, Y) :- likes(X, Y), likes(Y, X).
friend(X, Y) :- likes(X, Z), likes(Z, Y), X \= Y.

% 查詢
?- friend(john, mary).
false.

?- friend(mary, john).
true.
```

### 2. 遞迴

```prolog
% 列表長度
length([], 0).
length([_|T], N) :- length(T, N1), N is N1 + 1.

% 會員關係
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

%  append
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

% 反向列表
reverse([], []).
reverse([H|T], R) :- reverse(T, RT), append(RT, [H], R).
```

### 3. 結構

```prolog
% 結構定義
person(name, age, occupation).
date(day, month, year).

% 使用結構
?- person(john, 30, engineer).
true.

% 查詢結構欄位
?- person(Name, 30, _).
Name = john.
```

### 4. 數學運算

```prolog
% 費波那契數列
fib(0, 0).
fib(1, 1).
fib(N, F) :- 
    N > 1, 
    N1 is N - 1, 
    N2 is N - 2,
    fib(N1, F1), 
    fib(N2, F2), 
    F is F1 + F2.

% 階乘
factorial(0, 1).
factorial(N, F) :- 
    N > 0, 
    N1 is N - 1, 
    factorial(N1, F1), 
    F is N * F1.
```

### 5. 剪枝（Cut）

```prolog
% max 三個數
max(A, B, C, M) :- 
    A >= B, A >= C, M = A, !.
max(A, B, C, M) :- 
    B >= C, M = B, !.
max(_, _, C, C).

% if-then-else
max2(A, B, M) :- 
    A > B -> M = A; M = B.
```

### 6. 專家系統範例

```prolog
% 疾病專家系統
disease(flu) :- 
    symptom(fever),
    symptom(cough),
    symptom(fatigue).

disease(cold) :- 
    symptom(sneezing),
    symptom(runny_nose).

symptom(fever).
symptom(cough).

?- disease(flu).
true.
```

## 執行範例（SWI-Prolog）

```prolog
% 啟動
swipl

% 載入檔案
?- [myfile].

% 查詢
?- likes(john, Who).

% 列出所有解答
?- likes(john, Who), write(Who), nl, fail.
```

## 為什麼學習 Prolog？

1. **邏輯編程**：不同於程序式思維
2. **自動回溯**：自動搜尋解答
3. **符號處理**：擅長符號和關係運算
4. **AI 應用**：專家系統、自然語言處理
5. **理解計算**：了解邏輯與推導

## 參考資源

- "Programming in Prolog"
- "The Art of Prolog"
- "Learn Prolog Now"
- swi-prolog.org
