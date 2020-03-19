from rply.token import BaseBox


class Var(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def show(self):
        print(self.__class__.__name__)


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class UnaryOp:
    def __init__(self, argument):
        self.argument = argument


class Negation(UnaryOp):
    def eval(self):
        return self.argument.eval()


class Imp(BinaryOp):
    def eval(self):
        return self.left, self.right


class Disj(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()


class Conj(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()


class Forall(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()


class Exists(BinaryOp):
    def eval(self):
        return self.left.eval(), self.right.eval()