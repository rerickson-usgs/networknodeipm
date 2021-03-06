import sys
sys.path.append("../modelFiles")
import networkModelPopulate as nmp
import networkModelPopulateSex as nmps
import networkModelPopulateSterileMale as nmpsm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
''' 
Ths file tests functions that do now work with unit testing
such as plots and print to screen functions 
'''

## Read in CSV files and create network 
inputFolder = "../inputParameters/"
groupsFile = inputFolder + 'twoNodeTestGroupsSterileMales.csv'
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + 'twoNodeTestNodes.csv'
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + 'twoNodeTestNetworkYY.csv'
dfNetwork = pd.read_csv(networkFile)

createNetwork = nmpsm.createNetworkFromCSVwithSterileMale( dfNetwork)
createNetwork.addNodesFromCSV( dfNode, nodeIn = nmpsm.populatedNodeWithSexSterileMale)
createNetwork.addGroupSterileMaleFromCSV( dfGroups, groupInIn = nmpsm.groupWithSexSterileMale)

network = createNetwork.showNetwork()
network.selfPopulatePaths()
network.describeNetwork()


groupsPop = np.array([grp.showPopYear(0) for grp in network.nodes[0].groups])
groupsMale = [grp.showSex() == 'male'  for grp in network.nodes[0].groups]
groupsMale
groupsPop[groupsMale]
## Check simulate network here 
network.runSimulation()
        
# # ## Check plot 
network.calculateNetworkPop()
network.plotAllNodes(showGroups = True)


network.nodes[0].groups[2].showPop()
network.nodes[1].groups[2].showPop()

network.nodes[0].groups[1].showPop()
network.nodes[0].groups[0].showPop()
