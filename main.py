from lexer import lexer
from parsec import parser
import ast


def pprint(a, b):
    print(f"{', '.join(map(lambda x: x.show(), a))} |- {', '.join(map(lambda x: x.show(), b))}")


def find_by_mask(source):
    if not (isinstance(source, ast.Forall) or isinstance(source, ast.Exists) or isinstance(source, ast.Substitute)):    
        yield source
        if issubclass(type(source), ast.UnaryOp):
            for i in find_by_mask(source.argument):
                if i is not None:
                    yield i
        elif issubclass(type(source), ast.BinaryOp):
            for i in find_by_mask(source.left):
                if i is not None:
                    yield i
            for i in find_by_mask(source.right):
                if i is not None:
                    yield i
    yield None


def contains(box, item):
    if isinstance(box, ast.Var):
        return box == item
    elif issubclass(type(box), ast.UnaryOp):
        return contains(box.argument, item)
    elif isinstance(box, ast.Substitute):
        if box.left != item:
            return contains(box.right, item)
        else:
            box.collise()
            return contains(box.right, item)
    elif isinstance(box, ast.Forall) or isinstance(box, ast.Exists):
        return True
    elif issubclass(type(box), ast.BinaryOp):
        return contains(box.left, item) or contains(box.right, item)


def next_similiar(mask, array):
    for i in array:
        for var_new in find_by_mask(i):
            if var_new is not None and not contains(var_new, mask.right):
                result = ast.substitute(mask.left, var_new, mask.right)
                yield result
    end_phase = mask.copy()
    end_phase.collise()
    yield end_phase.right


def has_next(x):
    return isinstance(x, ast.Var)


def prepare_and_resolve(a, b, reversed, exists_mode, item):
    i, l, r = item

    a_next = a.copy()
    b_next = b.copy()
    
    if reversed:
        b_next.remove(i)
    else:
        a_next.remove(i)

    a_next.extend(l)
    b_next.extend(r)

    return resolve(a_next, b_next, exists_mode)
 

def resolve(a, b, exists_mode):

    if contraversial(a, b, exists_mode):
        return True

    for i in a:
        if isinstance(i, ast.Substitute):
            a_copy = a.copy()
            a_copy.remove(i)
            b_ext = b.copy()
            b_ext.extend(list(map(lambda x: x.argument if isinstance(x, ast.Negation) else ast.Negation(x), a_copy)))

            for j in next_similiar(i, b_ext):
                a_next = a.copy()
                a_next.remove(i)
                a_next.append(j)
                b_next = b.copy()
                
                cont = resolve(a_next, b_next, False)

                if not exists_mode and not cont:
                    pprint(a, b)
                    return False
                elif exists_mode and cont:
                    return True
            return True

        elif not isinstance(i, ast.Var):
            if isinstance(i, ast.Exists):
                exists_mode = True

            check = lambda x : prepare_and_resolve(a, b, False, exists_mode, x)
            
            cont = all(map(check, i.introduce()))
            
            if not exists_mode and not cont:
                pprint(a, b)
                return False
            elif exists_mode and cont:
                return True
            
    
    for i in b:
        if isinstance(i, ast.Substitute):
            b_copy = b.copy()
            b_copy.remove(i)
            a_ext = a.copy()
            a_ext.extend(list(map(lambda x: x.argument if isinstance(x, ast.Negation) else ast.Negation(x), b_copy)))

            for j in next_similiar(i, a_ext):
                a_next = a.copy()
                b_next = b.copy()
                b_next.remove(i)
                b_next.append(j)
                
                if resolve(a_next, b_next, True):
                    return True
            
            pprint(a, b)
            return False

        elif not isinstance(i, ast.Var):
            if isinstance(i, ast.Forall):
                exists_mode = False
            
            check = lambda x : prepare_and_resolve(a, b, True, exists_mode, x)
            
            cont = all(map(check, i.eliminate()))

            if not exists_mode and not cont:
                pprint(a, b)
                return False
            elif exists_mode and cont:
                return True
               
    if exists_mode or (all(map(has_next, a + b)) and not contraversial(a, b, exists_mode)):
        pprint(a, b)
        return False
    else:
        return True


def contraversial(a, b, exists_mode):
    duplicate = lambda x : x in a
    return any(map(duplicate, b))

example = ''
a = parser.parse(lexer.lex(example))

if resolve([], [a], False):
    print('General.')
else:
    print('Not general.')
