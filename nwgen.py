from networkbase import NetworkBase

class SubstrateNetwork(NetworkBase):

    def __init__(self, nbNodes=None, prb=None):
        NetworkBase.__init__(self, nbNodes, prb)
        self.setNetworkType(NetworkBase.SUBSTRATE)

    def setBandwidthCapacity(self, lb, ub):
        """
        Set bandwidth capacity of substrate network randomly.

        :param lb: the low bound of bandwidth capacity
        :param ub: the up bound of bandwidth capacity
        :return: none
        """
        self._setEdgesProperty(lb, ub, "capacity")

    def setBandwidthCost(self, cost):
        self._setEdgesProperty(cost, cost,'cost')

    def setCpuCapacity(self, lb, ub):
        self._setNodesProperty(lb, ub, "capacity")


class VirtualNetwork(NetworkBase):
    #virtual Network Class
    def __init__(self, nbNodes=None, prb=None):
        NetworkBase.__init__(self, nbNodes, prb)
        self.setNetworkType(NetworkBase.VIRTUAL)

    def setBandwidthRequirement(self, lb, ub):
        self._setEdgesProperty(lb, ub, "requirement")
    def setCpuRequirement(self, lb, ub, property):
        self._setNodesProperty(lb, ub, "requirement")


