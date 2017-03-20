from __future__ import print_function
import cplex
from nwgen import SubstrateNetwork, VirtualNetwork

class SubstrateNetworkData(object):
    def __init__(self):
        self.nbNodesOfSubstrateNetwork = None
        self.ctnProbability = None # connection probability
        # for randomly create cpu capacity property
        self.lbOfCpuCapacity = None
        self.ubOfCpuCapacity = None
        # for randomly create bandwidth capacity property
        self.lbOfBandwidthCapacity = None
        self.ubOfBandwidthCapacity = None

    def readData(self, d):
        #todo: a method to read data from external file or data source.
        pass

substrateNetworkData = SubstrateNetworkData()
substrateNetworkData.nbNodesOfSubstrateNetwork = 8
substrateNetworkData.ctnProbability = 0.5
substrateNetworkData.lbOfBandwidthCapacity = 50
substrateNetworkData.ubOfBandwidthCapacity = 100
substrateNetworkData.lbOfCpuCapacity = 50
substrateNetworkData.ubOfCpuCapacity = 100

sn = SubstrateNetwork( substrateNetworkData.nbNodesOfSubstrateNetwork, substrateNetworkData.ctnProbability)

sn.setCpuCapacity( substrateNetworkData.lbOfCpuCapacity, substrateNetworkData.ubOfCpuCapacity )
sn.setBandwidthCapacity( substrateNetworkData.lbOfBandwidthCapacity, substrateNetworkData.ubOfBandwidthCapacity )
sn.setBandwidthCost(1, 20)
sn.setCpuCost(1, 20)

vn = VirtualNetwork(4, 0.5)
vn.setBandwidthRequirement(1, 50)
vn.setCpuRequirement(1, 50)
#argumentGraph = sn.createArgumentGraph(vn)
#print(argumentGraph.nodes())


def generateNodeDecisionVariable(vn, sn):
    return [
            ['Xv' + str(i) + 's' + str(j) for j in range(0, sn.number_of_nodes()) ]
            for i in range(0, vn.number_of_nodes())
           ]



def generateLinkDecisionVariable(vn, sn):
    return ['Y_' + str(e[0]) + '_' + str(e[1]) for e in sn.edges()] \
           + ['Y_' + str(e[1]) + '_' + str(e[0]) for e in sn.edges()]



def constructFlowConstraintsRow(G, node):
    neighbors = G.getNeighbors(node)
    return [['Y_' + str(n) + '_' + str(node) for n in neighbors]
           + ['Y_' + str(node) + '_' + str(n) for n in neighbors],
           [ 1 for i in neighbors] + [-1 for i in neighbors]]


def constructNodeConstraints(G, node, rhs, name):
    """
    Construct flow constraints of node
    :param G: the network graph
    :param node: the node name
    :param rhs: the right hands of constraints, rhs should only be -1, 1 or 0
    :param name: the name of the row of the constraints
    :return: a tuple with row decision name, right hand, sense, and row name
             example:
                    ([['Y_0_meta_0', 'Y_4_meta_0', 'Y_meta_0_0', 'Y_meta_0_4'], [1, 1, -1, -1]], 1, 'E', 'src_node')
    """
    row = constructFlowConstraintsRow(G, node)
    row_rhs = rhs
    sense = 'E'
    row_name = name
    return (row, row_rhs, sense, row_name)

def constructSourceNodeConstraints(G, sourceNode):
    return constructNodeConstraints(G, sourceNode, -1, 'src_node')

def constructDestinationNodeConstraints(G, destinationNode):
    return constructNodeConstraints(G, destinationNode, 1, 'dst_node')

argumentGraph = sn.copy()
argumentGraph = sn.addMetaNode(argumentGraph, vn, 'meta_0')
argumentGraph = sn.addMetaNode(argumentGraph, vn, 'meta_1')

decision_name_link = generateLinkDecisionVariable(vn, argumentGraph)
obj_cost = [ 1 for i in range(0, len(decision_name_link )) ]

src_constraints = constructSourceNodeConstraints(argumentGraph, 'meta_0')
dst_constraints = constructDestinationNodeConstraints(argumentGraph, 'meta_1')


#btype = ['B' for i in range(0, len(decision_name_link))]
#bytpe = ''.join(btype)
btype = 'B' * len(decision_name_link)

row = []
row_rhs = []
row_sense = []
row_name = []

def appendFlowConstraint(row_tuple, row, rhs, sense, name):
    #todo: handle  all param validation
    row.append(row_tuple[0])
    rhs.append(row_tuple[1])
    sense.append(row_tuple[2])
    name.append(row_tuple[3])


appendFlowConstraint(src_constraints, row, row_rhs, row_sense, row_name)
appendFlowConstraint(dst_constraints, row, row_rhs, row_sense, row_name)

for node in sn.nodes():
    row_tuple = constructNodeConstraints(argumentGraph, node, 0, 'node_'+ str(node))
    appendFlowConstraint(row_tuple, row, row_rhs, row_sense, row_name)




for e in argumentGraph.edges():
    print (e)




#todo preprocess, to delete all nodes and links which have not enough capacity for mapping
#todo find out the new substrate nodes for the next mapping <- may be post process
#todo construct a new objective and constraint matrix
prob = cplex.Cplex()
prob.objective.set_sense(prob.objective.sense.minimize)
prob.variables.add(obj=obj_cost, types=btype,names = decision_name_link)
prob.linear_constraints.add(lin_expr = row, senses=''.join(row_sense),rhs=row_rhs, names=row_name)
prob.solve()
print()
print(prob.solution.status[prob.solution.get_status()])
print('Solution value = ', prob.solution.get_objective_value())

numcols = prob.variables.get_num()
numrows = prob.linear_constraints.get_num()

slack = prob.solution.get_linear_slacks()
x = prob.solution.get_values()


for j in decision_name_link:
    print('%10s: Value = %10f' %(j, prob.solution.get_values(j)) )

prob.write('prob.lp')
