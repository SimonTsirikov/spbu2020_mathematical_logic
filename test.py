from ast import *
from parsec import pparse
from solver import solve

# parsing test
assert pparse(r'P()\/P(a)\/P(F(a))\/P(F(a,b))') == Disjunction(Disjunction(Disjunction(Atom('P', []),
    Atom('P', [Term('a')])), Atom('P', [Term('F', [Term('a')])])), Atom('P', [Term('F', [Term('a'), Term('b')])]))

assert pparse(r'~P(a)') == Negation(Atom('P', [Term('a')]))
assert pparse(r'P(a)\/P1(b)') == Disjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')]))
assert pparse(r'P(a)/\P1(b)') == Conjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')]))
assert pparse(r'P(a)->P1(b)') == Implication(Atom('P', [Term('a')]), Atom('P1', [Term('b')]))

assert pparse(r'P(a)\/P1(b)\/P2(c)') == Disjunction(Disjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')])),
                                                    Atom('P2', [Term('c')]))
assert pparse(r'P(a)\/(P1(b)\/P2(c))') == Disjunction(Atom('P', [Term('a')]),
                                                      Disjunction(Atom('P1', [Term('b')]), Atom('P2', [Term('c')])))

assert pparse(r'P(a)/\P1(b)/\P2(c)') == Conjunction(Conjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')])),
                                                    Atom('P2', [Term('c')]))
assert pparse(r'P(a)/\(P1(b)/\P2(c))') == Conjunction(Atom('P', [Term('a')]),
                                                      Conjunction(Atom('P1', [Term('b')]), Atom('P2', [Term('c')])))

assert pparse(r'P(a)\/P1(b)/\P2(c)') == Disjunction(Atom('P', [Term('a')]),
                                                    Conjunction(Atom('P1', [Term('b')]), Atom('P2', [Term('c')])))
assert pparse(r'P(a)\/P1(b)->P2(c)') == Disjunction(Atom('P', [Term('a')]),
                                                    Implication(Atom('P1', [Term('b')]), Atom('P2', [Term('c')])))
assert pparse(r'P(a)/\P1(b)->P2(c)') == Conjunction(Atom('P', [Term('a')]),
                                                    Implication(Atom('P1', [Term('b')]), Atom('P2', [Term('c')])))

assert pparse(r'P(a)/\P1(b)\/P2(c)') == Disjunction(Conjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')])),
                                                    Atom('P2', [Term('c')]))
assert pparse(r'P(a)->P1(b)\/P2(c)') == Disjunction(Implication(Atom('P', [Term('a')]), Atom('P1', [Term('b')])),
                                                    Atom('P2', [Term('c')]))
assert pparse(r'P(a)->P1(b)/\P2(c)') == Conjunction(Implication(Atom('P', [Term('a')]), Atom('P1', [Term('b')])),
                                                    Atom('P2', [Term('c')]))

assert pparse(r'P(a)->P1(b)->P2(c)') == Implication(Atom('P', [Term('a')]),
                                                    Implication(Atom('P1', [Term('b')]), Atom('P2', [Term('c')])))
assert pparse(r'(P(a)->P1(b))->P2(c)') == Implication(Implication(Atom('P', [Term('a')]), Atom('P1', [Term('b')])),
                                                      Atom('P2', [Term('c')]))

assert pparse(r'~~P(a)') == Negation(Negation(Atom('P', [Term('a')])))
assert pparse(r'~P(a)\/P1(b)') == Disjunction(Negation(Atom('P', [Term('a')])), Atom('P1', [Term('b')]))
assert pparse(r'P(a)/\~P1(b)') == Conjunction(Atom('P', [Term('a')]), Negation(Atom('P1', [Term('b')])))
assert pparse(r'~(P(a)\/P1(b))') == Negation(Disjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')])))

assert pparse(r'a ! P(a)') == Exists(Term('a'), Atom('P', [Term('a')]))
assert pparse(r'a + P(a)') == Forall(Term('a'), Atom('P', [Term('a')]))

assert pparse(r'~(a ! P(a))') == Negation(Exists(Term('a'), Atom('P', [Term('a')])))
assert pparse(r'~(a + P(a))') == Negation(Forall(Term('a'), Atom('P', [Term('a')])))

assert pparse(r'a ! P(a) \/ P1(b)') == Disjunction(Exists(Term('a'), Atom('P', [Term('a')])), Atom('P1', [Term('b')]))
assert pparse(r'a ! (P(a) \/ P1(b))') == Exists(Term('a'), Disjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')])))

assert pparse(r'a ! P(a) /\ P1(b)') == Conjunction(Exists(Term('a'), Atom('P', [Term('a')])), Atom('P1', [Term('b')]))
assert pparse(r'a ! (P(a) /\ P1(b))') == Exists(Term('a'), Conjunction(Atom('P', [Term('a')]), Atom('P1', [Term('b')])))

assert pparse(r'a ! P(a) -> P1(b)') == Implication(Exists(Term('a'), Atom('P', [Term('a')])), Atom('P1', [Term('b')]))
assert pparse(r'a ! (P(a) -> P1(b))') == Exists(Term('a'), Implication(Atom('P', [Term('a')]), Atom('P1', [Term('b')])))

assert pparse(r'a ! ~P(a) \/ P1(b)') == Disjunction(Exists(Term('a'), Negation(Atom('P', [Term('a')]))),
                                                    Atom('P1', [Term('b')]))
assert pparse(r'a ! (~P(a) \/ P1(b))') == Exists(Term('a'),
                                                 Disjunction(Negation(Atom('P', [Term('a')])), Atom('P1', [Term('b')])))

# logic tests

assert solve(r'a + (P(a)\/~P(a))')
assert solve(r'a ! (P(a)\/~P(b))')
assert not solve(r'a + (P(a)\/~P(b))')
assert solve(r'a + (P(a)->P(a))')
assert solve(r'a ! (P(a)->P(b))')
assert solve(r'a ! b ! (P(a)\/~P(b))')
assert solve(r'a ! b ! (P(a)/\P(b)\/~P(c))')
