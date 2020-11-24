"""
Created on Tue Nov 24 13:56:43 2020
@authors: Kevin Hennessey, Mitch Morganti, Avery Warner, Alex Warning
"""


import cvxpy as cp

## Output of Regression for Fire Spread
FSP = 1

## Constant values for resource cost (to be changed)
Cost_BR10 = 1
Cost_BR20 = 1
Cost_TR = 1
Cost_DZ = 1
Cost_HL = 1

## Constant values for supression rates of resources (to be changed)
Spr_BR10 = 1
Spr_BR20 = 1
Spr_TR = 1
Spr_DZ = 1
Spr_HL = 1


## Decision variables: binary {0,1} for if resource i (row) was used during hour j (column)
## Matrices specific to each resource type
BR10 = cp.Variable((5,36), boolean  = True) 
BR20 = cp.Variable((3,36), boolean = True)
TR = cp.Variable((4,36), boolean = True)
DZ = cp.Variable((2,36), boolean  = True)
HL = cp.Variable((3,36), boolean = True)

# Cost of resources used
CRU = cp.Variable(1, nonneg = True)

# cost here
constraints.append()

obj_func = CRU

constraints = []
## People constraints

## Scheduling/Flow constraints

## Fire Damage/Reduce Fire Spread Constraints



problem = cp.Problem(cp.Minimize(obj_func), constraints)

problem.solve(solver=cp.GUROBI,verbose = True)

print("obj_func =")
print(obj_func.value)
print("Brigade of 10 Matrix =")
print(BR10.value)
print("Brigade of 20 Matrix =")
print(BR20.value)
print("Truck Scheduling Matrix = ")
print(TR.value)
print("Dozer Matrix =")
print(DZ.value)
print("Helicopter Matrix =")
print(HL.value)
