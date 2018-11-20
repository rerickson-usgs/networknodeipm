import unittest
import numpy as np
import scipy.stats as stats
import pandas as pd
import sys 
sys.path.append("../modelFiles")
import networkModelPopulate as nmp
import networkModelTimePeriods as nmtp


class testNetworkTimePeriods( unittest.TestCase): 

    def testAddTimePeriods(self):
        network = nmtp.networkWithTimePeriod()
        timePeriods = ["winter", "summer", "fall"]
        network.addTimePeriods( timePeriods)
        self.assertEqual( network.showTimePeriods(), timePeriods)

class testNodeTimePeriod( unittest.TestCase):
    def testAddTimePeriod(self):
        node = nmtp.nodeTimePeriod()
        tp = "fall"
        node.addTimePeriod( tp )
        self.assertEqual(node.showTimePeriod(), tp)


class testMovementRun( unittest.TestCase):
    def testRunSim( self):

        ## Load files 
        inputFolder = "../inputParameters/"
        groupsFile = inputFolder + 'threeNodeTestGroupsTimePeriodsNoBD.csv'
        dfGroups = pd.read_csv(groupsFile)
        
        nodeFile = inputFolder + 'threeNodeTestNodesTimePeriods.csv'
        dfNode = pd.read_csv(nodeFile)
        
        networkFile = inputFolder + 'threeNodeTestNetworkTimePeriods.csv'
        dfNetwork = pd.read_csv(networkFile)

        class populatedNetworkWithTimePeriods(nmtp.networkWithTimePeriod,
                                              nmp.populatedNetwork):
            def __init__(self, networkName):
                self.networkName = networkName
                self.nodes = []
                self.paths = []
                self.timePeriods = []

        ## Test creation of network 
        createNetwork = nmtp.createNetworkFromCSVwithTime(
            dfNetwork, populatedNetworkWithTimePeriods)

        ## Test addition of nodes
        class populatedNodeTimePeriod( nmtp.nodeTimePeriod,
                                       nmp.populatedNode):
            def __init__(self, nodeName):
                self.nodeName = nodeName
                self.groups = []
                self.pathsIn = []
                self.pathsOut = {}
        
        createNetwork.addNodesFromCSV( dfNode, populatedNodeTimePeriod)
        createNetwork.addTimePeriodToNodes( dfNode)
        
        ## Test addition of groups 
        createNetwork.addGroupsFromCSV( dfGroups, groupIn = nmp.group)

        ## Add in paths with timePeriod 
        createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath)
        
        ## Export and test network 
        network = createNetwork.showNetwork()
        self.assertEqual( network.showTimePeriods(), ['summer', 'fall', 'winter'])
        self.assertEqual( network.nodes[0].showTimePeriod(), 'summer')

        ## Test movement within network 


        network.calculateNetworkPop()
        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[0], 000)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[0], 0)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[0], 3000)
        
        for tp in network.showTimePeriods():
            network.moveGroups( 1, 1, tp)

        network.calculateNetworkPop()
        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[1], 3000)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[1], 3000)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[1], 3000)

        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[0], 0.0)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[0], 0.0)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[0], 3000.0)


class testSimulationRun( unittest.TestCase):
    ''' 
    test run without births or death
    '''
    def testRunSim( self):

        ## Load files 
        inputFolder = "../inputParameters/"
        groupsFile = inputFolder + 'threeNodeTestGroupsTimePeriodsNoBD.csv'
        dfGroups = pd.read_csv(groupsFile)
        
        nodeFile = inputFolder + 'threeNodeTestNodesTimePeriods.csv'
        dfNode = pd.read_csv(nodeFile)
        
        networkFile = inputFolder + 'threeNodeTestNetworkTimePeriods.csv'
        dfNetwork = pd.read_csv(networkFile)

        class populatedNetworkWithTimePeriods(nmtp.networkWithTimePeriod,
                                              nmp.populatedNetwork):
            def __init__(self, networkName):
                self.networkName = networkName
                self.nodes = []
                self.paths = []
                self.timePeriods = []

        ## Test creation of network 
        createNetwork = nmtp.createNetworkFromCSVwithTime(
            dfNetwork, populatedNetworkWithTimePeriods)

        ## Test addition of nodes
        class populatedNodeTimePeriod( nmtp.nodeTimePeriod,
                                       nmp.populatedNode):
            def __init__(self, nodeName):
                self.nodeName = nodeName
                self.groups = []
                self.pathsIn = []
                self.pathsOut = {}
        
        createNetwork.addNodesFromCSV( dfNode, populatedNodeTimePeriod)
        createNetwork.addTimePeriodToNodes( dfNode)
        
        ## Test addition of groups 
        createNetwork.addGroupsFromCSV( dfGroups, groupIn = nmp.group)

        ## Add in paths with timePeriod 
        createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath)
        
        ## Export and test network 
        network = createNetwork.showNetwork()
        self.assertEqual( network.showTimePeriods(), ['summer', 'fall', 'winter'])
        self.assertEqual( network.nodes[0].showTimePeriod(), 'summer')

        network.runSimulation()
        network.calculateNetworkPop()
            
        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[25], 000.0)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[25], 000.0)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[25], 000.0)

        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[24], 3000.0)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[24], 3000.0)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[24], 3000.0)


        
class testSimulationRunWithDeath( unittest.TestCase):
    def testRunSim( self):

        ## Load files 
        inputFolder = "../inputParameters/"
        groupsFile = inputFolder + 'threeNodeTestGroupsTimePeriodsNoB.csv'
        dfGroups = pd.read_csv(groupsFile)
        
        nodeFile = inputFolder + 'threeNodeTestNodesTimePeriods.csv'
        dfNode = pd.read_csv(nodeFile)
        
        networkFile = inputFolder + 'threeNodeTestNetworkTimePeriods.csv'
        dfNetwork = pd.read_csv(networkFile)

        class populatedNetworkWithTimePeriods(nmtp.networkWithTimePeriod,
                                              nmp.populatedNetwork):
            def __init__(self, networkName):
                self.networkName = networkName
                self.nodes = []
                self.paths = []
                self.timePeriods = []

        ## Test creation of network 
        createNetwork = nmtp.createNetworkFromCSVwithTime(
            dfNetwork, populatedNetworkWithTimePeriods)

        ## Test addition of nodes
        class populatedNodeTimePeriod( nmtp.nodeTimePeriod,
                                       nmp.populatedNode):
            def __init__(self, nodeName):
                self.nodeName = nodeName
                self.groups = []
                self.pathsIn = []
                self.pathsOut = {}
        
        createNetwork.addNodesFromCSV( dfNode, populatedNodeTimePeriod)
        createNetwork.addTimePeriodToNodes( dfNode)
        
        ## Test addition of groups 
        createNetwork.addGroupsFromCSV( dfGroups, groupIn = nmp.group)

        ## Add in paths with timePeriod 
        createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath)
        
        ## Export and test network 
        network = createNetwork.showNetwork()
        self.assertEqual( network.showTimePeriods(), ['summer', 'fall', 'winter'])
        self.assertEqual( network.nodes[0].showTimePeriod(), 'summer')

        network.runSimulation()
        network.calculateNetworkPop()
        
        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[24], 2766.6000809149141)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[24], 2763.5852597783942)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[24], 2760.5737244112697)

        
if __name__ == '__main__':
    unittest.main()
