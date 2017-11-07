import networkModelPopulateSex as nmps
import unittest
import numpy as np
import scipy.stats as stats
import networkModelPopulate as nmp
import pandas as pd 


class test_groupWithSex( unittest.TestCase ):

    def test_addSex(self):
        grp = nmps.groupWithSex("test group")
        grp.addSex("male")
        self.assertEqual( grp.showSex(), "male")

    def test_recruitmentGroup(self):
        grp = nmps.groupWithSex("test group")
        self.assertEqual( grp.showRecruitmentGroup(), False)
        grp.addRecruitmentGroup( True)
        self.assertEqual( grp.showRecruitmentGroup(), True)

class test_populatedNodeWithSex( unittest.TestCase):
    ''' 
    Test populated nodes and also test load with csv files
    '''
    def test_networkCreation(self):
        ## Load files 
        self.inputFolder = "./inputParameters/"
        self.groupsFile = self.inputFolder + 'twoNodeTestGroupsSex.csv'
        self.dfGroups = pd.read_csv(self.groupsFile)
        
        self.nodeFile = self.inputFolder + 'twoNodeTestNodes.csv'
        self.dfNode = pd.read_csv(self.nodeFile)
        
        self.networkFile = self.inputFolder + 'twoNodeTestNetwork.csv'
        self.dfNetwork = pd.read_csv(self.networkFile)
        
        ## Test creation of network 
        self.createNetwork = nmps.createNetworkFromCSVwithSex( self.dfNetwork)
        
        ## Test addition of nodes
        self.createNetwork.addNodesFromCSV( self.dfNode, nodeIn = nmps.populatedNodeWithSex)

        ## Add in group's sex
        self.createNetwork.addGroupSexFromCSV( self.dfGroups, groupInIn =  nmps.groupWithSex)

        ## export and test network 
        self.network = self.createNetwork.showNetwork()


        ## Check projection with sex
        self.network.runSimulation()
        self.network.calculateNetworkPop()
        
        ## Run tests
        self.assertEqual( self.network.showNetworkName(), 'twoNodeNetwork')
        self.assertEqual( self.network.nYears, 25)
        self.assertEqual( len(self.network.omega), 200)
        self.assertEqual( len(self.network.nodes), 2)
        self.assertEqual( self.network.nodes[0].pathsOut, {'path 1': 0.05})
        self.assertEqual( self.network.nodes[1].pathsOut, {'path 2': 0.05, 'path 3': 0.0})
        self.assertEqual( self.network.nodes[0].showPathsIn(), ['path 2'])
        self.assertEqual( self.network.nodes[1].showPathsIn(), ['path 1', 'path 4'])

        self.assertEqual( self.network.nodes[0].groups[0].groupName, 'test group 1 male') 
        self.assertEqual( self.network.nodes[0].groups[0].groupName, 'test group 1 male')
        self.assertEqual( self.network.nodes[0].groups[0].eggTransition,  7e-5 ) 
        
        self.assertFalse( self.network.nodes[0].groups[0].showRecruitmentGroup())
        self.assertTrue( self.network.nodes[0].groups[1].showRecruitmentGroup())

        self.assertEqual( self.network.nodes[0].groups[1].showSex(), 'female')
        self.assertEqual( self.network.nodes[0].groups[0].showSex(), 'male')

        self.assertEqual( self.network.nodes[0].groups[1].showRecruitmentProportion(), 0.5)

        self.assertAlmostEqual( self.network.showNetworkPop()[25], 70427.424211979087)
        
if __name__ == '__main__':
    unittest.main()
