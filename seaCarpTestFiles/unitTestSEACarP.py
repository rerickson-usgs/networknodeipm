import unittest
import numpy as np
import scipy.stats as stats
import pandas as pd 
import sys
sys.path.append("../modelFiles")
import SEACarP as sea

## Next steps:
## Add in group parameter values
## [x] create generic group variables
## Look at nmp.addGroupsFromCSV for next steps 
## [X] add in starting population details
## [X] add in LW details, no need to adjust for monthly
## [X] add in VB details and survival, adjust for monthly
## [X] add in maturation details, no need to adjust for montly
## [X] add in other parameter (not parameterize, in GroupDetails.csv)
## AM HERE, need to debug extraction function
## [ ] Add in update nodes (if needed)
## [ ] Add in harvest option, will need to create table for this step 
## [ ] Add in stochastic recruitment

class test_buildNetwork( unittest.TestCase):

    def test_network_construction(self):
        '''
        This funciton tests the construction of the network and
        the paths within the network. 
        '''
        rawNetwork = sea.createSEACarPNetwork()
        network = rawNetwork.outputNetwork()
        self.assertEqual(network.showNetworkName(), "SEACarpIL")
        self.assertEqual(network.nodes[12].showNodeSeason(), 3.0)
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
        self.assertEqual(network.nodes[3].groups[0].sigmaJ, 2)
        self.assertEqual(network.nodes[3].groups[1].sigmaJ, 2)
        self.assertEqual(network.nodes[3].groups[0].showPopYear(0), 1000.0)
        self.assertEqual(network.nodes[3].groups[1].showPopYear(0), 1000.0)
        self.assertAlmostEqual(network.nodes[3].groups[0].survival, 0.96074806)
        self.assertAlmostEqual(network.nodes[3].groups[1].survival, 0.96074806)
        self.assertAlmostEqual(network.nodes[6].groups[0].survival, 0.95449851)

        self.assertAlmostEqual(network.nodes[0].showNodeHarvest().sum(), 0)
        self.assertAlmostEqual(network.nodes[24].showNodeHarvest().sum(), 1.7)

        self.assertAlmostEqual(len(network.nodes[0].showNodeHarvest()), 51)


if __name__ == '__main__':
    unittest.main()
