"""
Maximize
 obj: x1 + 2 x2 + 3 x3
Subject To
 c1: - x1 + x2 + x3 <= 20
 c2: x1 - 3 x2 + x3 <= 30
Bounds
 0 <= x1 <= 40
End
"""
"""
import cplex


simple_lp = cplex.Cplex()
simple_lp.set_problem_name("Simple Linear Problem")

simple_lp.objective.set_sense("LL")
"""

#from __future__ import print_function

import sys

import cplex
from cplex.exceptions import CplexError

# data common to all populateby functions
my_obj = [1.0, 2.0, 3.0]
my_ub = [40.0, cplex.infinity, cplex.infinity]
my_colnames = ["x1", "x2", "x3"]
my_rhs = [20.0, 30.0]
my_rownames = ["c1", "c2"]
my_sense = "LL"

prob = cplex.Cplex()

prob.objective.set_sense(prob.objective.sense.maximize)

# since lower bounds are all 0.0 (the default), lb is omitted here
prob.variables.add(obj=my_obj, ub=my_ub, names=my_colnames)

# can query variables like the following:

# lbs is a list of all the lower bounds
lbs = prob.variables.get_lower_bounds()

# ub1 is just the first lower bound
ub1 = prob.variables.get_upper_bounds(0)

# names is ["x1", "x3"]
names = prob.variables.get_names([0, 2])

rows = [[[0, 1, "x3"], [-1.0, 1.0, 1.0]],
        [["x1", 1, 2], [1.0, -3.0, 1.0]]]

prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                rhs=my_rhs, names=my_rownames)

# because there are two arguments, they are taken to specify a range
# thus, cols is the entire constraint matrix as a list of column vectors
cols = prob.variables.get_cols("x1", "x3")
print prob.linear_constraints.get_rows(0)
print prob.linear_constraints.get_rhs()