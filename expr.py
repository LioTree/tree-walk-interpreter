from abc import ABCMeta, abstractmethod


class Expr():
    def accept(self, visitor):
        methname = 'visit' + self.__class__.__name__ + 'Expr'
        meth = getattr(visitor, methname, None)
        return meth(self)


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class Variable(Expr):
    def __init__(self, name):
        self.name = name


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments


class Get(Expr):
    def __init__(self, obj, name):
        self.obj = obj
        self.name = name


class Set(Expr):
    def __init__(self, obj, name, value):
        self.obj = obj
        self.name = name
        self.value = value


class This(Expr):
    def __init__(self, keyword):
        self.keyword = keyword


class Super(Expr):
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method


class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visitBinaryExpr(self, exp):
        pass

    @abstractmethod
    def visitGroupingExpr(self, exp):
        pass

    @abstractmethod
    def visitLiteralExpr(self, exp):
        pass

    @abstractmethod
    def visitUnaryExpr(self, exp):
        pass

    @abstractmethod
    def visitVariableExpr(self, exp):
        pass

    @abstractmethod
    def visitAssignExpr(self, exp):
        pass

    @abstractmethod
    def visitLogicalExpr(self, exp):
        pass

    @abstractmethod
    def visitCallExpr(self, exp):
        pass

    @abstractmethod
    def visitGetExpr(self, exp):
        pass

    @abstractmethod
    def visitSetExpr(self, exp):
        pass

    @abstractmethod
    def visitThisExpr(self, exp):
        pass

    @abstractmethod
    def visitSuperExpr(self, exp):
        pass
