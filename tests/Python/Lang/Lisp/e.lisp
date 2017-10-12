(def sumsome (x) (add x a))
(setq a `(add x 1))
(def wx (x) (sumsome x))
( print (wx 5) )

(def desc (seq) (setq [head, *tail] = seq))
