## The first part of this code enters parameter values that are used for all node.
## Next, a simple one node system is created to make sure the network functions work (which currently do not).
## The third section creates a 2 node system.

## Projection to dos:
## 0) Get migraiton working
## 1) Write a function to load a csv of possible parameter values
## 2) Get plotting working correctly (less important, but still usefull

## add in checker to make sure all groups are in the same order in all nodes

import numpy as np
import scipy.stats as stats
import networkNodeIPM  as nnIPM

## Setup numerical mesh, currently uses midpoint rule
minLength = 0
maxLength = 300
nPoints = 200
omega = np.linspace( start = minLength, stop = maxLength, num = nPoints +2)[1:-1]

## Denisty parameter and distribution 
a = 1
b = 1e-6 # 6e-7 # 1e-3

density = nnIPM.densityNegExp(a = a, b = b)

## Node's survival parameters and function
minS = 0.1
maxS = 0.9
alphaS = 40 # inflection point
betaS  =  -5 # slope

survival = nnIPM.logestic( alphaL = alphaS, betaL = betaS, minL = minS, maxL = maxS)

## Initial population length and size 
initMean = 150
popLenDist0 = (stats.lognorm.pdf(omega, loc = 0, s = 0.2, scale = initMean) /
               stats.lognorm.pdf(omega, loc = 0, s = 0.2, scale = initMean).sum() )
popSize0node1female = 6.0e3 * 0.5
popSize0node1male = 6.0e3 * 0.5

## Growth parametesr and function
aG = 180
kG = 0.16
sigmaG = 10
growth = nnIPM.growthVB(aG = aG, kG = kG, sigmaG = sigmaG)

## the probabilty of reproducing and its function
minR = 0
maxR = 1.0
alphaR = 40
betaR  = -4
probabilityReproducing = nnIPM.logestic( alphaL = alphaR, betaL = betaR, minL = minR, maxL = maxR)

## Age-1 length dist, J is for "juvenile"
muJ = np.log(10)
sigmaJ = np.log(2)

## relationship between length and weigth and its function
alphaLW = -4.33
betaLW = 2.77
lengthWeightUse = nnIPM.lengthWeight( alphaLW, betaLW)

## Recruitment function and required parameter not previously defined
eggPerkg = 5e6 # old default is 5e3
eggTransition = 3e-3  # 3e-3 ## Prob of making it from egg to age-1 fish 
recruitment = nnIPM.linearRecruitment(omega = omega,
                                      lengthWeight = lengthWeightUse,
                                      probabilityReproducing = probabilityReproducing,
                                      survival = survival,
                                      eggTransition = eggTransition, eggPerkg = eggPerkg,
                                      muJ = muJ, sigmaJ = sigmaJ)

## Create a recruitment function that produces no oppsring
recruitment0 = nnIPM.linearRecruitment(omega = omega,
                                       lengthWeight = lengthWeightUse,
                                       probabilityReproducing = probabilityReproducing,
                                       survival = survival,
                                       eggTransition = 0, eggPerkg = 0,
                                       muJ = muJ, sigmaJ = sigmaJ)

## Simulation parameters
nYears = 5

## Specify stocking of YY-males

## Define groups
node1group1female = nnIPM.group(groupName = "Node 1, females",
                                groupSex =  "female",
                                groupProduceEggs = True, 
                                popSize0 = popSize0node1female, 
                                popLenDist0 = popLenDist0, 
                                omega = omega,
                                nYears = nYears, 
                                survival = survival, 
                                growth = growth,
                                recruitment = recruitment,
                                density = density,
                                lengthWeight = lengthWeightUse)

node1group1male =   nnIPM.group(groupName = "Node 1, males",
                                groupSex =  "male",
                                groupProduceEggs = False, 
                                popSize0 = popSize0node1male, 
                                popLenDist0 = popLenDist0, 
                                omega = omega,
                                nYears = nYears, 
                                survival = survival, 
                                growth = growth,
                                recruitment = recruitment,
                                density = density,
                                groupImpactSexRatio = True,
                                lengthWeight = lengthWeightUse)




node1 = nnIPM.node("node 1")

## Add in groups to nodes 
node1.addGroupList( [node1group1male, node1group1female] )


## Make sure nodes present in the group 
node1.describeNodes()

oneNodeSystem = nnIPM.networkModel("one node", nYears = nYears, omega = omega)
nodesIn = [node1]
oneNodeSystem.addNodeList(nodesIn)

# oneNodeSystem.runNetworkSimulation()

# onenodesystem.plotAllNodeGroups()
# oneNodeSystem.nodes
## use https://stackoverflow.com/questions/1358977/how-to-make-several-plots-on-a-single-page-using-matplotlib
## to plot multiple subplots of all nodes in one pane 

## Setup system with one full and one empy node, no YY-males


node1group1female = nnIPM.group(groupName = "Node 1, females",
                                groupSex =  "female",
                                groupProduceEggs = True, 
                                popSize0 = popSize0node1female, 
                                popLenDist0 = popLenDist0, 
                                omega = omega,
                                nYears = nYears, 
                                survival = survival, 
                                growth = growth,
                                recruitment = recruitment,
                                density = density,
                                lengthWeight = lengthWeightUse)

node1group1male =   nnIPM.group(groupName = "Node 1, males",
                                groupSex =  "male",
                                groupProduceEggs = False, 
                                popSize0 = popSize0node1male, 
                                popLenDist0 = popLenDist0, 
                                omega = omega,
                                nYears = nYears, 
                                survival = survival, 
                                growth = growth,
                                recruitment = recruitment,
                                density = density,
                                groupImpactSexRatio = False,
                                lengthWeight = lengthWeightUse)


node2group1female = nnIPM.group(groupName = "Node 2, females",
                                groupSex =  "female",
                                groupProduceEggs = True,
                                popSize0 = 0, 
                                popLenDist0 = popLenDist0, 
                                omega = omega,
                                nYears = nYears, 
                                survival = survival, 
                                growth = growth,
                                recruitment = recruitment,
                                density = density,
                                lengthWeight = lengthWeightUse)

node2group1male =   nnIPM.group(groupName = "Node 2, males",
                                groupSex =  "male",
                                groupProduceEggs = False, 
                                popSize0 = 0, 
                                popLenDist0 = popLenDist0, 
                                omega = omega,
                                nYears = nYears, 
                                survival = survival, 
                                growth = growth,
                                recruitment = recruitment,
                                density = density,
                                groupImpactSexRatio = False,
                                lengthWeight = lengthWeightUse)


node1 = nnIPM.node("node 1")
node2 = nnIPM.node("node 2")

## Add in groups to nodes 
node1.addGroupList( [node1group1male, node1group1female] )
node2.addGroupList( [node2group1male, node2group1female] )

## Add in paths to nodes
node1PathsOut = {"node 2": 1.00}
node1PathsIn = ["node 1"]

node1.addPathsOut(node1PathsOut)
node1.addPathsIn(node1PathsIn)

node2PathsOut = {"node 1": 0.1}
node2PathsIn = ["node 2"]

node2.addPathsOut(node2PathsOut)
node2.addPathsIn(node2PathsIn)

# ## Add nodes to network
twoNodeSystem = nnIPM.networkModel("two nodes, one empty", nYears = nYears, omega = omega)
nodesIn2 = [node1, node2]
twoNodeSystem.addNodeList(nodesIn2)
print twoNodeSystem.nNodes()    

twoNodeSystem.initializePaths()
twoNodeSystem.describePaths()

twoNodeSystem.runNetworkSimulation()

[node.calculateNodePopulaiton() for node in twoNodeSystem.nodes]
dummy = [node.plotNodePop(nYears) for node in twoNodeSystem.nodes]

print "Done"



