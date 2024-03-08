import error


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        if type(name) == str:
            self.values[name] = value
        else:
            self.values[name.lexeme] = value

    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        if self.enclosing != None:
            return self.enclosing.get(name)
        raise error.RuntimeError_(
            name, "Undefined variable '" + name.lexeme + "'.")

    def getAt(self, distance, name):
        return self.ancestor(distance).values[name]

    def ancestor(self, distance):
        environment = self
        for i in range(0, distance):
            environment = environment.enclosing
        return environment

    def assign(self, name, value):
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
        elif self.enclosing != None:
            self.enclosing.assign(name, value)
        else:
            raise error.RuntimeError_(
                name, "Undefined variable '" + name.lexeme + "'.")

    def assignAt(self, distance, name, value):
        self.ancestor(distance).values[name.lexeme] = value
