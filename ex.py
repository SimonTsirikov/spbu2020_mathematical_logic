
from pyparsing import *
from parsec import parser
import ast

conj = '/\\'
disj = '\\/'
neg = '~'
exist = '!'
for_all = '+'
imp = '->'


def parser(p):
    if isinstance(p, str):
        if 'F' == p[0] or 'P' == p[0]:
            return p
        else:
            return ast.Term(p)

    elif len(p) >= 3:
        if p[1] == disj:
            return ast.Disj(parser(p[0: len(p) - 1]), parser([p[-1]]))
        else:
            for i in p[1]:
                parser(i)

    elif len(p) == 2:
        if 'F' in p[0]:
            return ast.Term(parser(p[0]), [parser(i) for i in p[1]])
        elif 'P' in p[0]:
            return ast.Atom(p[0], p[1])
        # elif p[0] == '!':
        #     return ast.Exists(parser(p[1]))
    else:
        return parser(p[0])


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


CONJ = Literal(conj)
DISJ = Literal(disj)
NEG = Literal(neg)
ALL = Literal(for_all)
IMP = Literal(imp)

# operation priority
operation = infixNotation(
    atom,
    [
        (NEG, 1, opAssoc.RIGHT),
        (IMP, 2, opAssoc.RIGHT),
        (CONJ, 2, opAssoc.LEFT),
        (DISJ, 2, opAssoc.LEFT)

    ],
)

expr = Forward()
expr <<= term | operation

l = expr.parseString(r'')

print(l)
# result = parser(l)
# print()
