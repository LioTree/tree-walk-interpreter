from error import RuntimeError_


class Instance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def __str__(self):
        return self.klass.name + " instance"

    def get(self, name):
        if name.lexeme in self.fields.keys():
            return self.fields[name.lexeme]

        method = self.klass.findMethod(name.lexeme)
        if method != None:
            return method.bind(self)

        raise RuntimeError_(name, "Undefined property '" + name.lexeme + "'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value
