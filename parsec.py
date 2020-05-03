import sys

from pyparsing import *
import ast


def pparse(string):
    return parse(expr.parseString(string))


conj = '/\\'
disj = '\\/'
neg = '~'
exist = '!'
for_all = '+'
imp = '->'


def parse(p):
    if isinstance(p, str):
        if 'F' == p[0] or 'P' == p[0]:
            return p
        else:
            return ast.Term(p)

    elif issubclass(type(p), ast.BaseBox):
        return p

    elif len(p) >= 3:
        if p[1] == for_all:
            return parse([ast.Forall(parse(p[0]), parse(p[2]))] + p[3:])
        elif p[1] == exist:
            return parse([ast.Exists(parse(p[0]), parse(p[2]))] + p[3:])
        elif p[-2] == imp:
            return parse(p[:-4] + [ast.Implication(parse(p[-3]), parse(p[-1]))])
        elif p[1] == conj:
            return parse([ast.Conjunction(parse(p[0]), parse(p[2]))] + p[3:])
        elif p[1] == disj:
            return parse([ast.Disjunction(parse(p[0]), parse(p[2]))] + p[3:])
        else:
            raise SyntaxError

    elif len(p) == 2:
        if 'F' in p[0]:
            return ast.Term(parse(p[0]), [parse(i) for i in p[1] if i != ''])
        elif 'P' in p[0]:
            return ast.Atom(p[0], [parse(i) for i in p[1] if i != ''])
        elif p[0] == neg:
            return ast.Negation(parse(p[1]))
        else:
            raise SyntaxError

    elif len(p) == 1:
        return parse(p[0])

    else:
        raise SyntaxError


ParserElement.enablePackrat()
sys.setrecursionlimit(3000)

# Parenthesis, dont show in result (function of suppress)
open_par = Literal("(").suppress()
close_par = Literal(")").suppress()

term_name = Word('F', srange('[0-9]'), max=100)
term = Forward()
term <<= Group(term_name + Group(open_par + Optional(delimitedList(term | "''" | Word(alphanums + '_')), ''
                                                     ) + close_par))

atom_name = Word('P', srange('[0-9]'), max=100)
atom = Forward()
atom <<= Group(atom_name + Group(open_par + Optional(delimitedList(atom | "''" | term | Word(alphanums + '_')), ''
                                                     ) + close_par))

ALL = Literal(for_all)
EXS = Literal(exist)
NEG = Literal(neg)
IMP = Literal(imp)
CONJ = Literal(conj)
DISJ = Literal(disj)

legal_expr = atom | Word(alphanums + '_')

# operation priority
operation = infixNotation(
    legal_expr,
    [
        (NEG, 1, opAssoc.RIGHT),
        (ALL, 2, opAssoc.RIGHT),
        (EXS, 2, opAssoc.RIGHT),
        (IMP, 2, opAssoc.RIGHT),
        (CONJ, 2, opAssoc.LEFT),
        (DISJ, 2, opAssoc.LEFT)

    ],
)

expr = Forward()
expr <<= term | operation | Group(for_all + Word(alphanums + '_') + expr) | Group(exist + Word(alphanums + '_') + expr)
