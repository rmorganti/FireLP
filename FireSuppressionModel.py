"""
Created on Tue Nov 24 13:56:43 2020
@authors: Kevin Hennessey, Mitch Morganti, Avery Warner, Alex Warning
"""


import cvxpy as cp


### INPUT PARAMETERS (TO CHANGE THE BEHAVIOR OF THE PROBLEM)
# Hour to stop spread of fire by: K hours
K = 6
# Max time to extinguish: fire extinguished in M hours
M = 24
# Output of Regression for Fire Spread
FSP = 577


### REDUCING FIRE SPREAD
# Variable to hold spread
New_FSP = FSP;
# Variable to hold fire size
FSZ = 0

# Loop to grow fire by adding the halved spread repeatedly over the length of the time constrainted to stop spread
# We can't take exact values of fire spread reduced at each hour and still include it in the problem (problem would need to run)
# Next best option is assuming the spread behavior shrinks in a manner such as represented below 
for x in range(K):
	FSZ = New_FSP + FSZ
	New_FSP = New_FSP / 2


### ESTIMATES FOR COST, SUPPRESSION GIVEN BY DATA

# Constant values for resource cost 
Cost_BR10 = 117
Cost_BR20 = 195 
Cost_TR = 340
Cost_DZ = 390 
Cost_HL = 1051

# Constant values for supression rates of resources (may need scaling)
Spr_BR10 = 5
Spr_BR20 = 9
Spr_TR = 18
Spr_DZ = 15 
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
for j in range(M):
	 holdCost = Cost_BR10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j])  + Cost_BR20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + Cost_TR * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])+ Cost_DZ * (DZ[0,j] +  DZ[1,j]) + Cost_HL * (HL[0,j] + HL[1,j] + HL[2,j])
	 CRU = CRU + holdCost


# Cost function is truly in the loop above, but the final value is placed in our variable holder CRU
obj_func = CRU

### SUBJECT TO

# Define constraints
constraints = []

# People constraints (only adjustments here could be people requirements/per resource)
for j in range(M):
	constraints.append(10 * (BR10[0,j] + BR10[1,j] + BR10[2,j] + BR10[3,j] + BR10[4,j]) 
	 + 20 * (BR20[0,j] + BR20[1,j] + BR20[2,j]) + 5 * (TR[0,j] + TR[1,j] + TR[2,j] + TR[3,j])
	 + 1 * (DZ[0,j] +  DZ[1,j]) + 2 * (HL[0,j] + HL[1,j] + HL[2,j]) <= 80)


## Scheduling/Flow constraints
## Brigade 10 can only be utilized 3 out of every 4 hours
for i in range(5):
    for j in range(M - 3):
        # For BR10 i on hour j, enfore constraint that for 4 hours a brigade can only be deployed for 3 hours.
        constraints.append(BR10[i, j] + BR10[i, j+1] + BR10[i, j+2] + BR10[i, j+3]  <= 3)

# Constraint for Brigade 20 Availability/Scheduling
# Loop through each BR20
for i in range(3):
    # Loop through hours
    for j in range(M - 2):
        # For BR20 i on hour j, enfore constraint that for 6 hours a brigade can only be deployed for 4 hours. 
        constraints.append(BR20[i, j] + BR20[i, j+1] + BR20[i, j+2] <= 2)

for i in range(4):
    # Loop through hours
    for j in range(M - 2):
        # For TR i on hour j, enfore constraint that for 3 hours a Truck can only be deployed for 2 hours. 
        constraints.append(TR[i, j] + TR[i, j+1] + TR[i, j+2] <= 2)

for i in range(2):
    # Loop through hours
    for j in range(M - 2):
        # For DZ i on hour j, enfore constraint that for 3 hours a brigade can only be deployed for 2 hours. 
        constraints.append(DZ[i, j] + DZ[i, j+1] + DZ[i, j+2] <= 2)

for i in range(3):
    # Loop through hours
    for j in range(M - 2):
        # For HL i on hour j, enfore constraint that for 3 hours a helicopter can only be deployed for 1 hour. 
        constraints.append(HL[i, j] + HL[i, j+1] + HL[i, j+2]<= 1)

#Constraints for the amount fo equipment released based on Equipment Type

# Only 4 out of 5 BR10 can be deployed within an hour period
for j in range(M):
    constraints.append(BR10[0,j] + BR10[1,j]+ BR10[2,j]+ BR10[3,j]+ BR10[4,j] <= 4)

# Only 2 out of 3 BR20 can be deployed within an hour period
for j in range(M):
    constraints.append(BR20[0,j] + BR20[1,j]+ BR20[2,j] <= 2)

# Only 2 out of 4 TR can be deployed within an hour period
for j in range(M):
    constraints.append(TR[0,j] + TR[1,j]+ TR[2,j] + TR[3,j] <= 2)

## No Constraints on Dozer. Both Dozers may be used simultaneously.

# only 2 out of 3 Helicopters can be relaesed in one hour period
for j in range(M):
    constraints.append(HL[0,j] + HL[1,j]+ HL[2,j] <= 2)


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
