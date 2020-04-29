from solver import solve

assert solve('!a a')
assert solve('~(+a a)')
assert not solve(r'!a (a/\~a)')
assert solve(r'~(!a (a/\~a))')
assert solve('!a (+b (a->b))')
assert solve('+a (!b (a->b))')
assert solve(r'+a (a\/~a)')
assert solve('+a (a->a)')
assert solve(r'(+a (+b ((a -> b) \/ (b -> a))))')
