from rply.token import BaseBox


class Var(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def show(self):
        return f'{self.__class__.__name__} {self.value}'


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def show(self):
        return f'{self.__class__.__name__}({self.left},{self.right})'


class UnaryOp:
    def __init__(self, argument):
        self.argument = argument

    def show(self):
        return f'{self.__class__.__name__}({self.argument})'


class Negation(UnaryOp):
    def eval(self):
        return self.argument.eval()

    def introduce(self):
        return [([], [self.argument])]

    def eliminate(self):
        return [([self.argument], [])]


class Imp(BinaryOp):
    def eval(self):
        return self.left, self.right

    def introduce(self):
        return [([], [self.left]), ([self.right], [])]

    def eliminate(self):
        return [([self.left], [self.right])]


class Disj(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()

    def introduce(self):
        return [([self.left], []), ([self.right], [])]

    def eliminate(self):
        return [([], [self.left, self.right])]


class Conj(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()

    def introduce(self):
        return [([self.left, self.right], [])]

    def eliminate(self):
        return [([], [self.left]), ([], [self.right])]


class Forall(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()


class Exists(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()
