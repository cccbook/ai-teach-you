# Haskell

## 概述

Haskell 是一種純函數式程式語言，於 1990 年發布命名，以數學家 Haskell Curry 命名。Haskell 採用惰性求值（Lazy Evaluation），支援自動類型推斷和強大的類別系統，是學習函數式編程理念的最佳語言。

## 歷史

- **1987 年**：函數式語言標準會議召開
- **1990 年**：Haskell 1.0 發布
- **1999 年**：Haskell 98 標準
- **2010 年**：Haskell 2010 標準
- **2014 年**：GHC 7.8 引進 Haskell 平台
- **現在**：Haskell 2010 仍為主要標準

## 核心特性

### 1. 函數式編程

```haskell
-- 基本函數
square :: Int -> Int
square x = x * x

-- 區域綁定
hypotenuse :: Double -> Double -> Double
hypotenuse a b =
    let c2 = a^2 + b^2
    in sqrt c2

-- 列表操作
sum' :: [Int] -> Int
sum' [] = 0
sum' (x:xs) = x + sum' xs

-- 列表推導
squares :: [Int] -> [Int]
squares xs = [x^2 | x <- xs]

evens :: [Int] -> [Int]
evens xs = [x | x <- xs, even x]
```

### 2. 惰性求值

```haskell
-- 無限列表
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- 取前 n 個元素
take 10 fibs
-- [0,1,1,2,3,5,8,13,21,34]

--  primes（無限質數列表）
primes :: [Integer]
primes = sieve [2..]
  where
    sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
```

### 3. 高階函數

```haskell
-- map, filter, fold
main :: IO ()
main = do
    let numbers = [1..10]
    print $ map square numbers
    print $ filter even numbers
    print $ foldr (+) 0 numbers
    
    -- composition
    print $ (map square . filter even) [1..10]
    
    -- partial application
    let add10 = (+ 10)
    print $ map add10 [1..5]
```

### 4. 類別（Typeclass）

```haskell
-- 定義類別
class Eq a where
    (==) :: a -> a -> Bool
    (/=) :: a -> Bool -> Bool
    
-- 實作類別
data Color = Red | Green | Blue

instance Eq Color where
    Red == Red = True
    Green == Green = True
    Blue == Blue = True
    _ == _ = False
```

### 5. IO 操作

```haskell
-- IO 動作
main :: IO ()
main = do
    putStrLn "What's your name?"
    name <- getLine
    putStrLn $ "Hello, " ++ name
    
    -- 讀取檔案
    content <- readFile "test.txt"
    putStrLn content
    
    -- 寫入檔案
    writeFile "output.txt" "Hello, World!"
```

### 6. Monads

```haskell
-- Maybe Monad
safeDivide :: Integral a => a -> a -> Maybe a
safeDivide _ 0 = Nothing
safeDivide a b = Just (a `div` b)

-- 使用 do notation
example :: Maybe Int
example = do
    a <- safeDivide 10 2
    b <- safeDivide a 2
    return b

-- Either Monad
divide :: Integral a => a -> a -> Either String a
divide _ 0 = Left "Division by zero"
divide a b = Right (a `div` b)
```

## 常見函式庫

```haskell
-- 資料結構
import Data.Map
import Data.Set
import Data.Sequence

-- 文字處理
import Data.Text

-- 並發
import Control.Concurrent
import Control.Monad.Par
```

## 為什麼學習 Haskell？

1. **函數式思維**：提升解決問題的能力
2. **類型系統**：強大的類型推斷
3. **惰性求值**：優雅的無限資料處理
4. **數學基礎**：理解計算理論
5. **學習曲線**：挑戰傳統編程思維

## 參考資源

- "Learn You a Haskell for Great Good!"
- "Real World Haskell"
- "Programming in Haskell"
- haskell.org
