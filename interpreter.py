import expr
import stmt
from token_type import TokenType
from error import RuntimeError_, hadRunTimeError
from environment import Environment
from callable_ import Callable_
from native_functions import Clock
from function import Function
from return_ import Return
from class_ import Class_
from instance import Instance
import ast_printer


class Interpreter(expr.Visitor, stmt.Visitor):
    def __init__(self):
        self.globals = Environment()
        self.globals.define("clock", Clock())
        self.environment = self.globals
        # self.environment = Environment()
        self.locals = {}

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
            # value = self.evaluate(exp)
            # return self.stringify(value)
        except RuntimeError_ as e:
            e.report()
            hadRunTimeError = True

    def execute(self, statement):  # 其实execute和evaluate可以合在一起...
        statement.accept(self)

    def resolve(self, exp, depth):
        self.locals[exp] = depth

    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def evaluate(self, exp):
        return exp.accept(self)

    def visitLiteralExpr(self, exp):
        return exp.value

    def visitGroupingExpr(self, exp):
        return self.evaluate(exp.expression)

    def visitUnaryExpr(self, exp):
        right = self.evaluate(exp.right)
        t = exp.operator.type
        if t == TokenType.MINUS:
            self.checkNumberOperand(exp.operator, right)
            return -right
        elif t == TokenType.BANG:
            return not self.isTruthy(right)

    def visitBinaryExpr(self, exp):
        left = self.evaluate(exp.left)
        right = self.evaluate(exp.right)
        t = exp.operator.type

        if t == TokenType.MINUS:
            self.checkNumberOperands(exp.operator, left, right)
            return left - right
        elif t == TokenType.SLASH:
            self.checkNumberOperands(exp.operator, left, right)
            return left / right
        elif t == TokenType.STAR:
            self.checkNumberOperands(exp.operator, left, right)
            return left * right
        elif t == TokenType.PLUS:
            try:
                return left + right
            except TypeError:
                raise RuntimeError_(
                    exp.operator, "Operands must be two numbers or two strings.")
        elif t == TokenType.GREATER:
            self.checkNumberOperands(exp.operator, left, right)
            return left > right
        elif t == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(exp.operator, left, right)
            return left >= right
        elif t == TokenType.LESS:
            self.checkNumberOperands(exp.operator, left, right)
            return left < right
        elif t == TokenType.LESS_EQUAL:
            self.checkNumberOperands(exp.operator, left, right)
            return left <= right
        elif t == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        elif t == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)

    def visitExpressionStmt(self, statement):
        self.evaluate(statement.expression)

    def visitPrintStmt(self, statement):
        value = self.evaluate(statement.expression)
        print(self.stringify(value))

    def visitVarStmt(self, statement):
        value = None
        if statement.initializer != None:
            value = self.evaluate(statement.initializer)
        self.environment.define(statement.name, value)

    def visitVariableExpr(self, exp):
        # return self.environment.get(exp.name)
        return self.lookUpVariable(exp.name, exp)

    def lookUpVariable(self, name, exp):
        distance = self.locals.get(exp)
        if distance != None:
            return self.environment.getAt(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def visitAssignExpr(self, exp):
        value = self.evaluate(exp.value)
        # self.environment.assign(exp.name,value)
        distance = self.locals.get(exp)
        if distance != None:
            self.environment.assignAt(distance, exp.name, value)
        else:
            self.globals.assign(exp.name, value)
        return value

    def visitLogicalExpr(self, exp):
        left = self.evaluate(exp.left)
        if exp.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        return self.evaluate(exp.right)

    def visitSetExpr(self, exp):
        obj = self.evaluate(exp.obj)

        if not isinstance(obj, Instance):
            raise RuntimeError_(exp.name, "Only instances hava fields.")
        value = self.evaluate(exp.value)
        obj.set(exp.name, value)
        return value

    def visitSuperExpr(self, exp):
        distance = self.locals.get(exp)
        superclass = self.environment.getAt(distance, "super")

        obj = self.environment.getAt(distance-1, "this")

        method = superclass.findMethod(exp.method.lexeme)

        if method == None:
            raise RuntimeError_(exp.method,"Undefined property '" + exp.method.lexeme + "'.")

        return method.bind(obj)

    def visitThisExpr(self, exp):
        return self.lookUpVariable(exp.keyword, exp)

    def visitCallExpr(self, exp):
        callee = self.evaluate(exp.callee)
        arguments = []
        for argument in exp.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, Callable_):
            raise RuntimeError_(
                exp.paren, "Can only call functions and classes.")
        function = callee
        if len(arguments) != function.arity():
            raise RuntimeError_(exp.paren, "Expected " + function.arity() +
                                " arguments but got " + len(arguments) + ".")
        return function.call(self, arguments)

    def visitGetExpr(self, exp):
        obj = self.evaluate(exp.obj)
        if isinstance(obj, Instance):
            return obj.get(exp.name)

        raise RuntimeError_(exp.name, "Only instances have properties.")

    def visitBlockStmt(self, statement):
        self.executeBlock(statement.statements, Environment(self.environment))

    def visitClassStmt(self, statement):
        superclass = None
        if statement.superclass != None:
            superclass = self.evaluate(statement.superclass)
            if not isinstance(superclass, Class_):
                raise RuntimeError_(statement.superclass.name,
                                    "Superclass must be a class.")

        self.environment.define(statement.name.lexeme, None)

        if statement.superclass != None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {}
        for method in statement.methods:
            function = Function(method, self.environment,
                                method.name.lexeme == "init")
            methods[method.name.lexeme] = function

        klass = Class_(statement.name.lexeme, superclass, methods)

        if superclass != None:
            self.environment = self.environment.enclosing

        self.environment.assign(statement.name, klass)

    def visitIfStmt(self, statement):
        if self.isTruthy(self.evaluate(statement.condition)):
            self.execute(statement.thenBranch)
        elif statement.elseBranch != None:
            self.execute(statement.elseBranch)

    def visitWhileStmt(self, statement):
        while self.isTruthy(self.evaluate(statement.condition)):
            self.execute(statement.body)

    def visitFunctionStmt(self, statement):
        # function = Function(statement, self.environment)
        function = Function(statement, self.environment, False)
        self.environment.define(statement.name.lexeme, function)

    def visitReturnStmt(self, statement):
        value = None
        if statement.value != None:
            value = self.evaluate(statement.value)
        raise Return(value)

    def isEqual(self, a, b):
        return a == b

    def isTruthy(self, obj):
        if type(obj) == bool:
            return obj
        elif obj == None:
            return False
        else:  # lox和ruby一样不把0当成false
            return True

    def checkNumberOperand(self, operator, operand):
        if type(operand) == int or type(operand) == float:
            return
        else:
            raise RuntimeError_(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator, left, right):
        if type(left) in [int, float] and type(right) in [int, float]:
            return
        else:
            raise RuntimeError_(operator, "Operands must be numbers.")

    def stringify(self, obj):
        if obj == None:
            return "nil"
        elif type(obj) in [int, float]:
            text = str(obj)
            if text[-2:] == '.0':
                text = text[0:-2]
            return text
        return str(obj)
