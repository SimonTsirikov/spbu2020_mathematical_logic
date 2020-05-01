from rply.token import BaseBox


class Term(BaseBox):
    def __init__(self, name, args=None):
        self.name = name
        self.args = args
        if args is not None:
            for item in args:
                if not isinstance(item, Term):
                    raise ValueError(f'Inappropriate argument for "{self.name}": {item.show()} should be Term, not {item.__class__.__name__}.')
    
    def __eq__(self, other): 
        if self.__class__ == other.__class__ and self.name == other.name:
            eq_args = self.args is None and other.args is None 
            if not (self.args is None or other.args is None):
                eq_args = (len(self.args) == len(other.args) and all([i == j for i, j in zip(self.args, other.args)]))     
            return eq_args
        return False

    def copy(self):
        if self.args is None:
            return self.__class__(self.name)
        else:
            return self.__class__(self.name, self.args.copy())

    def show(self):
        if self.args is None:
            return f'{self.__class__.__name__} {self.name}'
        else:
            return f'{self.__class__.__name__} {self.name}({", ".join(map(lambda x: x.show(), self.args))})'


class Atom(BaseBox):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        for item in args:
            if not isinstance(item, Term):
                raise ValueError(f'Inappropriate argument for "{self.name}": {item.show()} should be Term, not {item.__class__.__name__}.')
    
    def __eq__(self, other):
        if self.__class__ == other.__class__ and self.name == other.name:
            return (len(self.args) == len(other.args) and all([i == j for i, j in zip(self.args, other.args)]))     
        return False

    def copy(self):
        return self.__class__(self.name, self.args.copy())

    def show(self):
        if self.args is None:
            return f'{self.__class__.__name__} {self.name}'
        else:
            return f'{self.__class__.__name__} {self.name}({", ".join(map(lambda x: x.show(), self.args))})'

class UnaryOp:
    def __init__(self, argument):
        if not isinstance(argument, Term):
            self.argument = argument
        else:
            raise ValueError(f'In {self.__class__.__name__}, {argument.show()} should be Expr.')
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.argument == other.argument

    def copy(self):
        return self.__class__(self.argument.copy())

    def show(self):
        return f'{self.__class__.__name__}({self.argument.show()})'


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        if not (isinstance(left, Term) or isinstance(right, Term)):
            self.left = left
            self.right = right
        else:
            raise ValueError(f'In {self.__class__.__name__}, both {left.show()} and {right.show()} should be Expr.')

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right

    def copy(self):
        return self.__class__(self.left.copy(), self.right.copy())

    def show(self):
        return f'{self.__class__.__name__}({self.left.show()},{self.right.show()})'


class Negation(UnaryOp):
    def introduce(self):
        return [(self, [], [self.argument])]

    def eliminate(self):
        # if isinstance(self.argument, Forall):
        #     expr = Exists(self.argument.left, Negation(self.argument.right))
        #     return [(self, [], [expr])]
        # else:
        return [(self, [self.argument], [])]


class Implication(BinaryOp):
    def introduce(self):
        return [(self, [], [self.left]), (self, [self.right], [])]

    def eliminate(self):
        return [(self, [self.left], [self.right])]


class Disjunction(BinaryOp):
    def introduce(self):
        return [(self, [self.left], []), (self, [self.right], [])]

    def eliminate(self):
        return [(self, [], [self.left, self.right])]


class Conjunction(BinaryOp):
    def introduce(self):
        return [(self, [self.left, self.right], [])]

    def eliminate(self):
        return [(self, [], [self.left]), (self, [], [self.right])]


index = 0


class Forall(BinaryOp):
    def __init__(self, left, right):
        if isinstance(left, Term) and (left.args is None) and not isinstance(right, Term):
            self.left = left
            self.right = right
            self.depth = 0
        else:
            raise ValueError(f'In {self.__class__.__name__}, {left.show()} should be Var and {right.show()} should be Expr.')

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.left != other.left:
                self.right = substitute(self.left, other.left, self.right)
                self.left = other.left
            return self.right == other.right

        return False

    def introduce(self):
        global index
        index += 1
        if self.depth < 1:
            self.depth += 1
            return [(self, [Substitute(Term(f'_v{index}'), substitute(self.left, Term(f'_v{index}'), self.right)), self], [])]
        else:
            return [(self, [Substitute(Term(f'_v{index}'), substitute(self.left, Term(f'_v{index}'), self.right))], [])]

    def eliminate(self):
        global index
        index += 1
        return [(self, [], [substitute(self.left, Term(f'_c{index}'), self.right)])]


class Exists(BinaryOp):
    def __init__(self, left, right):
        if isinstance(left, Term) and (left.args is None) and not isinstance(right, Term):
            self.left = left
            self.right = right
            self.depth = 0
        else:
            raise ValueError(f'In {self.__class__.__name__}, {left.show()} should be Var and {right.show()} should be Expr.')

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.left != other.left:
                self.right = substitute(self.left, other.left, self.right)
                self.left = other.left
            return self.right == other.right

        return False

    def introduce(self):
        global index
        index += 1
        return [(self, [substitute(self.left, Term(f'_c{index}'), self.right)], [])]

    def eliminate(self):
        global index
        index += 1
        if self.depth < 1:
            self.depth += 1
            return [(self, [], [Substitute(Term(f'_v{index}'), substitute(self.left, Term(f'_v{index}'), self.right)), self])]
        else:
            return [(self, [], [Substitute(Term(f'_v{index}'), substitute(self.left, Term(f'_v{index}'), self.right))])]


class Substitute(BinaryOp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def show(self):
        return f'{self.__class__.__name__}({self.left.show()} in {self.right.show()})'

    def collision(self):
        global index
        index += 1
        if self.left.name.startswith('_v'):
            new_name = f'_v{index}'
        else:
            new_name = f'_c{index}'
        self.right = substitute(self.left, Term(new_name), self.right)
        self.left = Term(new_name)


def substitute(old, new, expr):
    res = expr.copy()
    if expr == old:
        res = new
    elif isinstance(expr, Atom):
        for i in range(0, len(expr.args)):
            res.args[i] = substitute(old, new, expr.args[i])
    elif issubclass(type(expr), UnaryOp):
        res.argument = substitute(old, new, res.argument)
    elif isinstance(expr, Forall) or isinstance(expr, Exists) or isinstance(expr, Substitute):
        if expr.left != old:
            res.right = substitute(old, new, res.right)
        else:
            global index
            index += 1
            if expr.left.name.startswith('_v'):
                res.left = Term(f'_v{index}')
            else:
                res.left = Term(f'_c{index}')
            res.right = substitute(expr.left, res.left, res.right)
            res.right = substitute(old, new, res.right)
    elif issubclass(type(expr), BinaryOp):
        res.left = substitute(old, new, res.left)
        res.right = substitute(old, new, res.right)

    return res
