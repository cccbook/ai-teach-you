-- Haskell - 使用遞迴與模式匹配
sum' :: [Int] -> Int
sum' [] = 0
sum' (x:xs) = x + sum' xs

main = print (sum' [1..10])  -- 輸出 55
