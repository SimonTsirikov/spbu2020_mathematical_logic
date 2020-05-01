from solver import resolve
from ast import *

assert resolve([], [Forall(Term('a'), Disjunction(Atom('P', [Term('a')]), Negation(Atom('P', [Term('a')]))))], False)
assert not resolve([], [Forall(Term('a'), Disjunction(Atom('P', [Term('a')]), Negation(Atom('P', [Term('b')]))))], False)
# assert solve('~(+a a)')
# assert solve(r'!a (a/\~a)')
# assert solve(r'~(!a (a/\~a))')
# assert solve('!a (+b (a->b))')
# assert solve('+a (!b (a->b))')
# assert solve(r'+a (a\/~a)')
# assert solve('+a (a->a)')
# assert solve(r'(+a (+b ((a -> b) \/ (b -> a))))')
