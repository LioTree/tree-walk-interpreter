from expr import *
from token_type import *
from token_ import Token
from ast_printer import *

expression = Binary(
  Unary(
    Token(TokenType.MINUS,"-",None,1),
    Literal(123)
  ),
  Token(TokenType.STAR,"*",None,1),
  Grouping(Literal(45.67))
)

output = AstPrinter().print(expression)
print(output)