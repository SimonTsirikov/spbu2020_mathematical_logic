from rply import LexerGenerator

lg = LexerGenerator()

lg.add('VAR', r'[a-z]+')
lg.add('NUMBER', r'\d+')

# Operators
lg.add('CONJ', r'\/\\')
lg.add('DISJ', r'\\\/')
lg.add('NEG', r'\~')
lg.add('EXIST', r'\!')
lg.add('SUBSTITUTION', r'\[y\][a-zA-Z]+\:[a-zA-Z]+')
lg.add('ALL', r'\+')
lg.add('IMP', r'\-\>')

# Parenthesis
lg.add('OPEN_PAREN', r'\(')
lg.add('CLOSE_PAREN', r'\)')

# Semi Colon
lg.add('SEMI_COLON', r'\;')

lg.ignore('\s+')

lexer = lg.build()
