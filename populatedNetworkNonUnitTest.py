import networkModelPopulate as nmp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
''' 
Ths file tests functions that do now work with unit testing
such as plots and print to screen functions 
'''

inputFolder = "./inputParameters/"
groupsFile = inputFolder + 'twoNodeTestGroups.csv'
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + 'twoNodeTestNodes.csv'
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + 'twoNodeTestNetwork.csv'
dfNetwork = pd.read_csv(networkFile)




## NEXT AREA WILL BE REPLACED BY READ FROM CSV FILES


node1 = nmp.populatedNode('test node 1')
node2 = nmp.populatedNode('test node 2')

group1 = nmp.group('test group')

nPoints = 50
nYears = 3
minLength = 1
maxLength = 450

group1.createPopDist( nYears = nYears, nPoints = nPoints, popDist0 = np.array(range(nPoints))/20.0)
group1.setGrowth( nmp.growthVB( 180.0, 0.16, 10.0) )
group1.setSurvival(  nmp.logistic( 40.0, -5.0, 0.0, 1.0) )
group1.setProbabilityOfReproducing( nmp.logistic( 40.0, -5.0, 0.0, 1.0))
group1.setEggTransition(1.0e-3)
group1.setEggPerkg( 200.0)
group1.setMuJ( np.log(10.0))
group1.setSigmaJ( 1.1)
group1.setLengthWeight( nmp.lengthWeight(alphaLW = 1.0,
                                         betaLW  = 2.0) )
group1.setRecruitment( nmp.linearRecruitment( lengthWeight = group1.lengthWeight,
                                              survival = group1.survival,
                                              probabilityReproducing = group1.probabilityOfReproducing,
                                              eggTransition = group1.eggTransition,
                                              eggPerkg = group1.eggPerkg,
                                              muJ = group1.muJ,
                                              sigmaJ = group1.sigmaJ) )
group1.setDensity( nmp.densityNegExp(a = 1.0,
                                     b = 1e-6) )


node1.addGroups( [group1 ])
node1.addPathsOut( [ {'path 1': 0.2} ] )

group2 = nmp.group('test group')
group2.createPopDist( nYears = nYears, nPoints = nPoints, popDist0 = np.array(range(nPoints))/30.0)
group2.setGrowth( nmp.growthVB( 180.0, 0.16, 10.0) )
group2.setSurvival(  nmp.logistic( 40.0, -5.0, 0.0, 1.0) )
group2.setProbabilityOfReproducing( nmp.logistic( 40.0, -5.0, 0.0, 1.0))
group2.setEggTransition(1.0e-3)
group2.setEggPerkg( 200.0)
group2.setMuJ( np.log(10.0))
group2.setSigmaJ( 1.1)
group2.setLengthWeight( nmp.lengthWeight(alphaLW = 1.0,
                                         betaLW  = 2.0) )
group2.setRecruitment( nmp.linearRecruitment( lengthWeight = group2.lengthWeight,
                                              survival = group2.survival,
                                              probabilityReproducing = group2.probabilityOfReproducing,
                                              eggTransition = group2.eggTransition,
                                              eggPerkg = group2.eggPerkg,
                                              muJ = group2.muJ,
                                              sigmaJ = group2.sigmaJ) )
group2.setDensity( nmp.densityNegExp(a = 1.0,
                                     b = 1e-6) )


node2.addGroups( [group2 ])      
node2.addPathsIn(  [ 'path 1'])


node2.addPathsOut( [ {'path 2': 0.2} ] )
node1.addPathsIn( ['path 2'] )

populatedPath1 = nmp.populatedPath('path 1')
populatedPath1.addStartNode('test node 1')
populatedPath1.addEndNode('test node 2')        

populatedPath2 = nmp.populatedPath('path 2')
populatedPath2.addStartNode('test node 2')
populatedPath2.addEndNode('test node 1')        

pathGroup1 = nmp.group('test group')
pathGroup1.createPopDist( nYears = nYears, nPoints = nPoints)
populatedPath1.addGroups( [pathGroup1])

pathGroup2 = nmp.group('test group')
pathGroup2.createPopDist( nYears = nYears, nPoints = nPoints)
populatedPath2.addGroups( [pathGroup2])


network = nmp.populatedNetwork('test network')
network.setupNetworkMesh( nPoints = nPoints, minLength = minLength, maxLength = maxLength)
network.setYears( nYears)
network.addPaths( [ populatedPath1, populatedPath2 ])        
network.addNodes( [ node1, node2] )


## END OF CODE CHUNCK TO BE ADDED TO READ CSV FILE AREA 
## Check describe network function
network.describeNetwork()

## Check simulate network here 
network.runSimulation()
        


## Check plot 
network.calculateNetworkPop()
network.showNetworkPop()
network.plotAllNodes()

## Change self back to network

# def plotAllNodes(self, outName = None, showPlot = True, showGroups = False, saveData = None):


