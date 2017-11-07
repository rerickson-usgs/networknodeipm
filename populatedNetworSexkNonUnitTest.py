import networkModelPopulate as nmp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
''' 
Ths file tests functions that do now work with unit testing
such as plots and print to screen functions 
'''


## Read in CSV files and create network 
inputFolder = "./inputParameters/"
groupsFile = inputFolder + 'twoNodeTestGroupsSex.csv'
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + 'twoNodeTestNodesSex.csv'
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + 'twoNodeTestNetworkSex.csv'
dfNetwork = pd.read_csv(networkFile)


### Temp test code
dfGroupUse = dfGroups.query(
    str( 'network == "twoNodeNetwork" &  node == "node 1" &  groupName == "test group 1 male" '))


grp.addSex( dfGroupUse[1]['groupSex'] ) ## check this line and next
grp.addRecruitmentGroup( dfGroupUse[1]['recruitmentGroup'] )
 
dfGroupUse[1]['groupSex']

### AM HERE EDITING CODE 
createNetwork = nmp.createNetworkFromCSV( dfNetwork)
createNetwork.addNodesFromCSV( dfNode)
createNetwork.addGroupsFromCSV( dfGroups)

network = createNetwork.showNetwork()
network.selfPopulatePaths()
## Check describe network function
network.describeNetwork()

## Check simulate network here 
network.runSimulation()
        
# ## Check plot 
network.calculateNetworkPop()
print network.showNetworkPop()
network.plotAllNodes()



