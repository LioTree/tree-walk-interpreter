from abc import ABCMeta, abstractmethod

class Stmt(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
      pass

class Class(Stmt):
    def __init__(self,name,methods):
        self.name=name
        self.methods=methods

    def accept(self,visitor):
        return visitor.visitClassStmt(self)

class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visitClassStmt(self,statement):
        pass

