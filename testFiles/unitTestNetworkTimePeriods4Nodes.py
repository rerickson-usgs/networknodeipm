import unittest
import numpy as np
import scipy.stats as stats
import pandas as pd
import sys 
sys.path.append("../modelFiles")
import networkModelPopulate as nmp
import networkModelTimePeriods as nmtp


class testSimulationRun4Noodes( unittest.TestCase):
    ''' 
    test run without births or death
    '''
    def testRunSim( self):
        ## Load files 
        inputFolder = "../inputParameters/"
        groupsFile = inputFolder + 'fourNodeTestGroupsTimePeriodsNoBD.csv'
        dfGroups = pd.read_csv(groupsFile)
        
        nodeFile = inputFolder + 'fourNodeTestNodesTimePeriods.csv'
        dfNode = pd.read_csv(nodeFile)

        networkFile = inputFolder + 'fourNodeTestNetworkTimePeriods.csv'
        dfNetwork = pd.read_csv(networkFile)

        class populatedNetworkWithTimePeriods(nmtp.networkWithTimePeriod,
                                              nmp.populatedNetwork):
            pass
        
        ## Test creation of network 
        createNetwork = nmtp.createNetworkFromCSVwithTime(
            dfNetwork, populatedNetworkWithTimePeriods)

        ## Test addition of nodes
        class populatedNodeTimePeriod( nmtp.nodeTimePeriod,
                                       nmp.populatedNode):
            pass 
        
        createNetwork.addNodesFromCSV( dfNode, populatedNodeTimePeriod)
        createNetwork.addTimePeriodToNodes( dfNode)

        ## Test addition of groups 
        createNetwork.addGroupsFromCSV( dfGroups, groupIn = nmp.group)

        ## Add in paths with timePeriod 
        createNetwork.addTimePeriodToPaths( pathIn = nmp.populatedPath )
        
        ## Export and test network 
        network = createNetwork.showNetwork()

        self.assertEqual( network.nodes[0].showNodeName(), 'node 1')
        self.assertEqual( network.nodes[1].showNodeName(), 'node 2')
        self.assertEqual( network.nodes[2].showNodeName(), 'node 3')
        self.assertEqual( network.nodes[3].showNodeName(), 'node 4')

        self.assertEqual( network.nodes[0].showPathsOut(), ['path 1'])
        self.assertEqual( network.nodes[1].showPathsOut(), ['path 3', 'path 2'])
        self.assertEqual( network.nodes[2].showPathsOut(), ['path 4'])
        self.assertEqual( network.nodes[3].showPathsOut(), ['path 5'])
        self.assertEqual( network.nodes[1].pathsOut, {'path 3': 0.45, 'path 2': 0.55})


        self.assertEqual( [p.timePeriod for p in network.paths],
                          ['fall', 'winter', 'winter', 'summer', 'summer'])

        self.assertEqual( network.showTimePeriods(), ['summer', 'fall', 'winter'])
        self.assertEqual( network.nodes[0].showTimePeriod(), 'summer')

        
        network.runSimulation()
        network.calculateNetworkPop()
            
        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[25], 000.0)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[25], 000.0)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[25], 000.0)
        self.assertAlmostEqual( network.nodes[3].showNodePopulation()[25], 000.0)
        
        self.assertAlmostEqual( network.nodes[0].showNodePopulation()[24], 6000.0)
        self.assertAlmostEqual( network.nodes[1].showNodePopulation()[24], 6000.0)
        self.assertAlmostEqual( network.nodes[2].showNodePopulation()[24], 3300.0)
        self.assertAlmostEqual( network.nodes[3].showNodePopulation()[24], 2700.0)
        
if __name__ == '__main__':
    unittest.main()
