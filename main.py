from __future__ import print_function
import cplex
from nwgen import SubstrateNetwork, VirtualNetwork
from vnemsg import VNE_Message

vne_msg = VNE_Message()

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

vne_msg.debug('vne msg debug')
substrateNetworkData = SubstrateNetworkData()
substrateNetworkData.nbNodesOfSubstrateNetwork = 30
substrateNetworkData.ctnProbability = 0.5
substrateNetworkData.lbOfBandwidthCapacity = 50
substrateNetworkData.ubOfBandwidthCapacity = 100
substrateNetworkData.lbOfCpuCapacity = 50
substrateNetworkData.ubOfCpuCapacity = 100

isConnected = False

sn = SubstrateNetwork()
isConnected = sn.createNetwork( substrateNetworkData.nbNodesOfSubstrateNetwork, substrateNetworkData.ctnProbability)
while not isConnected:
    isConnected = sn.createNetwork( substrateNetworkData.nbNodesOfSubstrateNetwork, substrateNetworkData.ctnProbability)
sn.setCpuCapacity( substrateNetworkData.lbOfCpuCapacity, substrateNetworkData.ubOfCpuCapacity )
sn.setBandwidthCapacity( substrateNetworkData.lbOfBandwidthCapacity, substrateNetworkData.ubOfBandwidthCapacity )
sn.setBandwidthCost(1, 20)
sn.setCpuCost(1, 20)

vn = VirtualNetwork()
isConnected = vn.createNetwork(4, 0.5)
while not isConnected:
    isConnected = vn.createNetwork(4, 0.5)
vn.setBandwidthRequirement(1, 50)
vn.setCpuRequirement(1, 50)



print('######## VN Info #############')
print('vn info')
for e in vn.edges():
    print(e)

print('######## VN Info END #############')
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

def appendFlowConstraint(row_tuple, row, rhs, sense, name):
    #todo: handle  all param validation
    row.append(row_tuple[0])
    rhs.append(row_tuple[1])
    sense.append(row_tuple[2])
    name.append(row_tuple[3])




# mapping_dic = {} #{vn_node : sn_node }
# for node in vn.nodes():
#     mapping_dic[node] = None
#
# for edge in vn.edges():
#
#     print('########################################################################')
#
#     src_node_vn = edge[0]
#     dst_node_vn = edge[1]
#     requirement_src_node_vn = vn.node[src_node_vn]['requirement']
#     requirement_dst_node_vn = vn.node[dst_node_vn]['requirement']
#     src_node_sn = None
#     dst_node_sn = None
#
#     print('Node: %s, requirement: %s' % (src_node_vn, requirement_src_node_vn))
#     print('Node: %s, requirement: %s' % (dst_node_vn, requirement_dst_node_vn))
#     print('bandwidth requirement: %s' % vn.getLinkPropertyBy(edge, 'requirement'))
#     row = []
#     row_rhs = []
#     row_sense = []
#     row_name = []
#
#     argumentGraph = sn.copy()
#     sn_tmp = sn.copy()
#
#     if mapping_dic[src_node_vn] == None:
#         argumentGraph =sn.addMetaNode(argumentGraph, vn, 'meta_' + str(src_node_vn))
#         src_node_sn = 'meta_' + str(src_node_vn)
#         #remove the link which the other node has not enough capacity in argument
#         for n in argumentGraph.getNeighbors(src_node_sn):
#             if argumentGraph.getNodePropertyBy(n, 'capacity') < vn.getNodePropertyBy(src_node_vn, 'requirement'):
#                 print('SRC: not enough cpu capacity %s' %n)
#                 print('remove edge %s - %s ' %(src_node_sn, n))
#                 argumentGraph.removeEdge((src_node_sn, n))
#     else:
#         src_node_sn = mapping_dic[src_node_vn]
#     if mapping_dic[dst_node_vn] == None:
#         argumentGraph = sn.addMetaNode(argumentGraph, vn, 'meta_' + str(dst_node_vn))
#         #remove the links which the other node has not enough capacity in argument nentwork
#         dst_node_sn = 'meta_' + str(dst_node_vn)
#         for n in argumentGraph.getNeighbors(dst_node_sn):
#             if argumentGraph.getNodePropertyBy(n, 'capacity') < vn.getNodePropertyBy(dst_node_vn, 'requirement'):
#                 print('DST: not enough cpu capacity')
#                 print('remove edge %s - %s ' %(dst_node_sn, n))
#                 argumentGraph.removeEdge((dst_node_sn, n))
#
#     else:
#         dst_node_sn = mapping_dic[dst_node_vn]
#     #todo: remove? the nodes that have not enough capacity in argument network
#     #remove the links that have not enough capacity in argument network
#     for e in argumentGraph.edges():
#         if argumentGraph.getLinkPropertyBy(e, 'capacity') < vn.getLinkPropertyBy(edge, 'requirement'):
#             print('Remove edge in argument network %s - %s' %(e[0], e[1]))
#             argumentGraph.removeEdge(e)
#
#
#     # Construct constraints
#     src_constraints = constructSourceNodeConstraints(argumentGraph, src_node_sn)
#     dst_constraints = constructDestinationNodeConstraints(argumentGraph, dst_node_sn)
#
#     appendFlowConstraint(src_constraints, row, row_rhs, row_sense, row_name)
#     appendFlowConstraint(dst_constraints, row, row_rhs, row_sense, row_name)
#
#     decision_name_link = generateLinkDecisionVariable(vn, argumentGraph)
#     obj_cost = [ 1 for i in range(0, len(decision_name_link )) ]
#
#     btype = 'B' * len(decision_name_link)
#
#     for node in argumentGraph.nodes():
#         if node != src_node_sn and node != dst_node_sn:
#             #print(node)
#             row_tuple = constructNodeConstraints(argumentGraph, node, 0, 'node_'+ str(node))
#             appendFlowConstraint(row_tuple, row, row_rhs, row_sense, row_name)
#
#     prob = cplex.Cplex()
#     prob.objective.set_sense(prob.objective.sense.minimize)
#     prob.variables.add(obj=obj_cost, types=btype,names = decision_name_link)
#     prob.linear_constraints.add(lin_expr = row, senses=''.join(row_sense),rhs=row_rhs, names=row_name)
#     prob.solve()
#     """
#     print()
#     print(prob.solution.status[prob.solution.get_status()])
#     print('Solution value = ', prob.solution.get_objective_value())
#
#     numcols = prob.variables.get_num()
#     numrows = prob.linear_constraints.get_num()
#
#     slack = prob.solution.get_linear_slacks()
#     x = prob.solution.get_values()
#
#     """
#
#     for j in decision_name_link:
#         print('%10s: Value = %10f' %(j, prob.solution.get_values(j)) )
#
#
#
#     prob.write('prob.lp')
#
#     #reduce the bandwidth of link which has been mapped
#     mapped_dvars = [dvar for dvar in decision_name_link if prob.solution.get_values(dvar) == 1]
#     for dvar in mapped_dvars:
#         if 'meta' in dvar:
#             node_sn = None
#             node_vn = None
#             # a new sn node is mapped, so change the capacity of node in sn
#             if 'meta' == dvar.split('_')[1]:
#                 node_sn = int(dvar.split('_')[3])
#                 node_vn = int(dvar.split('_')[2])
#                 mapping_dic[node_vn] = node_sn
#                 print('map vn node %s to sn node %s' %(node_vn, node_sn))
#
#             if 'meta' == dvar.split('_')[2]:
#                 node_sn = int(dvar.split('_')[1])
#                 node_vn = int(dvar.split('_')[3])
#                 mapping_dic[node_vn] = node_sn
#                 print('map vn node %s to sn node %s' %(node_vn, node_sn))
#             print(sn.getNodePropertyBy(node_sn, 'capacity'))
#             c = sn.getNodePropertyBy(node_sn, 'capacity') - vn.getNodePropertyBy(node_vn, 'requirement')
#             sn.setNodeProperty(node_sn, c, 'capacity')
#             print('new')
#             print(sn.getNodePropertyBy(node_sn, 'capacity'))
#
#         else:
#             link = (int(dvar.split('_')[1]), int(dvar.split('_')[2]))
#             #cp = sn.getLinkPropertyBy(link, 'capacity')
#             sn.setLinkProperty(link,
#                                sn.getLinkPropertyBy(link, 'capacity')
#                                - vn.getLinkPropertyBy(edge, 'requirement'),
#                                'capacity')
#
#
#     print ('Mapping dictionary: \n%s' %mapping_dic)
#
#     print(mapped_dvars)
#     #todo: reduce the nodes' capacity after mapping







def vne_mapping(vn, sn):
    mapping_dic = {} #{vn_node : sn_node }
    for node in vn.nodes():
        mapping_dic[node] = None
    count = 0
    for edge in vn.edges():
        count = count + 1
        print( 'count: %s'  %count )
        print('########################################################################')

        src_node_vn = edge[0]
        dst_node_vn = edge[1]
        requirement_src_node_vn = vn.node[src_node_vn]['requirement']
        requirement_dst_node_vn = vn.node[dst_node_vn]['requirement']
        src_node_sn = None
        dst_node_sn = None

        print('Node: %s, requirement: %s' % (src_node_vn, requirement_src_node_vn))
        print('Node: %s, requirement: %s' % (dst_node_vn, requirement_dst_node_vn))
        print('bandwidth requirement: %s' % vn.getLinkPropertyBy(edge, 'requirement'))
        row = []
        row_rhs = []
        row_sense = []
        row_name = []

        argumentGraph = sn.copy()
        sn_tmp = sn.copy()

        if mapping_dic[src_node_vn] == None:
            argumentGraph =sn.addMetaNode(argumentGraph, vn, 'meta_' + str(src_node_vn))
            src_node_sn = 'meta_' + str(src_node_vn)
            #remove the link which the other node has not enough capacity in argument
            for n in argumentGraph.getNeighbors(src_node_sn):
                if argumentGraph.getNodePropertyBy(n, 'capacity') < vn.getNodePropertyBy(src_node_vn, 'requirement'):
                    print('SRC: not enough cpu capacity %s' %n)
                    print('remove edge %s - %s ' %(src_node_sn, n))
                    argumentGraph.removeEdge((src_node_sn, n))
        else:
            src_node_sn = mapping_dic[src_node_vn]
        if mapping_dic[dst_node_vn] == None:
            argumentGraph = sn.addMetaNode(argumentGraph, vn, 'meta_' + str(dst_node_vn))
            #remove the links which the other node has not enough capacity in argument nentwork
            dst_node_sn = 'meta_' + str(dst_node_vn)
            for n in argumentGraph.getNeighbors(dst_node_sn):
                if argumentGraph.getNodePropertyBy(n, 'capacity') < vn.getNodePropertyBy(dst_node_vn, 'requirement'):
                    print('DST: not enough cpu capacity')
                    print('remove edge %s - %s ' %(dst_node_sn, n))
                    argumentGraph.removeEdge((dst_node_sn, n))

        else:
            dst_node_sn = mapping_dic[dst_node_vn]
        #todo: remove? the nodes that have not enough capacity in argument network
        #remove the links that have not enough capacity in argument network
        for e in argumentGraph.edges():
            if argumentGraph.getLinkPropertyBy(e, 'capacity') < vn.getLinkPropertyBy(edge, 'requirement'):
                print('Remove edge in argument network %s - %s' %(e[0], e[1]))
                print('not enough bandwidth capacity')
                argumentGraph.removeEdge(e)


        # Construct constraints
        src_constraints = constructSourceNodeConstraints(argumentGraph, src_node_sn)
        dst_constraints = constructDestinationNodeConstraints(argumentGraph, dst_node_sn)

        appendFlowConstraint(src_constraints, row, row_rhs, row_sense, row_name)
        appendFlowConstraint(dst_constraints, row, row_rhs, row_sense, row_name)

        decision_name_link = generateLinkDecisionVariable(vn, argumentGraph)
        obj_cost = [ 1 for i in range(0, len(decision_name_link )) ]

        btype = 'B' * len(decision_name_link)

        for node in argumentGraph.nodes():
            if node != src_node_sn and node != dst_node_sn:
                #print(node)
                row_tuple = constructNodeConstraints(argumentGraph, node, 0, 'node_'+ str(node))
                appendFlowConstraint(row_tuple, row, row_rhs, row_sense, row_name)

        prob = cplex.Cplex()
        prob.objective.set_sense(prob.objective.sense.minimize)
        prob.variables.add(obj=obj_cost, types=btype,names = decision_name_link)
        prob.linear_constraints.add(lin_expr = row, senses=''.join(row_sense),rhs=row_rhs, names=row_name)
        try:
            prob.solve()
        except:
            print("not solution, exit")
            exit(1)
        """
        print()
        print(prob.solution.status[prob.solution.get_status()])
        print('Solution value = ', prob.solution.get_objective_value())

        numcols = prob.variables.get_num()
        numrows = prob.linear_constraints.get_num()

        slack = prob.solution.get_linear_slacks()
        x = prob.solution.get_values()


        for j in decision_name_link:
            print('%10s: Value = %10f' %(j, prob.solution.get_values(j)) )


        """

        prob.write('prob.lp')

        #reduce the bandwidth of link which has been mapped
        mapped_dvars = [dvar for dvar in decision_name_link
                        if prob.solution.get_values(dvar) == 1]
        for dvar in mapped_dvars:
            if 'meta' in dvar:
                node_sn = None
                node_vn = None
                # a new sn node is mapped, so change the capacity of node in sn
                if 'meta' == dvar.split('_')[1]:
                    node_sn = int(dvar.split('_')[3])
                    node_vn = int(dvar.split('_')[2])
                    mapping_dic[node_vn] = node_sn
                    print('map vn node %s to sn node %s' %(node_vn, node_sn))

                if 'meta' == dvar.split('_')[2]:
                    node_sn = int(dvar.split('_')[1])
                    node_vn = int(dvar.split('_')[3])
                    mapping_dic[node_vn] = node_sn
                    print('map vn node %s to sn node %s' %(node_vn, node_sn))
                c = sn.getNodePropertyBy(node_sn, 'capacity') \
                    - vn.getNodePropertyBy(node_vn, 'requirement')
                sn.setNodeProperty(node_sn, c, 'capacity')

            else:
                link = (int(dvar.split('_')[1]), int(dvar.split('_')[2]))
                #cp = sn.getLinkPropertyBy(link, 'capacity')
                sn.setLinkProperty(link,
                                   sn.getLinkPropertyBy(link, 'capacity')
                                   - vn.getLinkPropertyBy(edge, 'requirement'),
                                   'capacity')


        print ('Mapping dictionary: \n%s' %mapping_dic)
        print(mapped_dvars)
        #todo: reduce the nodes' capacity after mapping


#vne_mapping(vn, sn)
count = 0
while True:
    vn = VirtualNetwork()
    isConnected = vn.createNetwork(8, 0.5)
    while not isConnected:
        isConnected = vn.createNetwork(8, 0.5)
    vn.setBandwidthRequirement(1, 50)
    vn.setCpuRequirement(1, 50)
    try:
        vne_mapping(vn, sn)
        count = count + 1
    except:
        print("no solution exit.....")
        print('total number of vn mapped: %s' %count)
        exit(1)



# vn = VirtualNetwork()
# isConnected = vn.createNetwork(4, 0.5)
# while not isConnected:
#     isConnected = vn.createNetwork(4, 0.5)
# vn.setBandwidthRequirement(1, 50)
# vn.setCpuRequirement(1, 50)
#
# vne_mapping(vn, sn)
# vn = VirtualNetwork()
# isConnected = vn.createNetwork(4, 0.5)
# while not isConnected:
#     isConnected = vn.createNetwork(4, 0.5)
# vn.setBandwidthRequirement(1, 50)
# vn.setCpuRequirement(1, 50)
#
# vne_mapping(vn, sn)






### CPLEX solve ###
"""
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
"""

