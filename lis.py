################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010; See http://norvig.com/lispy.html
## (c) Bunyk Taras, 2013; See http://norvig.com/lispy.html

from __future__ import division
from __future__ import print_function

from pprint import pprint

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."

    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer:
            return self.outer.find(var)
        else:
            raise NameError('name %r is not defined' % var)

    def print(self):
        if self.outer:
            self.outer.print()
        pprint(self)


def add_globals(env):
    "Add some Scheme standard procedures to an environment."
    import operator as op
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.div,
        'not': op.not_,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq, 
        'equal?': op.eq,
        'eq?': op.is_,
        'length': len,
        'cons': lambda x, y: [x] + y,
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'append': op.add,  
        'list': lambda *x: list(x),
        'list?': lambda x: isa(x, list), 
        'null?': lambda x: x == [],
        'symbol?': lambda x: isa(x, str),

        'print': print,
        'import': __import__,
        'getattr': getattr,
        'input': raw_input,
    })
    return env

global_env = add_globals(Env())

isa = isinstance

def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    try:
        if isa(x, str):             # variable reference
            return env.find(x)[x]
        elif not isa(x, list):         # constant literal
            return x                
        elif x[0] == 'quote':          # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] == 'if':             # (if test conseq alt)
            (_, test, conseq, alt) = x
            return eval((conseq if eval(test, env) else alt), env)
        elif x[0] == 'set!':           # (set! var exp)
            try:
                (_, var, exp) = x
            except ValueError:
                raise TypeError('set! expects two arguments')
            env.find(var)[var] = eval(exp, env)
        elif x[0] == 'define':         # (define var exp)
            (_, var, exp) = x
            if isa(var, str):
                env[var] = eval(exp, env)
            elif isa(var, list):
                env[var[0]] = eval(['lambda', var[1:], exp])
            else:
                RuntimeError('Cannot assign to constant!')
        elif x[0] == 'lambda':         # (lambda (var*) exp)
            (_, vars, exp) = x
            return lambda *args: eval(exp, Env(vars, args, env))
        elif x[0] == 'begin':          # (begin exp*)
            for exp in x[1:]:
                val = eval(exp, env)
            return val
        else:                          # (proc exp*)
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            return proc(*exps)
    except Exception as e:
        env.print()
        print('Caught exception while evaluating')
        print(to_string(x))
        print(e)
        raise


def parse(s):
    "Read a Scheme expression from a string."
    res = read_from(tokenize(s))
    return res


def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)

def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return '('+' '.join(map(to_string, exp))+')' if isa(exp, list) else str(exp)

def evaluate(s):
    return eval(parse('(begin ' + s + ')'))

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None: print(to_string(val))

def main(argv):
    if len(argv) > 1:
        with open(argv[1]) as f:
            lines = filter(lambda l: not l.startswith(';'), f.readlines())
            evaluate('\n'.join(lines))
    else:
        repl(argv[0])

if __name__ == '__main__':
    import sys
    main(sys.argv)
