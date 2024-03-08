import token_type

class Token:
    def __init__(self,type,lexeme,literal,line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self):
        # lexeme = self.lexeme.replace('\n','\\n')
        # literal = str(self.literal).replace('\n','\\n') if type(self.literal)==str else str(self.literal)
        return str(self.type) + " " + self.lexeme + " " + str(self.literal)