from llvmlite import ir

class Variable():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        return ir.Constant(
              ir.IntType(1)
            , int(self.value)
            )

class UnaryOp():
    def __init__(self, builder, module, argument):
        self.builder = builder
        self.module = module
        self.argument = argument

class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

class TernaryOp():
    def __init__(self, builder, module, left, middle, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.middle = middle
        self.right = right

class Negatiation(UnaryOp):
    def eval(self):
        return self.builder.negatiation(
              self.argument.eval()
            )

class Conjunction(BinaryOp):
    def eval(self):
        return self.builder.conjunction(
              self.left.eval()
            , self.right.eval()
            )

class Disjunction(BinaryOp):
    def eval(self):
        return self.builder.disjunction(
              self.left.eval()
            , self.right.eval()
            )

class Implication(BinaryOp):
    def eval(self):
        return self.builder.implication(
              self.left.eval()
            , self.right.eval()
            )

class Forall(BinaryOp):
    def eval(self):
        return self.builder.forall(
              self.left.eval()
            , self.right.eval()
            )

class Exists(BinaryOp):
    def eval(self):
        return self.builder.exists(
              self.left.eval()
            , self.right.eval()
            )

class Substitution(TernaryOp):
    def eval(self):
        return self.builder.substitution(
              self.left.eval()
            , self.middle.eval()
            , self.right.eval()
            )
