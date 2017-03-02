import cplex

#prob = cplex.Cplex()

tran_obj = [35, 30, 40, 32, 37, 40, 42, 25, 40, 15, 20, 28]
tran_node_name = ["x11", "x12", "x13", "x14",
                 "x21", "x22", "x23", "x24",
                 "x31", "x32", "x33", "x34"]
tran_rhs = [1200, 1000, 800, 1100, 400, 750, 750]
tran_row_name = ["c" + str(i) for i in range(1, 8)]
tran_sense = ["L","L","L","G","G","G","G"]





def transportation_problem():
    try:
        prob = cplex.Cplex()
        prob.set_problem_name("Transportation Problem")
        populate(prob)
        prob.solve()
        prob.write("transportation.lp")
        #print "Stats   : "
        #print prob.get_stats()
        print "Solutions            :", prob.solution.get_values()
        print "Reduced Cost         :", prob.solution.get_reduced_costs()
        print "Dual Values          :", prob.solution.get_dual_values()
        print "Solution value       :", prob.solution.get_objective_value()
    except:
        print "error"
        exit(1)

def populate(prob):
   prob.objective.set_name("Minimize Cost")
   prob.objective.set_sense(prob.objective.sense.minimize)
   prob.variables.add(obj = tran_obj, names=tran_node_name)

   exp = [[["x11", "x12", "x13", "x14"],[1,1,1,1]],
          [["x21", "x22", "x23", "x24"],[1,1,1,1]],
          [["x31", "x32", "x33", "x34"],[1,1,1,1]],
          [["x11", "x21", "x31"],  [1,1,1]],
          [["x12", "x22", "x32"], [1,1,1]],
          [["x13", "x23", "x33"], [1,1,1]],
          [["x14", "x24", "x34"], [1,1,1]]
          ]

   prob.linear_constraints.add(lin_expr=exp, rhs=tran_rhs,names=tran_row_name, senses=tran_sense)
   #print [prob.linear_constraints.get_rows("c"+str(i)) for i in range(1,8)]
   print prob.linear_constraints.get_rows("c1")
   print prob.linear_constraints.get_rows("c1").unpack()[0]
   print prob.linear_constraints.get_rows("c1").unpack()[1]
   print prob.linear_constraints.get_rows("c1").ind
   print prob.linear_constraints.get_rows("c1").val
   print prob.linear_constraints.get_names()
   print prob.linear_constraints.get_histogram()

transportation_problem()
