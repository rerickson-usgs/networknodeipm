import networkModelPopulateSterileMale as nmpsm
import networkModelPopulateSex as nmps
import unittest
import numpy as np
import scipy.stats as stats
import networkModelPopulate as nmp
import pandas as pd 


# class test_groupWithSex( unittest.TestCase ):

class test_groupWithSexYY( unittest.TestCase):
    def test_impactedParameter( self):
        grp = nmpsm.groupWithSexSterileMale( "test group")
        self.assertFalse(grp.stocking)
        self.assertFalse(grp.recruitmentGroup)
        self.assertEqual(grp.showRecruitmentViabilityMod(), 1.0)
        grp.addRecruitmentViabilityMod( 0.75)
        self.assertEqual( grp.showRecruitmentViabilityMod(), 0.75)

        grp.addImpactRecruitmentViability( 0.23)
        self.assertEqual( grp.showImpactRecruitmentViability(), 0.23)

class test_populatedNodeWithSex( unittest.TestCase):
    ''' 
    Test populated nodes and also test load with csv files
    '''
    def test_networkCreation(self):
        ## Load files 
        inputFolder = "./inputParameters/"
        groupsFile = inputFolder + 'twoNodeTestGroupsSterileMales.csv'
        dfGroups = pd.read_csv(groupsFile)
        
        nodeFile = inputFolder + 'twoNodeTestNodes.csv'
        dfNode = pd.read_csv(nodeFile)
        
        networkFile = inputFolder + 'twoNodeTestNetwork.csv'
        dfNetwork = pd.read_csv(networkFile)
        
        ## Test creation of network 
        createNetwork = nmpsm.createNetworkFromCSVwithSterileMale( dfNetwork)
        
        ## Test addition of nodes
        createNetwork.addNodesFromCSV( dfNode, nodeIn = nmps.populatedNodeWithSex)

        ## Add in group's sex
        createNetwork.addGroupSexFromCSV( dfGroups,
                                          groupInIn = nmpsm.groupWithSexSterileMale)

        ## export and test network 
        network = createNetwork.showNetwork()

        ## Check projection with sex
        network.runSimulation()
        network.calculateNetworkPop()

        ## Run tests
        self.assertEqual( network.showNetworkName(), 'twoNodeNetwork')
        self.assertEqual( network.nYears, 25)
        self.assertEqual( len(network.omega), 200)
        self.assertEqual( len(network.nodes), 2)
        self.assertEqual( network.nodes[0].pathsOut, {'path 1': 0.05})
        self.assertEqual( network.nodes[1].pathsOut, {'path 2': 0.05, 'path 3': 0.0})
        self.assertEqual( network.nodes[0].showPathsIn(), ['path 2'])
        self.assertEqual( network.nodes[1].showPathsIn(), ['path 1', 'path 4'])

        self.assertEqual( network.nodes[0].groups[0].groupName, 'test group 1 male') 
        self.assertEqual( network.nodes[0].groups[0].groupName, 'test group 1 male')
        self.assertEqual( network.nodes[0].groups[0].eggTransition,  7e-5 ) 
        
        self.assertFalse( network.nodes[0].groups[0].showRecruitmentGroup())
        self.assertTrue( network.nodes[0].groups[1].showRecruitmentGroup())

        self.assertEqual( network.nodes[0].groups[1].showSex(), 'female')
        self.assertEqual( network.nodes[0].groups[0].showSex(), 'male')

        self.assertEqual( network.nodes[0].groups[1].showRecruitmentProportion(), 0.5)

        self.assertAlmostEqual(
            network.showNetworkPop()[25],
            206091.43267436879)

        self.assertAlmostEqual(
            network.nodes[0].groups[2].showStockingPopYear(11).sum(),
            100000.0)
        self.assertAlmostEqual(
            network.nodes[0].groups[2].showStockingPopYear(9).sum(),
            0000.0)
if __name__ == '__main__':
    unittest.main()
