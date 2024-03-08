from abc import ABCMeta, abstractmethod


class Stmt():
    def accept(self, visitor):
        methname = 'visit' + self.__class__.__name__ + 'Stmt'
        meth = getattr(visitor, methname, None)
        return meth(self)


class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression


class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer


class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements


class If(Stmt):
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch


class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class Function(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class Return(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value


class Class(Stmt):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods


class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visitExpressionStmt(self, statement):
        pass

    @abstractmethod
    def visitPrintStmt(self, statement):
        pass

    @abstractmethod
    def visitVarStmt(self, statement):
        pass

    @abstractmethod
    def visitBlockStmt(self, statement):
        pass

    @abstractmethod
    def visitIfStmt(self, statement):
        pass

    @abstractmethod
    def visitWhileStmt(self, statement):
        pass

    @abstractmethod
    def visitClassStmt(self, statement):
        pass
