from enum import Enum,auto

class TokenType(Enum):
    # 单字符token
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto() 
    SEMICOLON = auto()
    STAR = auto()

    SLASH = auto() # 要考虑注释，把SLASH单独放出来

    # 一个或两个字符的token
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # 文字
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # 关键字
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()

SingleTokenMap = {
    '(':TokenType.LEFT_PAREN,
    ')':TokenType.RIGHT_PAREN,
    '{':TokenType.LEFT_BRACE,
    '}':TokenType.RIGHT_BRACE,
    ',':TokenType.COMMA,
    '.':TokenType.DOT,
    '-':TokenType.MINUS,
    '+':TokenType.PLUS,
    ';':TokenType.SEMICOLON,
    '*':TokenType.STAR
}

OneTokenMap = {
    '!':TokenType.BANG,
    '=':TokenType.EQUAL,
    '>':TokenType.GREATER,
    '<':TokenType.LESS,
}

TwoTokenMap = {
    '!=':TokenType.BANG_EQUAL,
    '==':TokenType.EQUAL_EQUAL,
    '>=':TokenType.GREATER_EQUAL,
    '<=':TokenType.LESS_EQUAL,
}

KeyWordMap = {
    'and':TokenType.AND,
    'class':TokenType.CLASS,  
    'else':TokenType.ELSE,    
    'false':TokenType.FALSE,  
    'for':TokenType.FOR,      
    'fun':TokenType.FUN,      
    'if':TokenType.IF,        
    'nil':TokenType.NIL,      
    'or':TokenType.OR,        
    'print':TokenType.PRINT,  
    'return':TokenType.RETURN,
    'super':TokenType.SUPER,  
    'this':TokenType.THIS,    
    'true':TokenType.TRUE,
    'var':TokenType.VAR,
    'while':TokenType.WHILE
}
