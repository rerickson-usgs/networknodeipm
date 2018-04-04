import unittest
import numpy as np
import scipy.stats as stats
import sys 
sys.path.append("../modelFiles")
import networkModelPopulate as nmp
import nodeHarvest as nH
import pandas as pd 


class test_nodeHarvest( unittest.TestCase):

    def testHarvestUniform( self):
        '''
        Tests a uniform harvest input
        '''
        class popNodeHarvest( nH.nodeHarvest, nmp.populatedNode):
            pass

        nYears = 10
        nPoints = 5
        harvest = np.ones(nYears) * 0.5
        nodeTest1 = popNodeHarvest("test node 1")
        nodeTest1.setHarvest( harvest )

        self.assertEqual( nodeTest1.showNodeHarvest()[2] , harvest[2]) 
        self.assertEqual( nodeTest1.showNodeHarvestYear(9), harvest[9])

        group = nmp.group('test group')
        group.createPopDist( nYears = nYears,
                             nPoints = nPoints,
                             popDist0 = np.ones( nPoints))

        nodeTest1.addGroups( [group])
        nodeTest1.nodeHarvest( year = 0)

        self.assertEqual( nodeTest1.groups[0].showPopDistYear(0).sum(), 2.5)

    def testHarvestNonUniform( self):
        '''
        Tests a uniform harvest input
        '''
        class popNodeHarvest( nH.nodeHarvest, nmp.populatedNode):
            pass

        nYears = 10
        harvest  = np.array([ [0.0, 0.1, 0.5, 0.9, 1.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
        nPoints = harvest.shape[1]
        nodeTest1 = popNodeHarvest("test node 1")
        nodeTest1.setHarvest( harvest )

        self.assertEqual( nodeTest1.showNodeHarvest()[1 ,2] , harvest[1, 2])
        self.assertTrue( all(nodeTest1.showNodeHarvestYear(0) == harvest[ 0, :]))

        group = nmp.group('test group')
        group.createPopDist( nYears = nYears,
                             nPoints = nPoints,
                             popDist0 = np.ones( nPoints))

        nodeTest1.addGroups( [group])
        nodeTest1.nodeHarvest( year = 0)
        self.assertEqual( nodeTest1.groups[0].showPopDistYear(0).sum(), 3.5)

        
        
class test_addNodeHarvestCSV( unittest.TestCase):

    def testAddFunction( self):
        inputFolder = "../inputParameters/"
        harvestFile = inputFolder + 'nodeHarvestTestSingle.csv'
        dfHarvest = pd.read_csv( harvestFile)

        networkFile = inputFolder + 'twoNodeTestNetwork.csv'
        dfNetwork = pd.read_csv(networkFile)

        nodeFile = inputFolder + 'twoNodeTestNodes.csv'
        dfNode = pd.read_csv(nodeFile)

        class popNodeWithHarvestCSV( nH.addNodeHarvestCSV, nmp.createNetworkFromCSV):
            pass

        class popNodeWithHarvest( nH.nodeHarvest, nmp.populatedNode):
            pass
        
        createNetwork = popNodeWithHarvestCSV( dfNetwork)
        createNetwork.addNodesFromCSV( dfNode, popNodeWithHarvest)
        createNetwork.addHarvestIntoNodes( dfHarvest)

    
        network = createNetwork.showNetwork()
        self.assertEqual(network.nodes[0].showNodeHarvest()[3], 0.5)
        self.assertEqual(network.nodes[1].showNodeHarvest()[3], 0.0)

    def testAddFunctionWithMutipleInputs( self):
        inputFolder = "../inputParameters/"
        harvestFile = inputFolder + 'nodeHarvestTestMultiple.csv'
        dfHarvest = pd.read_csv( harvestFile)

        networkFile = inputFolder + 'twoNodeTestNetwork.csv'
        dfNetwork = pd.read_csv(networkFile)

        nodeFile = inputFolder + 'twoNodeTestNodes.csv'
        dfNode = pd.read_csv(nodeFile)

        class popNodeWithHarvestCSV( nH.addNodeHarvestCSV, nmp.createNetworkFromCSV):
            pass

        class popNodeWithHarvest( nH.nodeHarvest, nmp.populatedNode):
            pass
        
        createNetwork = popNodeWithHarvestCSV( dfNetwork)
        createNetwork.addNodesFromCSV( dfNode, popNodeWithHarvest)
        createNetwork.addHarvestIntoNodes( dfHarvest)
    
        network = createNetwork.showNetwork()
        self.assertEqual(network.nodes[0].showNodeHarvest()[1], 0.0)
        self.assertEqual(network.nodes[0].showNodeHarvest()[2], 0.5)
        self.assertEqual(network.nodes[0].showNodeHarvest()[5], 0.0)


        self.assertEqual(network.nodes[1].showNodeHarvest()[0], 0.0)
        self.assertEqual(network.nodes[1].showNodeHarvest()[1], 0.75)
        self.assertEqual(network.nodes[1].showNodeHarvest()[3], 0.0)
        
if __name__ == '__main__':
    unittest.main()
