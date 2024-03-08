import expr


class AstPrinter(expr.Visitor):
    def print(self, exp):
        return exp.accept(self)

    def visitBinaryExpr(self, exp):
        return self.parenthesize(exp.operator.lexeme, exp.left, exp.right)

    def visitGroupingExpr(self, exp):
        return self.parenthesize("group", exp.expression)

    def visitLiteralExpr(self, exp):
        if exp.value == None:
            return "nil"
        return str(exp.value)

    def visitUnaryExpr(self, exp):
        return self.parenthesize(exp.operator.lexeme, exp.right)

    def parenthesize(self, name, *exps):
        output = "(" + name
        for exp in exps:
            output += " "
            output += exp.accept(self)
        output += ')'
        return output
