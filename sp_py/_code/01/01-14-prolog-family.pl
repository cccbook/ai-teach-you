% Prolog - 家族關係範例
father(tom, bob).
father(tom, alice).
mother(mary, bob).

parent(X, Y) :- father(X, Y).
parent(X, Y) :- mother(X, Y).

% 查詢：誰是 Bob 的父母？
% ?- parent(Who, bob).
% Who = tom ;
% Who = mary
