# Created time: 2023_12_03
# Created by: Chiu

"""
The WYNDOR Glass Co. problem

Max  3 x1 + 5 x2
s.t.   x1        <= 4
            2 x2 <= 12
     3 x1 + 2 x2 <= 18

       x1, x2 >= 0
"""

# import module
import gurobipy as gp
from gurobipy import GRB

# Create a new model
model = gp.Model("example_1")

# Create variables
x1 = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="x1")
x2 = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="x2")

# Set objective functions
model.setObjective(3 * x1 + 5 * x2, GRB.MAXIMIZE)

# Add constraints
model.addConstr(x1 <= 4, 'c1')
model.addConstr(2 * x2 <= 12, 'c2')
model.addConstr(3 * x1 + 2 * x2 <= 18, 'c3')

# Optimize the model
model.optimize()

# Create .lp file
model.write("example_1.lp")

# Print solutions
if model.status == GRB.OPTIMAL:
    print("Optimal solution found.")
    print("Objective value: ", model.objVal)
    print("x1 = ", x1.x)
    print("x2 = ", x2.x)
else:
    print("No solution found.")