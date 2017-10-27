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

    def test_populatedNodePopulate(self):
        self.populatedNode = nmp.populatedNode('test node')
        self.assertEqual( self.populatedNode.showNodeName(), 'test node')


    def test_addGroups(self):
        self.populatedNode = nmp.populatedNode('test node')
        self.populatedNode.addGroups(['male', 'female'])
        
        self.assertEqual( self.populatedNode.showGroups(), ['male', 'female'])


    def test_addSingleProbOut(self):
        self.node = nmp.populatedNode('test node')
        self.node.addPathsOut( {'path 1': 0.2})
        self.assertEqual(self.node.pathsOut, {'path 1': 0.2})

    def test_addTwoProbOut(self):
        self.node = nmp.populatedNode('test node')
        self.node.addPathsOut( [ {'path 1': 0.2},
                                 {'path 2': 0.8} ]
                               )
        self.assertEqual( self.node.pathsOut,
                          {'path 1': 0.2,
                           'path 2': 0.8}
                          )
        
    def test_claculateNodeBiomass(self):
        self.node = nmp.populatedNode('test node')
        self.group = nmp.group('test group')
        self.group.createPopDist( 10, 24, np.ones(24))
        def multBy1(omega):
            return np.multiply( omega, 1.0)
        self.group.setLengthWeight( multBy1)
        self.node.addGroups([self.group])
        self.node.calculateNodeBiomass( np.linspace(1, 24, 1), 0 )
        self.assertEqual( self.node.showNodeBiomass(), 24.0)


    def test_populationSize(self):
        self.omega = range(1, 300)
        self.node = nmp.populatedNode('test node')
        self.group = nmp.group('test group')
        self.group.createPopDist( nYears = 2, nPoints = len(self.omega), popDist0 = np.ones( len(self.omega) ))
        self.node.addGroups([ self.group ])
        self.node.calculateNodePop()
        self.assertEqual( self.node.populationDistribution.shape, (3, 299))
        self.assertEqual( len(self.node.population), 3)
        self.assertEqual( self.node.population[0], 299.0)
        self.assertEqual(  self.node.showNodePopulation()[0], 299)
        
    def test_projectionWithinNode(self):
        self.omega = range(1, 300)
        self.node = nmp.populatedNode('test node')
        self.group = nmp.group('test group')
        self.group.createPopDist( nYears = 3, nPoints = len(self.omega), popDist0 = np.ones( len(self.omega)))
        self.group.setGrowth( nmp.growthVB( 180.0, 0.16, 10.0) )
        self.group.setSurvival(  nmp.logistic( 40.0, -5.0, 0.0, 1.0) )
        self.group.setProbabilityOfReproducing( nmp.logistic( 40.0, -5.0, 0.0, 1.0))
        self.group.setEggTransition(1.0e-3)
        self.group.setEggPerkg( 200.0)
        self.group.setMuJ( np.log(10.0))
        self.group.setSigmaJ( 1.1)
        self.group.setLengthWeight( nmp.lengthWeight(alphaLW = 1.0,
                                                     betaLW  = 2.0) )
        self.group.setDensity( nmp.densityNegExp(a = 10.0,
                                                 b = 11.0) )
        
        self.group.recruitment = nmp.linearRecruitment(
            lengthWeight = self.group.lengthWeight,
            survival = self.group.survival,
            probabilityReproducing = self.group.probabilityOfReproducing,
            eggTransition = self.group.eggTransition,
            eggPerkg = self.group.eggPerkg,
            muJ = self.group.muJ,
            sigmaJ = self.group.sigmaJ)

        
        self.node.addGroups([ self.group ])

        ## test without density
        self.node.projectGroups( year = 0, omega = self.omega, hWidth = self.omega[1] - self.omega[0],
                                 nodeBiomass = 0.0)
        self.node.calculateNodePop()
        self.assertAlmostEqual(self.node.showNodePopulation()[0], 299)
        self.assertAlmostEqual(self.node.showNodePopulation()[1], 177771069.98259112)

        ## test with density
        self.group.createPopDist( nYears = 3, nPoints = len(self.omega), popDist0 = np.ones( len(self.omega)))
        self.node.projectGroups( year = 0, omega = self.omega, hWidth = self.omega[1] - self.omega[0],
                                 nodeBiomass = 1e4)
        self.node.calculateNodePop()
        self.assertAlmostEqual( self.node.showNodePopulation()[0], 299)
        self.assertAlmostEqual( self.node.showNodePopulation()[1], 256.6178009967002)
        
        
class test_linearRecruitment( unittest.TestCase):

    def test_linRec(self):
        self.lengthWeight = nmp.lengthWeight(alphaLW = 1.0,
                                             betaLW  = 2.0)
        self.survival = nmp.logistic( 40.0, -5.0, 0.0, 1.0)
        self.probabilityReproducing = nmp.logistic( 40.0, -5.0, 0.0, 1.0)
        self.eggTransition = 1.0e-3
        self.eggPerkg = 200.0
        self.muJ = np.log(10.0)
        self.sigmaJ = 1.1

        self.recruitment = nmp.linearRecruitment(
            lengthWeight = self.lengthWeight,
            survival = self.survival,
            probabilityReproducing = self.probabilityReproducing,
            eggTransition = self.eggTransition,
            eggPerkg = self.eggPerkg,
            muJ = self.muJ,
            sigmaJ = self.sigmaJ)

        self.assertAlmostEqual( self.recruitment( 180.0, 10.0), 64729.82385407)
        self.assertEqual(self.recruitment( omega = range(197, 200), omegaPrime = range( 196, 200)).shape,
                         ( 4, 3) )
            
class test_group( unittest.TestCase):

    def test_group(self):
        self.group = nmp.group( "test group")
        self.assertEqual( self.group.showGroupName(), "test group")

    def test_createPopDist(self):
        ''' test createPopDist and showPopDist''' 
        self.group = nmp.group( "test group")
        self.group.createPopDist( 10, 24)
        self.assertEqual( self.group.showPopDist().shape, (11, 24))
        self.assertEqual( self.group.showPopDist().sum(1)[0], 0 )

        self.group = nmp.group( "test group 2")
        self.group.createPopDist( 10, 24, np.ones(24))
        self.assertEqual( self.group.showPopDist().sum(1)[0], 24)

    def test_yearUpdateAndYearShow(self):
        ''' test yearly funcitons for pop dist''' 
        self.group = nmp.group( "test group")
        self.group.createPopDist( 2, 24, np.ones(24))
        self.group.updatePopDistYear(1, self.group.showPopDistYear(0) * 2.0)
        self.group.showPopDistYear(1)
        self.assertEqual( self.group.showPopDistYear(1).sum(), 48)

    def test_groupSurvivla(self):
        self.group = nmp.group( "test group")
        self.group.setSurvival( 'sur')
        self.assertEqual( self.group.survival, 'sur')

    def test_groupGrowth(self):
        self.group = nmp.group( "test group")
        self.group.setGrowth( 'grow')
        self.assertEqual( self.group.growth, 'grow')

    def test_groupProbabilityOfReproducing(self):
        self.group = nmp.group( "test group")
        self.group.setProbabilityOfReproducing( 'repo')
        self.assertEqual( self.group.probabilityOfReproducing, 'repo')


    def test_groupLengthWeigth(self):
        self.group = nmp.group( "test group")
        self.group.setLengthWeight( 1.0)
        self.assertEqual( self.group.lengthWeight, 1.0)
           
    def test_density(self):
        self.group = nmp.group("test group")
        self.group.setDensity( 2.0)
        self.assertEqual( self.group.density, 2.0)
    
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


    def test_noEffect(self):
        """Constructor"""
        a = 1.0
        b = 0.0
        biomass = 1000.0
        zeroFunc = nmp.densityNegExp(a = a, b = b)

        self.assertEqual( zeroFunc(biomass = biomass), 1.0)

        
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

    def test_growthVBmtx(self):
        self.growthVB = nmp.growthVB( 180.0, 0.16, 10.0)
        self.assertEqual( self.growthVB( range( 1, 20), range( 1, 20)).shape, (19, 19))

class test_populatedNetwork( unittest.TestCase):

    def test_move(self):
        self.node1 = nmp.populatedNode('test node 1')
        self.node2 = nmp.populatedNode('test node 2')

        self.group1 = nmp.group('test group')
        self.group1.createPopDist( nYears = 10, nPoints = 24, popDist0 = np.ones(24))

        self.node1.addGroups( [self.group1 ])
        self.node1.addPathsOut( [ {'path 1': 0.75} ] )

        self.assertEqual(self.node1.pathsOut, {'path 1': 0.75})

        self.group2 = nmp.group('test group')
        self.group2.createPopDist( nYears = 10, nPoints = 24)
        self.node2.addGroups( [self.group2 ])      
        self.node2.addPathsIn(  [ 'path 1'])
        self.assertEqual( self.node2.showPathsIn(), ['path 1'])

        self.populatedPath = nmp.populatedPath('path 1')
        self.populatedPath.addStartNode('test node 1')
        self.populatedPath.addEndNode('test node 2')        

        self.pathGroup = nmp.group('test group')
        self.pathGroup.createPopDist( nYears = 10, nPoints = 24)
        self.populatedPath.addGroups( [self.pathGroup])
        
        self.network = nmp.populatedNetwork('test network')
        self.network.addNodes( [ self.node1, self.node2 ] )
        self.network.addPaths( [ self.populatedPath ])
        
        self.network.moveGroups( startYear = 0, endYear = 0)

        ## Check to make sure 1/2 of population is at start and half is at end
        self.network.calculateNetworkPop()
        self.assertEqual(self.network.showNetworkPop()[0], 24.0)
        self.assertEqual(self.network.nodes[0].showNodePopulation()[0], 6.0)
        self.assertEqual(self.network.nodes[1].showNodePopulation()[0], 18.0)

    def test_nYearsAdd(self):
        self.network = nmp.populatedNetwork('test network')
        self.network.setYears(24)
        self.assertEqual( self.network.nYears, 24)

    def test_runSimulation(self):

        self.node1 = nmp.populatedNode('test node 1')
        self.node2 = nmp.populatedNode('test node 2')

        self.group1 = nmp.group('test group')

        self.nPoints = 50
        self.nYears = 3
        self.minLength = 1
        self.maxLength = 450

        self.group1.createPopDist( nYears = self.nYears, nPoints = self.nPoints,
                                   popDist0 = np.array(range(self.nPoints))/20.0)
        self.group1.setGrowth( nmp.growthVB( 180.0, 0.16, 10.0) )
        self.group1.setSurvival(  nmp.logistic( 40.0, -5.0, 0.0, 1.0) )
        self.group1.setProbabilityOfReproducing( nmp.logistic( 40.0, -5.0, 0.0, 1.0))
        self.group1.setEggTransition(1.0e-3)
        self.group1.setEggPerkg( 200.0)
        self.group1.setMuJ( np.log(10.0))
        self.group1.setSigmaJ( 1.1)
        self.group1.setLengthWeight( nmp.lengthWeight(alphaLW = 1.0,
                                                      betaLW  = 2.0) )
        self.group1.setRecruitment( nmp.linearRecruitment( lengthWeight = self.group1.lengthWeight,
                                                           survival = self.group1.survival,
                                                           probabilityReproducing = self.group1.probabilityOfReproducing,
                                                           eggTransition = self.group1.eggTransition,
                                                           eggPerkg = self.group1.eggPerkg,
                                                           muJ = self.group1.muJ,
                                                           sigmaJ = self.group1.sigmaJ) )
        self.group1.setDensity( nmp.densityNegExp(a = 1.0,
                                                  b = 1e-6) )
        self.node1.addGroups( [self.group1 ])
        self.node1.addPathsOut( [ {'path 1': 0.2} ] )

        self.group2 = nmp.group('test group')
        self.group2.createPopDist( nYears = self.nYears,
                                   nPoints = self.nPoints,
                                   popDist0 = np.array(range(self.nPoints))/30.0)
        self.group2.setGrowth( nmp.growthVB( 180.0, 0.16, 10.0) )
        self.group2.setSurvival(  nmp.logistic( 40.0, -5.0, 0.0, 1.0) )
        self.group2.setProbabilityOfReproducing( nmp.logistic( 40.0, -5.0, 0.0, 1.0))
        self.group2.setEggTransition(1.0e-3)
        self.group2.setEggPerkg( 200.0)
        self.group2.setMuJ( np.log(10.0))
        self.group2.setSigmaJ( 1.1)
        self.group2.setLengthWeight( nmp.lengthWeight(alphaLW = 1.0,
                                                      betaLW  = 2.0) )
        self.group2.setRecruitment( nmp.linearRecruitment( lengthWeight = self.group2.lengthWeight,
                                                           survival = self.group2.survival,
                                                           probabilityReproducing = self.group2.probabilityOfReproducing,
                                                           eggTransition = self.group2.eggTransition,
                                                           eggPerkg = self.group2.eggPerkg,
                                                           muJ = self.group2.muJ,
                                                           sigmaJ = self.group2.sigmaJ) )
        self.group2.setDensity( nmp.densityNegExp(a = 1.0,
                                                  b = 1e-6) )


        self.node2.addGroups( [self.group2 ])      
        self.node2.addPathsIn(  [ 'path 1'])

        self.node2.addPathsOut( [ {'path 2': 0.2} ] )
        self.node1.addPathsIn( ['path 2'] )

        self.populatedPath1 = nmp.populatedPath('path 1')
        self.populatedPath1.addStartNode('test node 1')
        self.populatedPath1.addEndNode('test node 2')        

        self.populatedPath2 = nmp.populatedPath('path 2')
        self.populatedPath2.addStartNode('test node 2')
        self.populatedPath2.addEndNode('test node 1')        

        self.pathGroup1 = nmp.group('test group')
        self.pathGroup1.createPopDist( nYears = self.nYears, nPoints = self.nPoints)
        self.populatedPath1.addGroups( [self.pathGroup1])

        self.pathGroup2 = nmp.group('test group')
        self.pathGroup2.createPopDist( nYears = self.nYears, nPoints = self.nPoints)
        self.populatedPath2.addGroups( [self.pathGroup2])


        self.network = nmp.populatedNetwork('test network')
        self.network.setupNetworkMesh( nPoints = self.nPoints,
                                       minLength = self.minLength,
                                       maxLength = self.maxLength)
        self.network.setYears( self.nYears)
        self.network.addPaths( [ self.populatedPath1, self.populatedPath2 ])        
        self.network.addNodes( [ self.node1, self.node2] )
        self.network.calculateNetworkPop()
        self.assertEqual( self.network.showNetworkPop()[0], 102.08333333333333)

class test_csvPopulate( unittest.TestCase):

    def test_networkCreation(self):
        ## Load files 
        self.inputFolder = "./inputParameters/"
        self.groupsFile = self.inputFolder + 'twoNodeTestGroups.csv'
        self.dfGroups = pd.read_csv(self.groupsFile)
        
        self.nodeFile = self.inputFolder + 'twoNodeTestNodes.csv'
        self.dfNode = pd.read_csv(self.nodeFile)
        
        self.networkFile = self.inputFolder + 'twoNodeTestNetwork.csv'
        self.dfNetwork = pd.read_csv(self.networkFile)
        
        ## Test creation of network 
        self.createNetwork = nmp.createNetworkFromCSV( self.dfNetwork)

        ## Test addition of nodes
        self.createNetwork.addNodesFromCSV( self.dfNode)

        ## Test addition of groups 
        self.createNetwork.addGroupsFromCSV( self.dfGroups)
        
        ## Export and test network 
        self.network = self.createNetwork.showNetwork()
        
        self.assertEqual( self.network.showNetworkName(), 'twoNodeNetwork')
        self.assertEqual( self.network.nYears, 50)
        self.assertEqual( len(self.network.omega), 200)
        self.assertEqual( len(self.network.nodes), 2)
        self.assertEqual( self.network.nodes[0].pathsOut, {'path 1': 0.05})
        self.assertEqual( self.network.nodes[1].pathsOut, {'path 2': 0.05, 'path 3': 0.0})
        self.assertEqual( self.network.nodes[0].showPathsIn(), ['path 2'])
        self.assertEqual( self.network.nodes[1].showPathsIn(), ['path 1', 'path 4'])


        self.assertEqual( self.network.nodes[0].groups[0].groupName, 'test group 1') 

        
if __name__ == '__main__':
    unittest.main()
