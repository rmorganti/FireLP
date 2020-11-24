# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:56:43 2020

@author: Kevin Hennessey
"""


import cvxpy as cp


## Problem 1
t = cp.Variable((5,36), nonneg  = True) # vector variable
e = cp.Variable((4,36), nonneg  = True)
d = cp.Variable((2,36), nonneg  = True)
h = cp.Variable((3,36), nonneg  = True)

obj_func=12

constraints = []
## Budget constraints

## Workforce constraints

## Scheduling/Flow constraints



problem = cp.Problem(cp.Minimize(obj_func), constraints)

problem.solve(solver=cp.GUROBI,verbose = True)

print("obj_func =")
print(obj_func.value)
print("Truck Matrix =")
print(t.value)
print("Engine Matrix =")
print(e.value)
print("Dozer Matrix =")
print(d.value)
print("Helicopter Matrix =")
print(h.value)
