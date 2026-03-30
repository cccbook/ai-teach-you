-- Lua 範例
function fib(n)
    if n <= 1 then return n end
    return fib(n - 1) + fib(n - 2)
end

print(fib(10))  -- 輸出 55
