import unittest
import numpy as np
import scipy.stats as stats
import networkModelPopulate as nmp
import pandas as pd 


class test_populatedPath( unittest.TestCase):

    def test_showPopulatedPathName(self):
        self.populatedPath = nmp.populatedPath('test populatedPath')

        self.assertEqual( self.populatedPath.showPathName(),
                          'test populatedPath')
        
    def test_startNode(self):
        self.populatedPath = nmp.populatedPath('test path')
        self.populatedPath.addStartNode('startNode')
        
        self.assertEqual( self.populatedPath.showStartNode(), 'startNode')

    def test_endNode(self):
        self.populatedPath = nmp.populatedPath('test path')
        self.populatedPath.addEndNode('endNode')
        
        self.assertEqual( self.populatedPath.showEndNode(), 'endNode')

    def test_addGroups(self):
        self.populatedPath = nmp.populatedPath('test path')
        self.populatedPath.addGroups(['male', 'female'])
        
        self.assertEqual( self.populatedPath.showGroups(), ['male', 'female'])
        

class test_populatedNode( unittest.TestCase):

    def test_pathIn(self):
        self.populatedNode = nmp.populatedNode('test node')

        self.populatedNode.addPathsIn( ['test path 1'])
        self.assertEqual( self.populatedNode.showPathsIn() , ['test path 1'])

    def test_pathOut(self):
        self.populatedNode = nmp.populatedNode('test node')
        
        self.populatedNode.addPathsOut( ['test path 1'])
        self.assertEqual( self.populatedNode.showPathsOut() , ['test path 1'])

    def test_populatedNode(self):
        self.populatedNode = nmp.populatedNode('test node')
        self.assertEqual( self.populatedNode.showNodeName(), 'test node')


    def test_addGroups(self):
        self.populatedNode = nmp.populatedNode('test node')
        self.populatedNode.addGroups(['male', 'female'])
        
        self.assertEqual( self.populatedNode.showGroups(), ['male', 'female'])
        
if __name__ == '__main__':
    unittest.main()
