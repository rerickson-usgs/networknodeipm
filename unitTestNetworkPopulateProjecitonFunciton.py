import unittest
import numpy as np
import scipy.stats as stats
import networkModelPopulate as nmp
import pandas as pd

class test_csvPopulateNoGrowth( unittest.TestCase):

    def test_networkCreation(self):
        ## Load files 
        inputFolder = "./inputParameters/"
        groupsFile = inputFolder + 'twoNodeTestGroupsNoBD.csv'
        dfGroups = pd.read_csv(groupsFile)
        
        nodeFile = inputFolder + 'twoNodeTestNodes.csv'
        dfNode = pd.read_csv(nodeFile)
        
        networkFile = inputFolder + 'twoNodeTestNetwork.csv'
        dfNetwork = pd.read_csv(networkFile)
        
        ## Test creation of network 
        createNetwork = nmp.createNetworkFromCSV( dfNetwork)

        ## Test addition of nodes
        createNetwork.addNodesFromCSV( dfNode)

        ## Test addition of groups 
        createNetwork.addGroupsFromCSV( dfGroups)
        
        ## Export and test network 
        network = createNetwork.showNetwork()
        
        self.assertEqual( network.nodes[0].groups[0].eggTransition,  0.0) 

        network.runSimulation()
        network.calculateNetworkPop()
        self.assertAlmostEqual(network.nodes[1].showNodePopulation()[25], 3000) 
        self.assertAlmostEqual(network.nodes[0].showNodePopulation()[25], 3000) 
if __name__ == '__main__':
    unittest.main()
