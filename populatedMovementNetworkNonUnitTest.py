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
groupsFile = inputFolder + 'twoNodeTestGroupsMovement.csv'
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + 'twoNodeTestNodes.csv'
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + 'twoNodeTestNetwork.csv'
dfNetwork = pd.read_csv(networkFile)

createNetwork = nmp.createNetworkFromCSV( dfNetwork)
createNetwork.addNodesFromCSV( dfNode)
createNetwork.addGroupsFromCSV( dfGroups)

network = createNetwork.showNetwork()

## Check describe network function
network.describeNetwork()

print "self pop paths"
network.selfPopulatePaths()

# ## Check simulate network here 
network.runSimulation()
        
# # ## Check plot 
network.calculateNetworkPop()
print network.showNetworkPop()
network.plotAllNodes()



