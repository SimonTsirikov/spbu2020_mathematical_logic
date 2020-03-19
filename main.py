from lexer import lexer
from parsec import parser

str = '+a ~(!b a V c) -> d'

a = parser.parse(lexer.lex(str))
print()
