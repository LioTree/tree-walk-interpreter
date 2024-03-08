import expr
import stmt
from error import ParseError, hadError
from enum import Enum, auto


class FunctionType(Enum):
    NONE = auto(),
    FUNCTION = auto(),
    INITIALIZER = auto(),
    METHOD = auto()


class ClassType(Enum):
    NONE = auto(),
    CLASS = auto(),
    SUBCLASS = auto()


class Resolver(expr.Visitor, stmt.Visitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.currentFunction = FunctionType.NONE
        self.currentClass = ClassType.NONE

    def visitBlockStmt(self, statement):
        self.beginScope()
        self.resolve(statement.statements)
        self.endScope()

    def visitClassStmt(self, statement):
        enclosingClass = self.currentClass
        self.currentClass = ClassType.CLASS
        self.declare(statement.name)
        self.define(statement.name)

        if statement.superclass != None and statement.name.lexeme == statement.superclass.name.lexeme:
            raise ParseError(statement.superclass.name,
                             "A class can't inherit from itself.")

        if statement.superclass != None:
            self.currentClass = ClassType.SUBCLASS
            self.resolve(statement.superclass)

        if statement.superclass != None:
            self.beginScope()
            self.scopes[len(self.scopes)-1]["super"] = True

        self.beginScope()
        self.scopes[len(self.scopes)-1]["this"] = True

        for method in statement.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self.resolveFunction(method, declaration)

        self.endScope()

        if statement.superclass != None:
            self.endScope()

        self.currentClass = enclosingClass

    def visitVarStmt(self, statement):
        self.declare(statement.name)
        if statement.name != None:
            self.resolve(statement.initializer)
        self.define(statement.name)

    def visitGetExpr(self, exp):
        self.resolve(exp.obj)

    def resolve(self, args):
        try:
            if isinstance(args, list):
                statements = args
                for statement in statements:
                    self.resolve(statement)
            elif isinstance(args, stmt.Stmt):
                statement = args
                statement.accept(self)
            elif isinstance(args, expr.Expr):
                exp = args
                exp.accept(self)
        except ParseError as e:
            e.report()
            hadError = True

    def visitVariableExpr(self, exp):
        if (not len(self.scopes) == 0) and self.scopes[len(self.scopes)-1].get(exp.name.lexeme) == False:
            raise ParseError(
                exp.name, "Can't read local variable in its own initializer.")
        self.resolveLocal(exp, exp.name)

    def visitAssignExpr(self, exp):
        self.resolve(exp.value)
        self.resolveLocal(exp, exp.name)

    def visitFunctionStmt(self, statement):
        self.declare(statement.name)
        self.define(statement.name)

        self.resolveFunction(statement, FunctionType.FUNCTION)

    def visitExpressionStmt(self, statement):
        self.resolve(statement.expression)

    def visitIfStmt(self, statement):
        self.resolve(statement.condition)
        self.resolve(statement.thenBranch)
        if statement.elseBranch != None:
            self.resolve(statement.elseBranch)

    def visitPrintStmt(self, statement):
        self.resolve(statement.expression)

    def visitReturnStmt(self, statement):
        if self.currentFunction == FunctionType.NONE:
            raise ParseError(statement.keyword,
                             "Can't return from top-level code.")
        if statement.value != None:
            if self.currentFunction == FunctionType.INITIALIZER:
                raise ParseError(statement.keyword,
                                 "Can't return a value from an initializer.")
            self.resolve(statement.value)

    def visitWhileStmt(self, statement):
        self.resolve(statement.condition)
        self.resolve(statement.body)

    def visitBinaryExpr(self, exp):
        self.resolve(exp.left)
        self.resolve(exp.right)

    def visitCallExpr(self, exp):
        self.resolve(exp.callee)

        for argument in exp.arguments:
            self.resolve(argument)

    def visitGroupingExpr(self, exp):
        self.resolve(exp.expression)

    def visitLiteralExpr(self, exp):
        return None

    def visitLogicalExpr(self, exp):
        self.resolve(exp.left)
        self.resolve(exp.right)

    def visitSetExpr(self, exp):
        self.resolve(exp.value)
        self.resolve(exp.obj)

    def visitSuperExpr(self,exp):
        if self.currentClass == ClassType.NONE:
            raise ParseError(exp.keyword,"Can't use 'super' outside of a class.")
        elif self.currentClass != ClassType.SUBCLASS:
            raise ParseError(exp.keyword,"Can't use 'super' in a class with no superclass.")
        self.resolveLocal(exp,exp.keyword)

    def visitThisExpr(self, exp):
        if self.currentClass == ClassType.NONE:
            raise ParseError(
                exp.keyword, "Can't use 'this' outside of a class.")

        self.resolveLocal(exp, exp.keyword)

    def visitUnaryExpr(self, exp):
        self.resolve(exp.right)

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name):
        if len(self.scopes) == 0:
            return
        if name.lexeme in self.scopes[len(self.scopes)-1]:
            raise ParseError(
                name, "Already variable with this name in this scope.")
        self.scopes[len(self.scopes)-1][name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return
        self.scopes[len(self.scopes)-1][name.lexeme] = True

    def resolveLocal(self, exp, name):
        for i in reversed(range(0, len(self.scopes))):
            if name.lexeme in self.scopes[i].keys():
                self.interpreter.resolve(exp, len(self.scopes)-1-i)
                return

    def resolveFunction(self, function, type_):
        enclosingFunction = self.currentFunction
        self.currentFunction = type_
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction
