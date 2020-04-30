#   spbu2020_mathematical_logic
The program in this repository implements an algorithm for automated proof search in the Sequent Calculus for First-Order Logic.


##   Pre-requirements
The program uses rply library, it could be installed with either
`pip install rply` 
or 
`conda install -c conda-forge rply`. 

Recommend python version is >= 3.7.


##   Usage
We assume you are now in 'spbu2020_mathematical_logic' directory.

To launch tests, run `python tests.py`.

To run program with your input, run `python main.py 'str1' 'str2' ... 'strN'`, where str is FOL expression in which available next constructions:


```
AND ::= '/\'
OR ::= '\/'
NOT ::= '~'
IMPLICATION ::= '->'
FORALL ::= '+'
EXISTS ::= '!'

Functional_symbol ::= 'F'[0-9]*
Predicate_symbol ::= 'P'[0-9]*  

Var ::= [a-z]+
Term ::= Var | Functional_symbol '(' ((Term ',')* Term)? ')' 
Expr ::= Predicate_symbol '(' ((Term ',')* Term)? ')' | '(' Expr ')' 
        | NOT Expr | Expr AND Expr | Expr OR Expr | Expr IMPLICATION Expr 
        | EXISTS Var Expr | FORALL Var Expr
```
