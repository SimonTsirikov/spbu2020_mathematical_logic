from lexer import lexer
from parsec import parser
import ast



# all(a, resovle(...) and all(b, resolve(...)) -> true, else -> false)
def resolve(a, b):

    if contraversial(a, b):
        return True

    if all(map(lambda x: isinstance(x, ast.Var), a)) and all(map(lambda x: isinstance(x, ast.Var), b)):
        print(f'{a} |- {b}')
        return False

    for i in a:
        if not isinstance(i, ast.Var):
            # foreach l, r in i.introduce: a' = copy(a) ...
            for l, r in i.introduce():
                a_next = a.copy()
                a_next.remove(i)
                a_next.extend(l)
                b_next = b.copy()
                b_next.extend(r)
                if not resolve(a_next, b_next):
                    print(f'{a} |- {b}')
                    return False
    
    for i in b:
        if not isinstance(i, ast.Var):
            for l, r in i.eliminate():
                a_next = a.copy()
                a_next.extend(l)
                b_next = b.copy()
                b_next.remove(i)
                b_next.extend(r)

                if not resolve(a_next, b_next):
                    print(f'{a} |- {b}')
                    return False
    
    return True

def contraversial(a, b):
    for i in a:
        if i in b:
            return True
    return False

str = 'a -> a'
a = parser.parse(lexer.lex(str))
if resolve([], [a]):
    print('General.')