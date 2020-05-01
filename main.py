from solver import solve
import sys

for i in range(1, len(sys.argv)):
    try:
        if solve(sys.argv[i]):
            print(f'Valid: {sys.argv[i]}')
        else:
            print(f'Not valid: {sys.argv[i]}')
    except SyntaxError:
        print(f'Invalid input: \'{str(sys.argv[i])}\'')
    except ValueError as error:
        print(error)
