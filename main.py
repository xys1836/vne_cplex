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
substrateNetworkData.nbNodesOfSubstrateNetwork = 20
substrateNetworkData.ctnProbability = 0.5
substrateNetworkData.lbOfBandwidthCapacity = 100
substrateNetworkData.ubOfBandwidthCapacity = 100
substrateNetworkData.lbOfCpuCapacity = 100
substrateNetworkData.ubOfCpuCapacity = 100

sn = SubstrateNetwork( substrateNetworkData.nbNodesOfSubstrateNetwork, substrateNetworkData.ctnProbability)

sn.setCpuCapacity( substrateNetworkData.lbOfCpuCapacity, substrateNetworkData.ubOfCpuCapacity )
sn.setBandwidthCapacity( substrateNetworkData.lbOfBandwidthCapacity, substrateNetworkData.ubOfBandwidthCapacity )
sn.setBandwidthCost(20)

vn = VirtualNetwork(5, 0.5)
vn.setBandwidthRequirement(1, 50)
vn.setCpuRequirement(1, 50)
print vn.number_of_nodes()



def generateNodeDecisionVariable(vn, sn):
    dv = []
    for i in range(0, vn.number_of_nodes()):
        for j in range(0, sn.number_of_nodes()):
            dv.append('Xv' + str(i) + 's' + str(j))
    return dv
def generateLinkDecisionVariable(vn, sn):
    dv = []
    
print generateNodeDecisionVariable(vn, sn)

prob = cplex.Cplex()
prob.objective.set_sense(prob.objective.sense.minimize)



