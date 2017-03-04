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
substrateNetworkData.nbNodesOfSubstrateNetwork = 100
substrateNetworkData.ctnProbability = 0.5
substrateNetworkData.lbOfBandwidthCapacity = 100
substrateNetworkData.ubOfBandwidthCapacity = 100
substrateNetworkData.lbOfCpuCapacity = 100
substrateNetworkData.ubOfCpuCapacity = 100

sn = SubstrateNetwork( substrateNetworkData.nbNodesOfSubstrateNetwork, substrateNetworkData.ctnProbability)

sn.setCpuCapacity( substrateNetworkData.lbOfCpuCapacity, substrateNetworkData.ubOfCpuCapacity )
sn.setBandwidthCapacity( substrateNetworkData.lbOfBandwidthCapacity, substrateNetworkData.ubOfBandwidthCapacity )
sn.setBandwidthCost(20)

prob = cplex.Cplex()
prob.objective.set_sense(prob.objective.sense.minimize)

