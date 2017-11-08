import networkModelPopulate as nmp
import networkModelPopulateSex as nmps
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

nodeFile = inputFolder + 'twoNodeTestNodes.csv'
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + 'twoNodeTestNetwork.csv'
dfNetwork = pd.read_csv(networkFile)

createNetwork = nmps.createNetworkFromCSVwithSex( dfNetwork)
createNetwork.addNodesFromCSV( dfNode, nodeIn = nmps.populatedNodeWithSex)
createNetwork.addGroupSexFromCSV( dfGroups, groupInIn = nmps.groupWithSex)

network = createNetwork.showNetwork()
network.selfPopulatePaths()
if 'stocking' in dfGroups.columns:
    print "yes"
## Check describe network function
network.describeNetwork()

## Check simulate network here 
network.runSimulation()
        
# ## Check plot 
network.calculateNetworkPop()
# print network.showNetworkPop()
network.plotAllNodes(showGroups = True)



