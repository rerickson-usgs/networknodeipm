import sys
sys.path.append("../modelFiles")
import networkModelPopulate as nmp
import networkModelPopulateSex as nmps
import networkModelPopulateSterileMale as nmpsm
import networkModelTimePeriods as nmtp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


'''
Run lake scnearios with sterile male stocking
'''

scnName  = "lake" 
scnNumber= "Scn_1"
scnNetworkSetup = "Scn_0"

inputFolder = "./inputParameters/"
outputFolder = "./modelOutputs/"


groupsFile = inputFolder + scnName + "_groups_" + scnNumber +'.csv'
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + scnName + '_Nodes_' + scnNetworkSetup + '.csv'
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + scnName +'_Network_' + scnNetworkSetup +'.csv'
dfNetwork = pd.read_csv(networkFile)

class networkUse( nmtp.networkWithTimePeriod,
                  nmp.populatedNetwork):
    pass


class nodeUse( nmtp.nodeTimePeriod,
               nmpsm.populatedNodeWithSexSterileMale):
    pass


class createNetworkUse(nmtp.createNetworkFromCSVwithTime,
                       nmpsm.createNetworkFromCSVwithSterileMale):
    pass

dir(createNetworkUse)
createNetwork = createNetworkUse(dfNetwork, networkUse)

createNetwork.addNodesFromCSV( dfNode, nodeUse)
createNetwork.addTimePeriodToNodes( dfNode)

createNetwork.addGroupSterileMaleFromCSV( dfGroups, nmpsm.groupWithSexSterileMale)
createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath)

network = createNetwork.showNetwork()
network.runSimulation()
network.calculateNetworkPop()
print network.showNetworkPop()

network.plotAllNodes(saveData = outputFolder + "out_" + scnName + "_" + scnNumber +  ".csv", showGroups = True)
network.saveGroupData(saveGroupFile = outputFolder + "groups_" + scnName + "_" + scnNumber +  ".csv")

print("Done")



