import error
from token_type import TokenType
import token_
import expr
import stmt


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, *types):
        if not self.isAtEnd():
            for t in types:
                if self.tokens[self.current].type == t:
                    self.current += 1
                    return True
        return False

    def isAtEnd(self):
        # return self.current>=len(self.tokens)
        return self.tokens[self.current].type == TokenType.EOF

    def previous(self):
        return self.tokens[self.current-1]

    def consume(self, type, message):
        if self.match(type):
            return self.previous()
        else:
            error.hadError = True
            raise error.ParseError(self.tokens[self.current], message)

    def check(self, type):
        if self.isAtEnd():
            return False
        return self.tokens[self.current].type == type

    def parse(self):
        statements = []
        while not self.isAtEnd():
            # statements.append(self.statement())
            statements.append(self.declaration())
        return statements
        # return self.expression()

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.CLASS):
                return self.classDeclaration()
            return self.statement()
        except error.ParseError as e:
            error.hadError = True
            e.report()
            self.synchronize()
            return None

    def classDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")

        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = expr.Variable(self.previous())

        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")

        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")

        return stmt.Class(name, superclass, methods)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON,
                     "Expect ';' after variable declaration.")
        return stmt.Var(name, initializer)

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.LEFT_BRACE):
            return stmt.Block(self.block())
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.RETURN):
            return self.returnStatement()
        return self.expressionStatement()

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        return stmt.If(condition, thenBranch, elseBranch)

    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return stmt.While(condition, body)

    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()
        if increment != None:
            body = stmt.Block([body, stmt.Expression(increment)])
        if condition == None:
            conditon = expr.Literal(True)
        body = stmt.While(condition, body)
        if initializer != None:
            body = stmt.Block([initializer, body])
        return body

    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return stmt.Return(keyword, value)

    def expressionStatement(self):
        exp = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return stmt.Expression(exp)

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, "Expect " + kind + " name.")
        self.consume(TokenType.LEFT_PAREN,
                     "Expect '(' after " + kind + " name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            if len(parameters) >= 255:
                raise error.ParseError(
                    self.tokens[self.current], "Can't have more than 255 parameters.")
            parameters.append(self.consume(
                TokenType.IDENTIFIER, "Expect parameter name."))

            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    raise error.ParseError(
                        self.tokens[self.current], "Can't have more than 255 parameters.")
                parameters.append(self.consume(
                    TokenType.IDENTIFIER, "Expect parameter name."))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE,
                     "Expect '{' before " + kind + " body.")
        body = self.block()
        return stmt.Function(name, parameters, body)

    def expression(self):
        return self.assignment()
        # return self.equality()

    def assignment(self):
        # exp = self.equality()
        exp = self.or_()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(exp, expr.Variable):
                name = exp.name
                return expr.Assign(name, value)
            elif isinstance(exp, expr.Get):
                get = exp
                return expr.Set(get.obj, get.name, value)
            # raise error.RuntimeError_(equals, "Invalid assignment target.")
            raise error.ParseError(equals, "Invalid assignment target.")
        return exp

    def or_(self):
        exp = self.and_()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            exp = expr.Logical(exp, operator, right)
        return exp

    def and_(self):
        exp = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            exp = expr.Logical(exp, operator, right)
        return exp

    def equality(self):
        exp = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            left = exp
            operator = self.previous()
            right = self.comparison()
            exp = expr.Binary(left, operator, right)
        return exp

    def comparison(self):
        exp = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            left = exp
            operator = self.previous()
            right = self.term()
            exp = expr.Binary(left, operator, right)
        return exp

    def term(self):
        exp = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            left = exp
            operator = self.previous()
            right = self.factor()
            exp = expr.Binary(left, operator, right)
        return exp

    def factor(self):
        exp = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            left = exp
            operator = self.previous()
            right = self.unary()
            exp = expr.Binary(left, operator, right)
        return exp

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            exp = expr.Unary(operator, right)
            return exp
        else:
            return self.call()
            # return self.primary()

    def call(self):
        exp = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                exp = self.finishCall(exp)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER,
                                    "Expect property name after '.'.")
                exp = expr.Get(exp, name)
            else:
                break
        return exp

    def finishCall(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    raise error.ParseError(
                        self.tokens[self.current], "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN,
                             "Expect ')' after arguments.")
        return expr.Call(callee, paren, arguments)

    def primary(self):
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return expr.Literal(self.previous().literal)
        elif self.match(TokenType.TRUE):
            return expr.Literal(True)
        elif self.match(TokenType.FALSE):
            return expr.Literal(False)
        elif self.match(TokenType.NIL):
            return expr.Literal(None)
        elif self.match(TokenType.LEFT_PAREN):
            exp = self.expression()
            if self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression."):
                return expr.Grouping(exp)
            '''
            if self.match(TokenType.RIGHT_PAREN):
                return expr.Grouping(exp)
            else:
                error.hadError = True
                raise error.ParseError(self.tokens[self.current],"Expect ')' after expression.")
            '''
        elif self.match(TokenType.IDENTIFIER):
            return expr.Variable(self.previous())
        elif self.match(TokenType.THIS):
            return expr.This(self.previous())
        elif self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(TokenType.IDENTIFIER,
                                  "Expect superclass method name.")
            return expr.Super(keyword, method)

    def synchronize(self):
        pass
