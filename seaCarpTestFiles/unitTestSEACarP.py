import unittest
import numpy as np
import scipy.stats as stats
import pandas as pd 
import sys
sys.path.append("../modelFiles")
import SEACarP as sea

class test_Network( unittest.TestCase):

    def test_network_(self):
        '''
        This funciton tests the construction of the network and
        the paths within the network. 
        '''
        rawNetwork = sea.createSEACarPNetwork()
        network = rawNetwork.outputNetwork()

        ## testbuilding the network 
        self.assertEqual(network.showNetworkName(), "SEACarpIL")
        self.assertEqual(network.nodes[12].showTimePeriod(), 3.0)
        self.assertEqual(network.nodes[0].showNodeName(), 'Alton')
        self.assertEqual(network.nodes[0].showPathsIn(), ['LaGrange', 'Peoria'] )
        self.assertEqual(network.nodes[0].showPathsOut(),  ['LaGrange', 'Alton'] )
        self.assertEqual(network.nodes[0].pathsOut, {'LaGrange': 0.27, 'Alton':0.73})
        self.assertTrue(network.nodes[0].probSuccessSpawn.args == (1, 3))
        self.assertEqual(network.nodes[3].groups[0].showSex(), 'Male')
        self.assertEqual(network.nodes[3].groups[1].showSex(), 'Female')
        self.assertEqual(network.nodes[3].groups[0].showRecruitmentGroup(), False)
        self.assertEqual(network.nodes[3].groups[1].showRecruitmentGroup(), True)
        self.assertEqual(network.nodes[3].groups[0].recruitmentProportion, 0.5)
        self.assertEqual(network.nodes[3].groups[1].recruitmentProportion, 0.5)
        self.assertEqual(network.nodes[3].groups[0].eggPerkg, 0)
        self.assertEqual(network.nodes[3].groups[1].eggPerkg, 500)
        self.assertEqual(network.nodes[3].groups[0].eggTransition, 0)
        self.assertEqual(network.nodes[3].groups[1].eggTransition, 7e-5)
        self.assertEqual(network.nodes[3].groups[0].muJ, 10)
        self.assertEqual(network.nodes[3].groups[1].muJ, 10)
        self.assertAlmostEqual(network.nodes[3].groups[1].density(0), 1.0)
        self.assertAlmostEqual(network.nodes[3].groups[1].density(1E4), 0.99004983374916811)
        self.assertAlmostEqual(network.nodes[3].groups[1].density(1E6), 0.36787944117144233)
        self.assertAlmostEqual(network.nodes[3].groups[1].density(1E8), 3.7200759760208361e-44)
        self.assertEqual(network.nodes[3].groups[0].sigmaJ, 2)
        self.assertEqual(network.nodes[3].groups[1].sigmaJ, 2)
        self.assertAlmostEqual(network.nodes[3].groups[0].showPopDistYear(0).sum(), 1000.0)
        self.assertAlmostEqual(network.nodes[3].groups[0].showPopYear(0), 1000.0)
        self.assertAlmostEqual(network.nodes[3].groups[1].showPopYear(0), 1000.0)
        self.assertAlmostEqual(network.nodes[3].groups[0].survival(1), 0.96074806)
        self.assertAlmostEqual(network.nodes[3].groups[1].survival(10), 0.96074806)
        self.assertAlmostEqual(network.nodes[6].groups[0].survival(234), 0.95449851)
        self.assertAlmostEqual(network.nodes[24].showNodeHarvest().sum(), 2.5)


        
if __name__ == '__main__':
    unittest.main()
