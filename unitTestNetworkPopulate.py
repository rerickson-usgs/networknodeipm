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

class test_gropu( unittest.TestCase):

    def test_group(self):
        self.group = nmp.group( "test group")
        self.assertEqual( self.group.showGroupName(), "test group")

    def test_createPopDist(self):
        ''' test createPopDist and showPopDist''' 
        self.group = nmp.group( "test group")
        self.group.createPopDist( 10, 24)
        self.assertEqual( self.group.showPopDist().shape, (10, 24))
        self.assertEqual( self.group.showPopDist().sum(1)[0], 0 )

        self.group = nmp.group( "test group 2")
        self.group.createPopDist( 10, 24, np.ones(24))
        self.assertEqual( self.group.showPopDist().sum(1)[0], 24)

    def test_yearUpdateAndYearShow(self):
        ''' test createPopDist and showPopDist''' 
        self.group = nmp.group( "test group")
        self.group.createPopDist( 2, 24, np.ones(24))
        self.group.updatePopDistYear(1, self.group.showPopDistYear(0) * 2.0)
        self.group.showPopDistYear(1)
        self.assertEqual( self.group.showPopDistYear(1).sum(), 48)
        
class test_logistic(unittest.TestCase):
    
    def test_one(self):
        self.logistic = nmp.logistic( 40.0, -5.0, 0.0, 1.0)
        self.assertEqual( self.logistic(2e8), 1.0)

    def test_inflecitonPoint(self):
        self.logistic = nmp.logistic( 40.0, -5.0, 0.0, 1.0)
        self.assertEqual( self.logistic( 40.0), 0.5)


class test_densityNegExp(unittest.TestCase):

    def test_zeros(self):
        """Constructor"""
        a = 10.0
        b = 11.0
        biomass = 0.0
        zeroFunc = nmp.densityNegExp(a = a, b = b)

        self.assertEqual( zeroFunc(biomass = biomass), 10.0)

class test_lengthWeight(unittest.TestCase):

    def test_zero(self):
        self.lengthWeight = nmp.lengthWeight(alphaLW = 1.0,
                                               betaLW  = 2.0)
        self.assertEqual( self.lengthWeight(1.0), 10.0)

    def test_nonzero(self):
        self.lengthWeight = nmp.lengthWeight(alphaLW = 1.0,
                                               betaLW  = 2.0)
        self.assertEqual( self.lengthWeight(10.0), 1000.0)

        
class test_growthVB(unittest.TestCase):

    def test_growthVB(self):
        self.growthVB = nmp.growthVB( 180.0, 0.16, 10.0)
        self.assertEqual( self.growthVB(180, 180), 0.039894228040143268)

        
if __name__ == '__main__':
    unittest.main()
