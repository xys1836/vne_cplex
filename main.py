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

substrateNetworkData = SubstrateNetworkData()
substrateNetworkData.nbNodesOfSubstrateNetwork = 100
substrateNetworkData.ctnProbability = 0.5
substrateNetworkData.lbOfBandwidthCapacity = 50
substrateNetworkData.ubOfBandwidthCapacity = 100
substrateNetworkData.lbOfCpuCapacity = 50
substrateNetworkData.ubOfCpuCapacity = 100

sn = SubstrateNetwork(substrateNetworkData.nbNodesOfSubstrateNetwork, substrateNetworkData.ctnProbability)
sn.setCpuCapacity(substrateNetworkData.lbOfCpuCapacity, substrateNetworkData.ubOfCpuCapacity)
sn.setBandwidthCapacity(substrateNetworkData.lbOfBandwidthCapacity, substrateNetworkData.ubOfBandwidthCapacity)




print sn.nodes()
print sn.edges()
for n in sn.nodes():
    print sn.node[n]['capacity']

