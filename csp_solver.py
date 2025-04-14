from pycsp3 import *

# Define the variables
x = Var(1, 5)  # Single variable with domain [1, 5]
y = Var(1, 5)  # Another variable with domain [1, 5]

# Define the constraint
satisfy(
    x + y == 6  # Constraint: x + y = 6
)

# Search for a solution
output = solve()

# Print the solution
if output:
    print("Solution found:")
    print("x =", x.value)
    print("y =", y.value)
else:
    print("No solution found")
