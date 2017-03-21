import networkx as nx
import random
from itertools import islice


class NetworkBase(nx.Graph):
    SUBSTRATE = 0
    VIRTUAL = 1

    def __init__(self):
        nx.Graph.__init__(self)

    def createNetwork(self, nbNodes = None, prb = None):
        if nbNodes == None or prb == None:
            #todo: handle other situations
            pass
        else:
            self.add_nodes_from(nx.erdos_renyi_graph(nbNodes, prb).nodes())
            self.add_edges_from(nx.erdos_renyi_graph(nbNodes, prb).edges())
        if not nx.is_connected(self):
            print('network is not connected')
            return False
        else:
            print('network is connected')
            return True
    def _setNetworkType(self, nType):
        """
        Set network Type
        :param nType: network type. SUBSTRATE or VIRTUAL
        :return: the network type set
        """
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

    def getAllPath(self, srcNode, dstNode):
        if nx.has_path(self, srcNode,dstNode):
            return nx.all_simple_paths(self, srcNode,dstNode)
        else:
            return None

    def getShortestPath(self, srcNode, dstNode):
        return nx.shortest_path(self, srcNode, dstNode)

    def getKShortestPaths(self, srcNode, dstNode, k):
        if nx.has_path(self, srcNode,dstNode):
            return list(islice(nx.shortest_simple_paths(self, srcNode, dstNode), k))
        else:
            return None
    def getLinkPropertyBy(self, e,  property):
        return self.edge[e[0]][e[1]][property]
    def getNodePropertyBy(self, n, property):
        return self.node[n][property]
