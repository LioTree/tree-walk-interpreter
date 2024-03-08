from token_type import TokenType,SingleTokenMap,OneTokenMap,TwoTokenMap,KeyWordMap
import token_
import error

class Scanner:
    def __init__(self,source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1

    def scanTokens(self):
        for token in self.scanToken():
            self.tokens.append(token)
        return self.tokens

    def scanToken(self):
        while not self.isAtEnd():
            try:
                c = self.source[self.current]
                cc = self.source[self.current:self.current+2] # 不需要考虑前看越界的问题，py大法好
                if c in SingleTokenMap.keys():
                    yield token_.Token(SingleTokenMap[c],c,None,self.line)
                elif c in OneTokenMap.keys():
                    if cc in TwoTokenMap.keys():
                        yield token_.Token(TwoTokenMap[cc],cc,None,self.line)
                        self.current += 1
                    else:
                        yield token_.Token(OneTokenMap[c],c,None,self.line)
                elif c == '/':
                    if cc == '//':
                        self.comment()
                    else:
                        yield token_.Token(TokenType.SLASH,'/',None,self.line)
                elif c == '"':
                    yield self.string()
                elif c.isdigit():
                    yield self.number()
                elif c.isalpha() or c=='_':
                    yield self.identifier()
                elif c==' ' or c=='\t' or c=='\r':
                    pass
                elif c=='\n':
                    self.line += 1
                else:
                    raise error.LexerError(self.line,"Unexpected character.")
            except error.LexerError as e:
                error.hadError = True
                e.report()
            finally:
                self.current += 1
        yield token_.Token(TokenType.EOF,'',None,self.line)

    def isAtEnd(self):
        return self.current>=len(self.source)

    def comment(self):
        end = self.source.find('\n',self.current+2)
        if end == -1:
            self.current = len(self.source) # 没找到\n，说明已经是最后一行了，退出循环返回EOF
        else:
            self.current = end-1 # 将self.current前移到\n的前一个位置

    def string(self):
        end = self.source.find('"',self.current+1)
        if end == -1:
            raise error.LexerError(self.line,"Unterminated string.")
        else:
            string_token = token_.Token(TokenType.STRING,self.source[self.current:end+1],self.source[self.current+1:end],self.line)
            self.line += self.source.count('\n',self.current,end)
            self.current = end # 将self.current前移到闭合的"
            return string_token

    def number(self):
        start = self.current
        while not self.isAtEnd() and self.source[self.current].isdigit():
            self.current += 1
        if not self.isAtEnd() and self.source[self.current] == '.':
            self.current += 1
            while not self.isAtEnd() and self.source[self.current].isdigit():
                self.current += 1
            number_token = token_.Token(TokenType.NUMBER,self.source[start:self.current],float(self.source[start:self.current]),self.line)
        else:
            number_token = token_.Token(TokenType.NUMBER,self.source[start:self.current],int(self.source[start:self.current]),self.line)
        self.current -= 1
        return number_token

    def identifier(self):
        start = self.current
        while not self.isAtEnd() and (self.source[self.current].isalnum() or self.source[self.current]=='_'):
            self.current += 1
        lexeme = self.source[start:self.current]
        self.current -= 1
        if lexeme in KeyWordMap.keys():
            return token_.Token(KeyWordMap[lexeme],lexeme,None,self.line)
        else:
            return token_.Token(TokenType.IDENTIFIER,lexeme,None,self.line)