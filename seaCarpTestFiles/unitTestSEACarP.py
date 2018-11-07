import unittest
import numpy as np
import scipy.stats as stats
import pandas as pd 
import sys
sys.path.append("../modelFiles")
import SEACarP as sea

        
class test_buildNetwork( unittest.TestCase):

    def test_network_construction(self):
        '''
        This funciton tests the construction of the network and
        the paths within the network. 
        '''
        network = sea.createSEACarPNetwork()
        self.assertEqual(network.showNetworkName(), "SEACarpIL")
        self.assertEqual(network.nodes[0].showNodeName(), 'Alton')
        self.assertEqual(network.nodes[0].showPathsIn(), ['LaGrange', 'Peoria'] )
        self.assertEqual(network.nodes[0].showPathsOut(),  ['LaGrange', 'Alton'] )
        self.assertEqual(network.nodes[0].pathsOut, {'LaGrange': 0.27, 'Alton':0.73})


        
if __name__ == '__main__':
    unittest.main()
