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
import numpy as np

# Create a new model
model = gp.Model("example_3")

# Set parameters 
I = 2
J = 3
A = [3, 5]
B = np.array([[1, 0],
              [0, 2],
              [3, 2]])
C = [4, 12, 18]


# Create variables
x = model.addVars(I, lb=0, vtype=GRB.CONTINUOUS, name="x")

# Set objective functions
model.setObjective(gp.quicksum(A[i] * x[i] for i in range(I)), GRB.MAXIMIZE)

# Add constraints
for j in range(J):
    model.addConstr(gp.quicksum(B[j, i] * x[i] for i in range(I)) <= C[j], "c%d" % j)      # New!!!


# Optimize the model
model.optimize()

# Create .lp file
model.write("example_3.lp")

# Print solutions
if model.status == GRB.OPTIMAL:
    print("Optimal solution found.")
    print("Number of variables: ", model.numVars)
    print("Number of constraints: ", model.numConstrs)
    print("Objective value: ", model.objVal)
    for v in model.getVars():
        print("%s = %.4f"%(v.varName, v.x))
else:
    print("No solution found.")