import unittest
import numpy as np
import scipy.stats as stats
import networkModel as nm
import pandas as pd 


class test_path( unittest.TestCase):

    def test_showPathName(self):
        self.path = nm.path('test path')

        self.assertEqual( self.path.showPathName(), 'test path')
    
    def test_startNode(self):
        self.path = nm.path('test path')
        self.path.addStartNode('startNode')
        
        self.assertEqual( self.path.showStartNode(), 'startNode')

    def test_endNode(self):
        self.path = nm.path('test path')
        self.path.addEndNode('endNode')
        
        self.assertEqual( self.path.showEndNode(), 'endNode')


class test_node( unittest.TestCase):

    def test_pathIn(self):
        self.node = nm.node('test node')

        self.node.addPathsIn( ['test path 1'])
        self.assertEqual( self.node.showPathsIn() , ['test path 1'])


    def test_pathOut(self):
        self.node = nm.node('test node')
        
        self.node.addPathsOut( ['test path 1'])
        self.assertEqual( self.node.showPathsOut() , ['test path 1'])


    def test_node(self):
        self.node = nm.node('test node')
        self.assertEqual( self.node.showNodeName(), 'test node')

class test_network:
    
    def test_networkName(self):
        self.netowrk = nm.network('test network')
        self.assertEqual( self.network.showNetworkName(), 'test network')

        
if __name__ == '__main__':
    unittest.main()
