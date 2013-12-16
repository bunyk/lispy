
; while loop
(define (while condition body) 
    (if (condition)
        (begin
            (body)
            (while condition body)
        )
        (list)
    )
)

; for loop
(define (for setup condition increment body)
    (begin
        (setup)
        (while condition
            (lambda () (begin
                (body)
                (increment)
            ))
        )
    )
)


; importing turtle functions
(define turtle (import (quote turtle)))
(define forward (getattr turtle (quote forward)))
(define right (getattr turtle (quote right)))


(define (pentagram size)
    (begin 
        (define i 0)
        (for
            (lambda () (set! i 0))
            (lambda () (< i 5))
            (lambda () (set! i (+ i 1)))
            (lambda () (begin
                (forward size)
                (right (- 180 36))
            ))
        )
    )
)

(pentagram 100)
(forward 100)
(pentagram 100)

(input)

; (while (lambda () (< i 4))
;     (lambda () (begin
;         (set! i (+ i 1)
;         (forward 100)
;         (right 90)
;     ))
; )

