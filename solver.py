from parsec import pparse
import ast


def solve(string):
    expr = pparse(string)
    return resolve([], [expr], False)


def resolve(antecedent, succedent, exists_mode):    
    if contraversial(antecedent, succedent):
        return True

    are_valid_branches_left, exists_mode_1 = check_side(antecedent, succedent, False, exists_mode)
    if are_valid_branches_left is not None:
        return are_valid_branches_left

    are_valid_branches_right, exists_mode_2 = check_side(antecedent, succedent, True, exists_mode_1)
    if are_valid_branches_right is not None:
        return are_valid_branches_right

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

                are_valid_branches = resolve(antecedent_next, succedent_next, reversed)

                if reversed:
                    if are_valid_branches:
                        return True, exists_mode
                elif not exists_mode and not are_valid_branches:
                    return False, exists_mode
                elif exists_mode and are_valid_branches:
                    return True, exists_mode

            return not reversed, exists_mode

        elif not isinstance(i, ast.Atom):
            if not reversed and isinstance(i, ast.Exists):
                exists_mode = True
            elif reversed and isinstance(i, ast.Forall):
                exists_mode = False

            def check(x): return prepare_and_resolve(
                antecedent, succedent, reversed, exists_mode, x)
            func = i.eliminate() if reversed else i.introduce()
            are_valid_branches = all(map(check, func))

            if not exists_mode and not are_valid_branches:
                return False, exists_mode
            elif exists_mode and are_valid_branches:
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
            if var_new is not None:
                result = ast.substitute(mask.left, var_new, mask.right)
                yield result
    end_phase = mask.copy()
    end_phase.collision()
    yield end_phase.right


def traverse_expression_tree(source):
    if isinstance(source, ast.Term):
        yield source
        if source.args is not None:
            for arg in source.args:
                for item in traverse_expression_tree(arg):
                    yield item
    elif isinstance(source, ast.Atom):
        for arg in source.args:
            for item in traverse_expression_tree(arg):
                yield item
    elif issubclass(type(source), ast.UnaryOp):
        for item in traverse_expression_tree(source.argument):
            yield item
    elif aware_recursion(source):
        for item in traverse_expression_tree(source.right):
            if isinstance(item, ast.Term) and not item.name == source.left.name:
                yield item
    elif issubclass(type(source), ast.BinaryOp):
        for item in traverse_expression_tree(source.left):
            yield item
        for item in traverse_expression_tree(source.right):
            yield item
    yield None


def aware_recursion(expr):
    return isinstance(expr, ast.Forall) or isinstance(expr, ast.Exists) or isinstance(expr, ast.Substitute)


def has_next(x):
    return isinstance(x, ast.Atom)


def transist(x):
    return x.argument if isinstance(x, ast.Negation) else ast.Negation(x)


def contraversial(antecedent, succedent):
    return any(map(lambda x: x in antecedent, succedent))
