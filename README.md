#   spbu2020_mathematical_logic
The program in this repository implements an algorithm for automated proof search in the Sequent Calculus for First-Order Logic.


##   Pre-requirements
The program uses third-party libraries, it could be installed with `pip install -r requirements.txt`.

Python version recommended is >= 3.7.


##   Usage
We assume you are now in 'spbu2020_mathematical_logic' directory.

To launch tests, run `python tests.py`.

To run program with your input, run `python main.py 'str1' 'str2' ... 'strN'`, where str is FOL Expr in next grammar:


```
Var ::= [a-z]+
Functional_symbol ::= 'F'[0-9]*
Predicate_symbol  ::= 'P'[0-9]*  

Term ::= Var | Functional_symbol '(' ((Term ',')* Term)? ')' 
Atom ::= Predicate_symbol '(' ((Term ',')* Term)? ')'
Expr ::= Atom | '(' Expr ')' | Negation | Conjunction 
        | Disjunction | Implication | Exists | Forall

Negation    ::= '~' Expr
Conjunction ::= Expr '/\' Expr
Disjunction ::= Expr '\/' Expr
Implication ::= Expr '->' Expr

Forall ::= '+' Var Expr
Exists ::= '!' Var Expr
```
