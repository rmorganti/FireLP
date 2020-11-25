"""
Created on Tue Nov 24 13:56:43 2020
@authors: Kevin Hennessey, Mitch Morganti, Avery Warner, Alex Warning
"""


import cvxpy as cp

# Output of Regression for Fire Spread
FSP = 10
# Var to keep track of fire size. Initial size = arrival time(1) * Fire Spread
FSZ = 1 * FSP
FSP_j = FSP
FSZ_updated = 0
# Constant values for resource cost (to be changed)
Cost_BR10 = 1
Cost_BR20 = 1
Cost_TR = 1
Cost_DZ = 1
Cost_HL = 1

# Constant values for supression rates of resources (to be changed)
Spr_BR10 = 1
Spr_BR20 = 1
Spr_TR = 1
Spr_DZ = 1
Spr_HL = 1


# Decision variables: binary {0,1} for if resource i (row) was used during hour j (column).
# Matrices specific to each resource type
BR10 = cp.Variable((5,36), boolean  = True) 
BR20 = cp.Variable((3,36), boolean = True)
TR = cp.Variable((4,36), boolean = True)
DZ = cp.Variable((2,36), boolean  = True)
HL = cp.Variable((3,36), boolean = True)

constraints = []

# Variables to keep track of Cost Used. CRU represents the final cost with values added to it in running total loop below.
# holdCost holds the cost of resources used at hour j, adds them to the running total
CRU = 0
holdCost = 0



# Complete summation for cost function; this loop truly represents the objective function
# Recall python loop index is number-1 (here is 0 to 35)
for j in range(36):
	 holdCost = Cost_BR10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j])  + Cost_BR20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + Cost_TR * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])+ Cost_DZ * (DZ[0,j] +  DZ[1,j]) + Cost_HL * (HL[0,j] + HL[1,j] + HL[2,j])
	 CRU = CRU + holdCost	


# Cost function is truly in the loop above, but the final value is placed in our variable holder CRU
obj_func = CRU


# People constraints (only adjustments here could be people requirements/per resource)
for j in range(36):
	constraints.append(10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + 20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + 5 * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + 1 * (DZ[0,j] +  DZ[1,j]) + 2 * (HL[0,j] + HL[1,j] + HL[2,j]) <= 50)


## Scheduling/Flow constraints

# Fire Damage/Reduce Fire Spread Constraints
# E.g fire spread must be reduced within 6? hours
for j in range(6):
	constraints.append(FSP - (Spr_BR10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + Spr_BR20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + Spr_TR * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + Spr_DZ * (DZ[0,j] +  DZ[1,j]) + Spr_HL * (HL[0,j] + HL[1,j] + HL[2,j]))<= 0)
	# Keeping track of fire spread to adjust fire size accordingly
	FSP_j = FSP - (Spr_BR10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + Spr_BR20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + Spr_TR * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + Spr_DZ * (DZ[0,j] +  DZ[1,j]) + Spr_HL * (HL[0,j] + HL[1,j] + HL[2,j]))
	# Add to fire size what the spread is at hour j 
	FSZ_updated = FSZ_updated + FSP_j 

# Removing the rest of the fire 
for j in range(6,36):
	constraints.append(FSZ_updated - (Spr_BR10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + Spr_BR20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + Spr_TR * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + Spr_DZ * (DZ[0,j] +  DZ[1,j]) + Spr_HL * (HL[0,j] + HL[1,j] + HL[2,j])) <= 0)


# Solve the problem of minimizing cost of deployed resources, s.t constraints above
problem = cp.Problem(cp.Minimize(obj_func), constraints)

problem.solve(solver=cp.GUROBI,verbose = True)

# Solve 
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
