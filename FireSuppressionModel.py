"""
Created on Tue Nov 24 13:56:43 2020
@authors: Kevin Hennessey, Mitch Morganti, Avery Warner, Alex Warning
"""


import cvxpy as cp


### INPUT PARAMETERS (TO CHANGE THE BEHAVIOR OF THE PROBLEM)
# Hour to stop spread of fire by: K hours
K = 6
# Max time to extinguish: fire extinguished in M hours
M = 36
# Output of Regression for Fire Spread
FSP = 500


### REDUCING FIRE SPREAD
# Variable to hold spread
New_FSP = FSP;
# Variable to hold fire size
FSZ = 0

# Loop to grow fire by adding the halved spread repeatedly over the length of the time constrainted to stop spread
# We can't take exact values of fire spread reduced at each hour and still include it in the problem (problem would need to run)
# Next best option is assuming the spread behavior shrinks in a manner such as represented below 
for x in range(6):
	FSZ = New_FSP + FSZ
	New_FSP = New_FSP / 2
	print(FSZ)	


### ESTIMATES FOR COST, SUPPRESSION GIVEN BY DATA
# Constant values for resource cost (may need scaling)
Cost_BR10 = 230
Cost_BR20 = 460
Cost_TR = 240
Cost_DZ = 188
# may need to change heli cost
Cost_HL = 1051

# Constant values for supression rates of resources (may need scaling)
Spr_BR10 = 3
Spr_BR20 = 5
Spr_TR = 20
# may need to change dozer 
Spr_DZ = 25
Spr_HL = 30



### OPTIMIZATION CODE BEGINS HERE
# Decision variables: binary {0,1} for if resource i (row) was used during hour j (column).
# Matrices specific to each resource type
BR10 = cp.Variable((5,M), boolean  = True) 
BR20 = cp.Variable((3,M), boolean = True)
TR = cp.Variable((4,M), boolean = True)
DZ = cp.Variable((2,M), boolean  = True)
HL = cp.Variable((3,M), boolean = True)


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

### SUBJECT TO

# Define constraints
constraints = []

# People constraints (only adjustments here could be people requirements/per resource)
for j in range(36):
	constraints.append(10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + 20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + 5 * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + 1 * (DZ[0,j] +  DZ[1,j]) + 2 * (HL[0,j] + HL[1,j] + HL[2,j]) <= 80)


## Scheduling/Flow constraints

# Fire Spread constraint: fire spread must be reduced to 0 in K hours
# Holds constraints and adds together in loop
resources_holder = 0
	 
for j in range(K):
	resources_holder = resources_holder + (Spr_BR10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + Spr_BR20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + Spr_TR * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + Spr_DZ * (DZ[0,j] +  DZ[1,j]) + Spr_HL * (HL[0,j] + HL[1,j] + HL[2,j]))

# constraint: over hours 0-K, suppression must reduce spread to 0
constraints.append(FSP - resources_holder <=0)

# Holds constraints and adds together in loop
resources_holder2 = 0

# For all hours K-M, suppression works against 0 spread; reduces size of the fire (also in chains)
for j in range(K,M):
	resources_holder2 = resources_holder2 + (Spr_BR10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + Spr_BR20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + Spr_TR * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + Spr_DZ * (DZ[0,j] +  DZ[1,j]) + Spr_HL * (HL[0,j] + HL[1,j] + HL[2,j]))

# constraint: over M-K, suppression must expunge the fire
constraints.append(FSZ - resources_holder2 <= 0)	



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
