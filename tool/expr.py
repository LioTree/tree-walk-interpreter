from abc import ABCMeta, abstractmethod

class Expr(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
      pass

class Super(Expr):
    def __init__(self,keyword,method):
        self.keyword=keyword
        self.method=method

    def accept(self,visitor):
        return visitor.visitSuperExpr(self)

class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visitSuperExpr(self,exp):
        pass

