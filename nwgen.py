import networkx as nx
import random

class NetworkBase(nx.Graph):
    SUBSTRATE = 0
    VIRTUAL = 1

    def __init__(self, nbNodes = None, prb = None):
        nx.Graph.__init__(self)
        if nbNodes == None or prb == None:
            #todo: handle other situation
            pass
        else:
            self.add_nodes_from(nx.erdos_renyi_graph(nbNodes, prb).nodes())
            self.add_edges_from(nx.erdos_renyi_graph(nbNodes, prb).edges())

    def setNetworkType(self, nType):
        if nType == NetworkBase.SUBSTRATE or nType == NetworkBase.VIRTUAL:
            self.network_type = nType
        else:
            print "Network Type Error"
        return nType

    def _setEdgesProperty(self, lb, ub, propertyName="capacity"):
        if ub < lb:
            print "Error: Set edges property failed: up bound is lower than lower bound"
            exit(1)
        for e in self.edges():
            self.edge[e[0]][e[1]][propertyName] = random.randint(lb, ub)

    def _setNodesProperty(self, lb, ub, propertyName="capacity"):
        if ub < lb:
            print "Error: Set node property failed: up bound is lower than lower bound"
        for n in self.nodes():
            self.node[n][propertyName] = random.randint(lb, ub)

class SubstrateNetwork(NetworkBase):

    def __init__(self, nbNodes=None, prb=None):
        NetworkBase.__init__(self, nbNodes, prb)
        self.setNetworkType(NetworkBase.SUBSTRATE)

    def setBandwidthCapacity(self, lb, ub):
        self._setEdgesProperty(lb, ub, "capacity")
    def setCpuCapacity(self, lb, ub):
        self._setNodesProperty(lb, ub, "capacity")


class VirtualNetwork(NetworkBase):

    def __init__(self, nbNodes=None, prb=None):
        NetworkBase.__init__(self, nbNodes, prb)
        self.setNetworkType(NetworkBase.VIRTUAL)

    def setBandwidthRequirement(self, lb, ub):
        self._setEdgesProperty(lb, ub, "requirement")
    def setCpuRequirement(self, lb, ub, property):
        self._setNodesProperty(lb, ub, "requirement")


