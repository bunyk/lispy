import unittest

from lis import global_env, Env, evaluate, parse

class TestEvaluations(unittest.TestCase):
    def evals(self, exp, val):
        self.assertEquals(evaluate(exp), val)

    def test_first_order_operators(self):
        self.evals('''
            (define (abs a)
                ((if (> a 0) + -) 0 a)
            )
            (list
                (abs 1)
                (abs -1)
            )
        ''', [1, 1])

    def test_define_function(self):
        self.evals('''
            (define (square x)
                (* x x)
            )
            (square 2)
        ''', 4
        )

    def test_recursion(self):
        self.evals('''
            (define (f x) 
                (if (> x 1)
                    (* x (f (- x 1)))
                    1
                )
            )
            (f 6)
        ''', 720
        )

    def test_import(self):
        import math
        self.evals('''
            (define math (import (quote math)))
            (define sin (getattr math (quote sin)))
            sin
        ''', math.sin
        )

if __name__ == '__main__':
    unittest.main()

