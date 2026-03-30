;; LISP - 計算 1 到 10 的總和
(defun sum (n)
  (if (= n 0)
      0
      (+ n (sum (- n 1)))))

(print (sum 10))  ; 輸出 55
