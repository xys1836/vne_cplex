from networkbase import NetworkBase

class SubstrateNetwork(NetworkBase):

    def __init__(self):
        NetworkBase.__init__(self)
        self._setNetworkType(NetworkBase.SUBSTRATE)


    def setBandwidthCapacity(self, lb, ub):
        """
        Set bandwidth capacity of substrate network randomly.

        :param lb: the low bound of bandwidth capacity
        :param ub: the up bound of bandwidth capacity
        :return: none
        """
        self._setEdgesPropertyRandomly(lb, ub, "capacity")

    def setBandwidthCost(self, lb, ub):
        self._setEdgesPropertyRandomly(lb, ub, 'cost')

    def setCpuCapacity(self, lb, ub):
        self._setNodesPropertyRandomly(lb, ub, "capacity")

    def setCpuCost(self, lb, ub):
        self._setNodesPropertyRandomly(lb, ub, 'cost')

    def createArgumentGraph(self, vn):
        """Create an argument graph with meta nodes.
        :param times: how many times of nodes in sn is than that in vn.
                        for example, if sn includes 8 nodes and vnn includes 4 nodes, then
                        times = 2
        :return:  an argument graph with meta nodes

        """
        """
        argument_graph = self.copy()
        num_nodes_sn = self.number_of_nodes()
        num_nodes_vn = vn.number_of_nodes()

        for i in range(0, num_nodes_sn):
            meta_node = 'meta_' + str(i % num_nodes_vn)
            argument_graph.add_edge(i, meta_node, {'capacity': float('inf')})

        """
        argument_graph = self.copy()
        num_areas = vn.number_of_nodes()
        for i in range(0, num_areas ):
            self.addMetaNode(argument_graph, vn, 'meta_'+str(i))
        return argument_graph

    def addMetaNode(self, argument_graph, vn, metaNode):
        num_nodes_vn = vn.number_of_nodes()
        num_nodes_sn = self.number_of_nodes()
        node_num = None
        try:
            node_num = int(metaNode.split('_')[1])

        except:
            print('not a valid meta Node name, x is not a number or format is not correct')
            print('rename the metaNode with name like "meta_x" where x is not larger than number of virtual network edges')
            exit(1)
        if node_num > num_nodes_vn - 1:
            print('not a valid meta Node name, x is larger than number of virtual network links')
            print('rename the metaNode with name like "meta_x" where x is not larger than number of virtual network edges')
            exit(1)
        if argument_graph == None:
            #argument_graph = self.copy()
            print('argument graph cannot be None')
            exit(1)
        t = num_nodes_vn * node_num
        num_nodes_area = (num_nodes_sn + num_nodes_sn % num_nodes_vn)/num_nodes_vn #number of nodes in one area

        d = node_num * num_nodes_area

        if d + num_nodes_area <= num_nodes_sn:
            for i in range(d, d + num_nodes_area ):
                print('add a new edge %s - %s' %(i, metaNode))
                argument_graph.add_edge(i, metaNode, {'capacity': float('inf')})
        else:
            for i in range(d, num_nodes_sn ):
                print('add a new edge %s - %s' %(i, metaNode))
                argument_graph.add_edge(i, metaNode, {'capacity': float('inf')})
        return argument_graph

    def getNeighbors(self, n):
        return self.neighbors(n)

    def removeNode(self, n):
        self.remove_node(n)

    def removeEdge(self, e):
        self.remove_edge(e[0], e[1])
    def removeLink(self, e):
        self.remove_edge(e[0], e[1])
    def setLinkProperty(self, e, b, p):
        """
        set Link property
        :param e:  the edge or link
        :param b:  the value of property (say bandwidth capacity)
        :param p:  the name of property (say capacity or cost)
        :return:
        """
        self.edge[e[0]][e[1]]['capacity'] = b
    def setNodeProperty(self, n, c, p):
        """
        set node property
        :param n:  name of the node
        :param c:  value of property
        :param p:  name of property
        :return:  None
        """
        self.node[n][p] = c

class VirtualNetwork(NetworkBase):
    #virtual Network Class
    def __init__(self):
        NetworkBase.__init__(self)
        self._setNetworkType(NetworkBase.VIRTUAL)

    def setBandwidthRequirement(self, lb, ub):
        self._setEdgesPropertyRandomly(lb, ub, "requirement")
    def setCpuRequirement(self, lb, ub):
        self._setNodesPropertyRandomly(lb, ub, "requirement")
    def printOutInfo(self):
        #todo: write a method to print out network info
        pass
    def setName(self, name):
        self.name = name

