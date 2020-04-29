from lexer import lexer
from parsec import parser
import ast


def solve(string):
    expr = parser.parse(lexer.lex(string))
    if resolve([], [expr], False):
        print('General')
        return True
    else:
        print('Not general')
        return False


def resolve(antecedent, succedent, exists_mode):
    if contraversial(antecedent, succedent, exists_mode):
        return True

    lcont, exists_mode_1 = check_side(antecedent, succedent, False, exists_mode)
    if lcont is not None:
        return lcont

    rcont, exists_mode_2 = check_side(antecedent, succedent, True, exists_mode_1)
    if rcont is not None:
        return rcont

    if exists_mode_2 or all(map(has_next, antecedent + succedent)):
        return False
    else:
        return True


def check_side(antecedent, succedent, reversed, exists_mode):
    iterable = succedent if reversed else antecedent
    for i in iterable:
        if isinstance(i, ast.Substitute):

            copy = succedent.copy() if reversed else antecedent.copy()
            extended = antecedent.copy() if reversed else succedent.copy()

            copy.remove(i)
            extended.extend(list(map(transist, copy)))

            for j in enumerate_available_substitutions(i, extended):

                antecedent_next = antecedent.copy()
                succedent_next = succedent.copy()

                if reversed:
                    succedent_next.remove(i)
                    succedent_next.append(j)
                else:
                    antecedent_next.remove(i)
                    antecedent_next.append(j)

                cont = resolve(antecedent_next, succedent_next, reversed)

                if reversed:
                    if cont:
                        return True, exists_mode
                elif not exists_mode and not cont:
                    return False, exists_mode
                elif exists_mode and cont:
                    return True, exists_mode

            return not reversed, exists_mode

        elif not isinstance(i, ast.Var):
            if not reversed and isinstance(i, ast.Exists):
                exists_mode = True
            elif reversed and isinstance(i, ast.Forall):
                exists_mode = False

            def check(x): return prepare_and_resolve(
                antecedent, succedent, reversed, exists_mode, x)
            func = i.eliminate() if reversed else i.introduce()
            cont = all(map(check, func))

            if not exists_mode and not cont:
                return False, exists_mode
            elif exists_mode and cont:
                return True, exists_mode
    return None, exists_mode


def prepare_and_resolve(antecedent, succedent, reversed, exists_mode, item):
    i, l, r = item

    antecedent_next = antecedent.copy()
    succedent_next = succedent.copy()

    if reversed:
        succedent_next.remove(i)
    else:
        antecedent_next.remove(i)

    antecedent_next.extend(l)
    succedent_next.extend(r)

    return resolve(antecedent_next, succedent_next, exists_mode)


def enumerate_available_substitutions(mask, array):
    for i in array:
        for var_new in traverse_expression_tree(i):
            if var_new is not None and not contains(var_new, mask.right):
                result = ast.substitute(mask.left, var_new, mask.right)
                yield result
    end_phase = mask.copy()
    end_phase.collision()
    yield end_phase.right


def traverse_expression_tree(source):
    if not aware_recursion(source):
        if not check_recursion(source):
            if not isinstance(source, ast.Neg):
                yield ast.Neg(source)
            yield source

        if issubclass(type(source), ast.UnaryOp):
            for i in traverse_expression_tree(source.argument):
                if i is not None:
                    yield i
        elif issubclass(type(source), ast.BinaryOp):
            for i in traverse_expression_tree(source.left):
                if i is not None:
                    yield i
            for i in traverse_expression_tree(source.right):
                if i is not None:
                    yield i
    yield None


def aware_recursion(expr):
    return isinstance(expr, ast.Forall) or isinstance(expr, ast.Exists) or isinstance(expr, ast.Substitute)


def check_recursion(expr):
    if issubclass(type(expr), ast.UnaryOp):
        return check_recursion(expr.argument)
    elif issubclass(type(expr), ast.BinaryOp):
        return aware_recursion(expr) and check_recursion(expr.left) and check_recursion(expr.right)
    else:
        return False


def contains(box, item):
    if isinstance(box, ast.Var):
        return box == item
    elif issubclass(type(box), ast.UnaryOp):
        return contains(box.argument, item)
    elif isinstance(box, ast.Substitute):
        if box.left != item:
            return contains(box.right, item)
        else:
            box.collision()
            return contains(box.right, item)
    elif isinstance(box, ast.Forall) or isinstance(box, ast.Exists):
        return True
    elif issubclass(type(box), ast.BinaryOp):
        return contains(box.left, item) or contains(box.right, item)


def has_next(x):
    return isinstance(x, ast.Var)


def transist(x):
    return x.argument if isinstance(x, ast.Neg) else ast.Neg(x)


def contraversial(antecedent, succedent, exists_mode):
    union = antecedent + succedent
    return any(map(lambda x: x in antecedent, succedent)) or (exists_mode and len(union) == 1 and all(map(has_next, union)))
