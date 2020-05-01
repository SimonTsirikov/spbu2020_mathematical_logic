from solver import resolve
from ast import *

assert resolve([], [Forall(Term('a'), Disjunction(Atom('P', [Term('a')]), Negation(Atom('P', [Term('a')]))))], False)
assert not resolve([], [Forall(Term('a'), Disjunction(Atom('P', [Term('a')]), Negation(Atom('P', [Term('b')]))))], False)
