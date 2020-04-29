from rply.token import BaseBox


class Var(BaseBox):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value

    def copy(self):
        return self.__class__(self.value)

    def show(self):
        return f'{self.__class__.__name__} {self.value}'


class UnaryOp:
    def __init__(self, argument):
        self.argument = argument

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.argument == other.argument

    def copy(self):
        return self.__class__(self.argument.copy())

    def show(self):
        return f'{self.__class__.__name__}({self.argument.show()})'


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.left == other.left and self.right == other.right

    def copy(self):
        return self.__class__(self.left.copy(), self.right.copy())

    def show(self):
        return f'{self.__class__.__name__}({self.left.show()},{self.right.show()})'


class Negation(UnaryOp):
    def introduce(self):
        # if isinstance(self.argument, Exists):
        #     expr = Forall(self.argument.left, Negation(self.argument.right))
        # elif isinstance(self.argument, Forall):
        #     expr = Exists(self.argument.left, Negation(self.argument.right))
        # else:
        #     expr = self.argument

        # return [(self, [], [expr])]
        return [(self, [], [self.argument])]

    def eliminate(self):
        if isinstance(self.argument, Forall):
            expr = Exists(self.argument.left, Negation(self.argument.right))
            return [(self, [], [expr])]
        else:
            # elif isinstance(self.argument, Exists):
            #     expr = Forall(self.argument.left, Negation(self.argument.right))
            # else:
            #     expr = self.argument

            return [(self, [self.argument], [])]


class Imp(BinaryOp):
    def introduce(self):
        return [(self, [], [self.left]), (self, [self.right], [])]

    def eliminate(self):
        return [(self, [self.left], [self.right])]


class Disj(BinaryOp):
    def introduce(self):
        return [(self, [self.left], []), (self, [self.right], [])]

    def eliminate(self):
        return [(self, [], [self.left, self.right])]


class Conj(BinaryOp):
    def introduce(self):
        return [(self, [self.left, self.right], [])]

    def eliminate(self):
        return [(self, [], [self.left]), (self, [], [self.right])]


index = 0


class Forall(BinaryOp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.depth = 0

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if (self.left != other.left):
                self.right = substitute(self.left, other.left, self.right)
                self.left = other.left
            return self.right == other.right

        return False

    def introduce(self):
        global index
        index += 1
        if self.depth < 1:
            self.depth += 1
            return [(self, [Substitute(Var(f'_v{index}'), substitute(self.left, Var(f'_v{index}'), self.right)), self], [])]
        else:
            return [(self, [Substitute(Var(f'_v{index}'), substitute(self.left, Var(f'_v{index}'), self.right))], [])]

    def eliminate(self):
        global index
        index += 1
        return [(self, [], [substitute(self.left, Var(f'_c{index}'), self.right)])]


class Exists(BinaryOp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.depth = 0

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if (self.left != other.left):
                self.right = substitute(self.left, other.left, self.right)
                self.left = other.left
            return self.right == other.right

        return False

    def introduce(self):
        global index
        index += 1
        return [(self, [substitute(self.left, Var(f'_c{index}'), self.right)], [])]

    def eliminate(self):
        global index
        index += 1
        if self.depth < 1:
            self.depth += 1
            return [(self, [], [Substitute(Var(f'_v{index}'), substitute(self.left, Var(f'_v{index}'), self.right)), self])]
        else:
            return [(self, [], [Substitute(Var(f'_v{index}'), substitute(self.left, Var(f'_v{index}'), self.right))])]


class Substitute(BinaryOp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def show(self):
        return f'{self.__class__.__name__}({self.left.show()} in {self.right.show()})'

    def collise(self):
        global index
        index += 1
        if self.left.value.startswith('_v'):
            new_name = f'_v{index}'
        else:
            new_name = f'_t{index}'
        self.right = substitute(self.left, Var(new_name), self.right)
        self.left = Var(new_name)


def substitute(old, new, expr):
    res = expr.copy()
    if expr == old:
        res = new
    elif issubclass(type(expr), UnaryOp):
        res.argument = substitute(old, new, res.argument)
    elif isinstance(expr, Forall) or isinstance(expr, Exists):
        if expr.left != old:
            res.right = substitute(old, new, res.right)
        else:
            global index
            index += 1
            if expr.left.value.startswith('_v'):
                res.left = Var(f'_v{index}')
            else:
                res.left = Var(f'_t{index}')
            res.right = substitute(expr.left, res.left, res.right)
            res.right = substitute(old, new, res.right)
    elif issubclass(type(expr), BinaryOp):
        res.left = substitute(old, new, res.left)
        res.right = substitute(old, new, res.right)

    return res
