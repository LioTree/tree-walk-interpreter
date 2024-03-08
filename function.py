from callable_ import Callable_
from environment import Environment
from return_ import Return


class Function(Callable_):
    def __init__(self, declaration, closure,isInitializer):
        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer

    def call(self, interpreter, arguments):
        # environment = Environment(interpreter.globals)
        environment = Environment(self.closure)
        for param, argument in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, argument)
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            if self.isInitializer:
                return self.closure.getAt(0,"this")
            return returnValue.value
        if self.isInitializer:
            return self.closure.getAt(0,"this")

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"

    def bind(self, ins):
        environment = Environment(self.closure)
        environment.define("this", ins)
        # return Function(self.declaration, environment)
        return Function(self.declaration,environment,self.isInitializer)
