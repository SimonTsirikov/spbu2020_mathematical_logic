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


Grammar        | Meaning
-------------- | -------------
[a-z]+         | variable name
~ expr         | not
expr1 /\ expr2 | and
expr1 \/ expr2 | or
expr1 -> expr2 | implication
! var expr     | exists
\+ var expr     | forall
