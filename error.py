from token_type import TokenType

hadError = False
hadRunTimeError = False


class LexerError(Exception):
    def __init__(self, line, message):
        self.line = line
        self.message = message
        self.where = ""

    def report(self):
        print("[line " + str(self.line) + "] Error" +
              self.where + ": " + self.message)


class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def report(self):
        where = "at '" + str(self.token.lexeme) + "'"
        if self.token.type == TokenType.EOF:
            where = "at end"
        print("[line {}] Error {}: {}".format(
            str(self.token.line), where, self.message))


class RuntimeError_(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def report(self):
        # print(self.message + "\n[line " + str(self.token.line) + "]")
        print("[line " + str(self.token.line) + "]" + self.message)
