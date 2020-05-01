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
Negation    ::= '~' Expr
Conjunction ::= Expr '/\' Expr
Disjunction ::= Expr '\/' Expr
Implication ::= Expr '->' Expr
Forall ::= '+' Var Expr
Exists ::= '!' Var Expr

Functional_symbol ::= 'F'[0-9]*
Predicate_symbol ::= 'P'[0-9]*  

Var ::= [a-z]+
Term ::= Var | Functional_symbol '(' ((Term ',')* Term)? ')' 
Atom ::= Predicate_symbol '(' ((Term ',')* Term)? ')'
Expr ::= Atom | '(' Expr ')' | Negation | Conjunction 
        | Disjunction | Implication | Exists | Forall
```
