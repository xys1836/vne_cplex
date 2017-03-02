#from __future__ import print_function
import sys
import cplex

assignment = cplex.Cplex()
assignment.set_problem_name("Assignment_Problem")
assignment.objective.set_name("objective")
print assignment.get_problem_name()
print assignment.objective.get_name()
#assignment.objective.set_sense()
#assignment.variables.add(obj=[],lb=[],ub=[],types="",names=[],columns=[])



