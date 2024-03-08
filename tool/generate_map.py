keywords = [
    'and',
    'class',
    'else',
    'false',
    'for',
    'fun',
    'if',
    'nil',
    'or',
    'print',
    'return',
    'super',
    'this',
    'true',
    'var',
    'while'
    ]

for k in keywords:
    print("'" + k + "':TokenType." + k.upper() + ',')