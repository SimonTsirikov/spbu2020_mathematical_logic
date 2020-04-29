from solver import solve
import sys

for i in range(1, len(sys.argv)):
    try:
        if solve(sys.argv[i]):
            print('General.')
        else:
            print('Not general.')
    except:
        print(f'Invalid input: "{str(sys.argv[i])}".')
