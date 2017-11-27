import unittest
import numpy as np
import scipy.stats as stats
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

class test_addNodeHarvestCSV( unittest.TestCase):

    def testAddFunction( self):
        inputFolder = "./inputParameters/"
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
        inputFolder = "./inputParameters/"
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



        self.assertFalse(False)
# class testMovementRun( unittest.TestCase):
#     def testRunSim( self):

#         ## Load files 
#         inputFolder = "./inputParameters/"
#         groupsFile = inputFolder + 'threeNodeTestGroupsTimePeriodsNoBD.csv'
#         dfGroups = pd.read_csv(groupsFile)
        
#         nodeFile = inputFolder + 'threeNodeTestNodesTimePeriods.csv'
#         dfNode = pd.read_csv(nodeFile)
        
#         networkFile = inputFolder + 'threeNodeTestNetworkTimePeriods.csv'
#         dfNetwork = pd.read_csv(networkFile)

#         class populatedNetworkWithTimePeriods(nmtp.networkWithTimePeriod,
#                                               nmp.populatedNetwork):
#             def __init__(self, networkName):
#                 self.networkName = networkName
#                 self.nodes = []
#                 self.paths = []
#                 self.timePeriods = []

#         ## Test creation of network 
#         createNetwork = nmtp.createNetworkFromCSVwithTime(
#             dfNetwork, populatedNetworkWithTimePeriods)

#         ## Test addition of nodes
#         class populatedNodeTimePeriod( nmtp.nodeTimePeriod,
#                                        nmp.populatedNode):
#             def __init__(self, nodeName):
#                 self.nodeName = nodeName
#                 self.groups = []
#                 self.pathsIn = []
#                 self.pathsOut = {}
        
#         createNetwork.addNodesFromCSV( dfNode, populatedNodeTimePeriod)
#         createNetwork.addTimePeriodToNodes( dfNode)
        
#         ## Test addition of groups 
#         createNetwork.addGroupsFromCSV( dfGroups, groupIn = nmp.group)

#         ## Add in paths with timePeriod 
#         createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath)
        
#         ## Export and test network 
#         network = createNetwork.showNetwork()
#         self.assertEqual( network.showTimePeriods(), ['summer', 'fall', 'winter'])
#         self.assertEqual( network.nodes[0].showTimePeriod(), 'summer')

#         ## Test movement within network 


#         network.calculateNetworkPop()
#         self.assertAlmostEqual( network.nodes[0].showNodePopulation()[0], 000)
#         self.assertAlmostEqual( network.nodes[1].showNodePopulation()[0], 0)
#         self.assertAlmostEqual( network.nodes[2].showNodePopulation()[0], 3000)
        
#         for tp in network.showTimePeriods():
#             network.moveGroups( 1, 1, tp)

#         network.calculateNetworkPop()
#         self.assertAlmostEqual( network.nodes[0].showNodePopulation()[1], 3000)
#         self.assertAlmostEqual( network.nodes[1].showNodePopulation()[1], 3000)
#         self.assertAlmostEqual( network.nodes[2].showNodePopulation()[1], 3000)

#         self.assertAlmostEqual( network.nodes[0].showNodePopulation()[0], 0.0)
#         self.assertAlmostEqual( network.nodes[1].showNodePopulation()[0], 0.0)
#         self.assertAlmostEqual( network.nodes[2].showNodePopulation()[0], 3000.0)


# class testSimulationRun( unittest.TestCase):
#     ''' 
#     test run without births or death
#     '''
#     def testRunSim( self):

#         ## Load files 
#         inputFolder = "./inputParameters/"
#         groupsFile = inputFolder + 'threeNodeTestGroupsTimePeriodsNoBD.csv'
#         dfGroups = pd.read_csv(groupsFile)
        
#         nodeFile = inputFolder + 'threeNodeTestNodesTimePeriods.csv'
#         dfNode = pd.read_csv(nodeFile)
        
#         networkFile = inputFolder + 'threeNodeTestNetworkTimePeriods.csv'
#         dfNetwork = pd.read_csv(networkFile)

#         class populatedNetworkWithTimePeriods(nmtp.networkWithTimePeriod,
#                                               nmp.populatedNetwork):
#             def __init__(self, networkName):
#                 self.networkName = networkName
#                 self.nodes = []
#                 self.paths = []
#                 self.timePeriods = []

#         ## Test creation of network 
#         createNetwork = nmtp.createNetworkFromCSVwithTime(
#             dfNetwork, populatedNetworkWithTimePeriods)

#         ## Test addition of nodes
#         class populatedNodeTimePeriod( nmtp.nodeTimePeriod,
#                                        nmp.populatedNode):
#             def __init__(self, nodeName):
#                 self.nodeName = nodeName
#                 self.groups = []
#                 self.pathsIn = []
#                 self.pathsOut = {}
        
#         createNetwork.addNodesFromCSV( dfNode, populatedNodeTimePeriod)
#         createNetwork.addTimePeriodToNodes( dfNode)
        
#         ## Test addition of groups 
#         createNetwork.addGroupsFromCSV( dfGroups, groupIn = nmp.group)

#         ## Add in paths with timePeriod 
#         createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath)
        
#         ## Export and test network 
#         network = createNetwork.showNetwork()
#         self.assertEqual( network.showTimePeriods(), ['summer', 'fall', 'winter'])
#         self.assertEqual( network.nodes[0].showTimePeriod(), 'summer')

#         network.runSimulation()
#         network.calculateNetworkPop()
            
#         self.assertAlmostEqual( network.nodes[0].showNodePopulation()[25], 000.0)
#         self.assertAlmostEqual( network.nodes[1].showNodePopulation()[25], 000.0)
#         self.assertAlmostEqual( network.nodes[2].showNodePopulation()[25], 000.0)

#         self.assertAlmostEqual( network.nodes[0].showNodePopulation()[24], 3000.0)
#         self.assertAlmostEqual( network.nodes[1].showNodePopulation()[24], 3000.0)
#         self.assertAlmostEqual( network.nodes[2].showNodePopulation()[24], 3000.0)


# class testSimulationRunWithDeath( unittest.TestCase):
#     def testRunSim( self):

#         ## Load files 
#         inputFolder = "./inputParameters/"
#         groupsFile = inputFolder + 'threeNodeTestGroupsTimePeriodsNoB.csv'
#         dfGroups = pd.read_csv(groupsFile)
        
#         nodeFile = inputFolder + 'threeNodeTestNodesTimePeriods.csv'
#         dfNode = pd.read_csv(nodeFile)
        
#         networkFile = inputFolder + 'threeNodeTestNetworkTimePeriods.csv'
#         dfNetwork = pd.read_csv(networkFile)

#         class populatedNetworkWithTimePeriods(nmtp.networkWithTimePeriod,
#                                               nmp.populatedNetwork):
#             def __init__(self, networkName):
#                 self.networkName = networkName
#                 self.nodes = []
#                 self.paths = []
#                 self.timePeriods = []

#         ## Test creation of network 
#         createNetwork = nmtp.createNetworkFromCSVwithTime(
#             dfNetwork, populatedNetworkWithTimePeriods)

#         ## Test addition of nodes
#         class populatedNodeTimePeriod( nmtp.nodeTimePeriod,
#                                        nmp.populatedNode):
#             def __init__(self, nodeName):
#                 self.nodeName = nodeName
#                 self.groups = []
#                 self.pathsIn = []
#                 self.pathsOut = {}
        
#         createNetwork.addNodesFromCSV( dfNode, populatedNodeTimePeriod)
#         createNetwork.addTimePeriodToNodes( dfNode)
        
#         ## Test addition of groups 
#         createNetwork.addGroupsFromCSV( dfGroups, groupIn = nmp.group)

#         ## Add in paths with timePeriod 
#         createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath)
        
#         ## Export and test network 
#         network = createNetwork.showNetwork()
#         self.assertEqual( network.showTimePeriods(), ['summer', 'fall', 'winter'])
#         self.assertEqual( network.nodes[0].showTimePeriod(), 'summer')

#         network.runSimulation()
#         network.calculateNetworkPop()
        
#         self.assertAlmostEqual( network.nodes[0].showNodePopulation()[24], 2769.61819149)
#         self.assertAlmostEqual( network.nodes[1].showNodePopulation()[24], 2766.60008091)
#         self.assertAlmostEqual( network.nodes[2].showNodePopulation()[24], 2763.58525978)

        
if __name__ == '__main__':
    unittest.main()
