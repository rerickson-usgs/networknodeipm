import networkModel as nm
import numpy as np
import scipy.stats as stats
import sys 
import matplotlib.pyplot as plt
import pandas as pd


class populatedHelpers:
    ''' Helper funcitons that are coded in one place to avoid repeating'''
    
    def addGroups(self, groups):
        for grp in groups:
            self.groups.append( grp)

    def showGroups(self):
        return self.groups

    def setLengthWeight(self, lengthWeight):
        self.lengthWeight = lengthWeight
        
    def createPopDist(self, nYears, nPoints, popDist0 = None):
        if popDist0 is None:
            self.popDist0 = np.zeros(nPoints)
        else:
            self.popDist0 = popDist0
            
        self.popDist = np.zeros( (nYears + 1, nPoints))
        self.popDist[ 0, :] = self.popDist0

    def showPop(self):
        return self.popDist.sum(1)
        
    def showPopDist(self):
        return self.popDist

    def showPopDistYear(self, year):
        return self.popDist[ year, :]
    
    def updatePopDistYear(self, year, popAdd):
        self.popDist[ year, :] += popAdd

class logistic:
    '''Defines a logistic function.''' 
    def __init__(self, alphaL, betaL, minL, maxL):
        self.alphaL = alphaL
        self.betaL = betaL
        self.minL = minL
        self.maxL = maxL       

    def __call__(self, z):
        out = ( self.minL + 
                (self.maxL - self.minL) / 
                ( 1 + np.exp( self.betaL * ( np.log(z) - np.log(self.alphaL)))) )
        return out

   
class densityNegExp:
    '''Define a function where density has a negative exponential impact on the system.'''
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self, biomass):
        out = self.a * np.exp( -1 *  self.b  * biomass)
        return out 
    
class lengthWeight:
    '''Define a relationship between length and weight.'''
    def __init__(self, alphaLW, betaLW):
        self.alphaLW = alphaLW
        self.betaLW  = betaLW

    def __call__(self, omega):
        out = 10 ** (self.alphaLW +
                     np.log10(omega) * self.betaLW)
        return out

class growthVB:
    '''
    Define a von Bertalanffy growth function that maps the length at a 
    current year to the probability of length at a future year. 
    '''
    def __init__(self, aG, kG, sigmaG):
        self.aG = aG
        self.kG = kG
        self.sigmaG = sigmaG

    def __call__(self, zIn, zPrimeIn):
        z = np.atleast_1d(zIn)
        zPrime = np.atleast_1d(zPrimeIn)

        out = np.zeros( ( len(zPrime), len(z) ))
        
        for index in range(0, len(z)):
            out[ : , index ] = stats.norm.pdf(x = zPrime, 
                                            loc = (1 - self.kG) * z[index] + self.kG * self.aG,
                                            scale = self.sigmaG)
        return(out)

    
class populatedPath( nm.path, populatedHelpers):
    def __init__(self, pathName):
        self.pathName = pathName
        self.groups = []
        self.startNode = ''
        self.endNode = ''


class populatedNode( nm.node, populatedHelpers):
    def __init__(self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsIn = []
        self.pathsOut = {}

    def addPathsOut(self, pathsOutInput):
        if type(pathsOutInput) is dict:
            self.pathsOut.update( pathsOutInput)
        elif type(pathsOutInput) is list:
            [self.pathsOut.update(pO) for pO in pathsOutInput]

    def calculateNodeBiomass(self, omega, year):
        self.nodeBiomass  = 0.0
        for grp in self.groups:
            self.nodeBiomass += np.sum( grp.showPopDistYear( year) * grp.lengthWeight( omega) )

    def showNodeBiomass(self):
        return self.nodeBiomass
               
    def projectGroups(self, year, omega, hWidth, nodeBiomass):
        '''  projects population using midpoint rule.
             First dotproduct is growth/maturation.
             Second dotproduct is recruitment.
        '''
        year = year
        omega = omega
        hWidth = hWidth
        nodeBiomass = nodeBiomass
        for grp in self.groups:
            popAdd = ( np.dot( hWidth * grp.growth( omega, omega), 
                                    grp.showPopDistYear( year) *
                                    grp.survival( omega) ) +
                            np.dot(hWidth * grp.recruitment( omega, omega),
                                   grp.showPopDistYear( year)) *  grp.density(nodeBiomass)
            )


            grp.updatePopDistYear( year + 1, popAdd)
            
                
            
    def calculateNodePop(self):
        self.populationDistribution = 0.0
        for grp in self.groups:
            self.populationDistribution += grp.showPopDist()
        self.population = self.populationDistribution.sum(1)

    def showNodePopulation(self):
        return self.population

    def showNodePopulationDist(self):
        return self.populationDist
    
class linearRecruitment:
    '''Define a function that models the recruitment as a function of fish length.'''
    def __init__( self, lengthWeight, survival, probabilityReproducing,
                  eggTransition, eggPerkg, muJ, sigmaJ):

        self.muJ = muJ
        self.sigmaJ = sigmaJ     
        self.lengthWeight = lengthWeight
        self.survival = survival
        self.probabilityReproducing = probabilityReproducing
        self.eggTransition = eggTransition
        self.eggPerkg = eggPerkg
        
    def __call__(self, omega, omegaPrime):
        omega      = np.atleast_1d(omega)
        omegaPrime = np.atleast_1d(omegaPrime)

        out = np.zeros( (len(omegaPrime), len(omega) ))

        for index, val in enumerate(omega):
            out[ :, index] = ( self.eggTransition *
                               self.eggPerkg *
                               self.survival( val ) *
                               self.probabilityReproducing( val ) * 
                               self.lengthWeight( val) *
                               (stats.lognorm.pdf(omegaPrime,
                                                  loc = 0,
                                                  s = self.sigmaJ,
                                                  scale = self.muJ) / 
                                stats.lognorm.pdf(omegaPrime,
                                                  loc = 0,
                                                  s = self.sigmaJ,
                                                  scale = self.muJ).sum())
            )
            
        return(out)

    
class group( populatedHelpers ):
    def __init__(self, groupName):
        self.groupName = groupName
        
    def showGroupName(self):
        return self.groupName

    def setSurvival(self, survival):
        self.survival = survival

    def setGrowth(self, growth):
        self.growth = growth

    def setProbabilityOfReproducing(self, probabilityOfReproducing):
        self.probabilityOfReproducing = probabilityOfReproducing

    def setEggTransition(self, eggTransition):
        self.eggTransition = eggTransition

    def setEggPerkg(self, eggPerkg):
        self.eggPerkg = eggPerkg

    def setMuJ(self, muJ):
        self.muJ = muJ

    def setSigmaJ(self, sigmaJ):
        self.sigmaJ = sigmaJ

    def setRecruitment(self, recruitment):
        self.recruitment = recruitment
        
    def setDensity(self, density):
        self.density = density 

    def setLengthWeight(self, lengthWeight):
        self.lengthWeight = lengthWeight 

        
class populatedNetwork( nm.network):
    def __init__(self, networkName):
        self.networkName = networkName
        self.nodes = []
        self.paths = []

    def setYears(self, nYears):
        self.nYears = nYears
        
    def moveGroups( self, startYear, endYear):    
        #####################
        ## Run movement in three steps
        ## First, copy individuals onto a path
        for p in self.paths:
            for nodeStart in self.nodes:
                if nodeStart.showNodeName() is p.showStartNode():
                    p.groups = [ nodeStart.pathsOut[ p.showPathName() ] *
                                 grp.showPopDistYear( startYear) for grp in nodeStart.groups ]
                                
        ## Second, unload paths
        for p in self.paths:
            for nodeEnd in self.nodes:
                if nodeEnd.showNodeName() is p.showEndNode():
                    if len(nodeEnd.groups) != len(p.groups):
                        sys.exit("There are not the same number of groups in the node as there is in the pathway")
                    else:
                        for index in range(0, len(nodeEnd.showGroups())):
                            nodeEnd.groups[index].popDist[ endYear, :] += p.groups[index] 
            
        # ## Third, remove migrants from their original nodes 
        for p in self.paths:
            for nodeStart in self.nodes:
                if nodeStart.showNodeName() is p.showStartNode():
                    if len(nodeStart.groups) != len(p.groups):
                        sys.exit("There are not the same number of groups in the node as there is in the pathway")
                    else:
                        for index in range(0, len(nodeStart.groups)):
                            nodeStart.groups[index].popDist[ endYear, :] += -1.0 * p.groups[index] 

    def calculateNetworkPop(self):

        self.population = 0.0
        
        for n in self.nodes:
            n.calculateNodePop()
            self.population += n.showNodePopulation()

    def showNetworkPop(self):
        return self.population

    def describeNetwork(self):
        print str(self.networkName) + ' is a network with ' + str(self.nNodes()) + ' nodes.'


    def plotAllNodes(self, outName = None, showPlot = True, showGroups = False, saveData = None):
        nCol =  int(np.ceil(np.sqrt(self.nNodes())))
        nRow =  int(np.floor(np.sqrt(self.nNodes())))

        tPlot, ax = plt.subplots(
            nrows = nRow, ncols= nCol, sharex=True, sharey=True
        )

        plotNodePop = np.zeros( (self.nYears + 1, self.nNodes()))
        for index in xrange(self.nNodes()):
            plotNodePop[ : , index] = self.nodes[index].showNodePopulation()
            ax[index].plot(np.arange(0,  self.nYears +1 , 1),  plotNodePop[ :, index])
        if showGroups:
            for grp in self.nodes[index].groups:
                ax[index].plot( np.arange(0, self.nYears +1, 1), grp.showPop())      
                ax[index].set_title(self.nodes[index].nodeName)
                ax[index].set_xlabel("Time (years)")
                ax[index].set_ylabel("Population")
            
        if showPlot:
            plt.show()

        if outName is not None:
            plt.savefig( outName )

        if saveData is not None:
            nodeNames = [node.showNodeName() for node in self.nodes]
            popDF = pd.DataFrame( plotNodePop, columns = nodeNames)
            popDF.to_csv(saveData, index = False)

    def setupNetworkMesh( self, nPoints, minLength, maxLength):
        self.nPoints = nPoints
        self.minLength = minLength
        self.maxLength = maxLength

        self.omega = np.linspace( start = self.minLength, stop = self.maxLength, num = self.nPoints + 2)[1:-1]
        self.hWidth = self.omega[1] - self.omega[0]

        
    def runSimulation(self):
        ''' This function runs the network simulation and assumes movement occures before spawning.'''

        for yearIndex in xrange(self.nYears):
            ## Step 1, move groups 
            self.moveGroups( yearIndex, yearIndex)
            ## Step 2, update popualtions within nodes
            for n in self.nodes:
                ## Step 2a: calculate biomass in each node and density effect 
                n.calculateNodeBiomass( omega = self.omega, year = yearIndex)
                n.projectGroups(yearIndex, self.omega, self.hWidth, nodeBiomass = n.showNodeBiomass())


class createNetworkFromCSV:
    '''contains functions to populate a network from csv files'''
    
    def __init__(self, dfNetwork):
        self.network = populatedNetwork( dfNetwork['networkName'][0] )
        self.network.setYears( dfNetwork['nYears'][0] )
        self.network.setupNetworkMesh( dfNetwork['nPoints'][0],
                                       dfNetwork['minLength'][0],
                                       dfNetwork['maxLength'][0])

    def showNetwork(self):
        return self.network 
    
    def pathOutListFunction( self, pathsOut, pathsOutProb):
        '''
        Function used to convert path names and probabilities from lists 
        (e.g., from CSV files) into a dictionary for the model.
        '''
        pathsOutTemp = dict()
        if isinstance(pathsOutProb, float):
            pathsOutTemp[pathsOut] = pathsOutProb
        else:
            pathsOut2 = pathsOut.strip().split(";")
            pathsOutProb2 = [float(x) for x in pathsOutProb.strip().split(";")]
            for index, pth in enumerate(pathsOut2):
                pathsOutTemp[pth] = pathsOutProb2[index]
        return pathsOutTemp

    def addNodesFromCSV( self, dfNode ):

        ## Extract out nodes from the network we are using
        ## (this allows a yet to be implement function for generating multiple networks from one set of files)
        dfNodeUse = dfNode.query(str('network == ' + "'" + self.network.showNetworkName() + "'"))
     
        ## Loop through each node in the network and generate it
        for nodeRow in dfNodeUse.iterrows():
            ## Add in node's name
            nodeTemp =  populatedNode( nodeName = nodeRow[1]['nodeName'])
            pathsOutTemp = self.pathOutListFunction( nodeRow[1]['pathsOut'],
                                                          nodeRow[1]['pathsOutProb'])
            nodeTemp.addPathsOut( pathsOutTemp)
            nodeTemp.addPathsIn( nodeRow[1]['pathsIn'].split(";"))           
            self.network.addNodes([ nodeTemp])



    def standarizedLogNormal(self, omega,  sIn, scaleIn):                     
        ( stats.lognorm.pdf( omega, loc = 0, s = sIn, scale = scaleIn) /
          stats.lognorm.pdf( omega, loc = 0, s = sIn, scale = scaleIn).sum() )
                             
    
    def addGroupsFromCSV( self, dfGroups):
        ## Loop through nodes and add in groups
        for n in self.network.nodes:
            dfGroupsUse = dfGroups.query(str('network == ' + "'" +
                                             self.network.networkName + "'" + 
                                             ' & node == ' + "'" + 
                                             n.showNodeName() + "'" ))
            ## Loop through each group in a node and generate it
            for groupRow in dfGroupsUse.iterrows():
                grpTemp = group( groupRow[1]['groupName'] )
                grpTemp.setLengthWeight( lengthWeight(groupRow[1]['alphaLW'],
                                                      groupRow[1]['betaLW']) )
                grpTemp.setDensity( densityNegExp(a = groupRow[1]['densityA'],
                                                  b = groupRow[1]['densityB']) )
                grpTemp.setSurvival( logistic( alphaL = groupRow[1]['alphaS'],
                                               betaL = groupRow[1]['betaS'],
                                               minL = groupRow[1]['minS'],
                                               maxL = groupRow[1]['maxS']) )
                grpTemp.createPopDist( nYears = self.network.nYears,
                                       nPoints = self.network.nPoints,
                                       popDist0 =
                                       self.standarizedLogNormal(
                                           self.network.omega,
                                           sIn = groupRow[1]['initS'], 
                                           scaleIn = groupRow[1]['initMean']) )
                grpTemp.setGrowth( growthVB(aG = groupRow[1]['aG'],
                                            kG = groupRow[1]['kG'],
                                            sigmaG = groupRow[1]['sigmaG']) )
                #########==========
    ## AM HERE EDITING CODE
    ## Next steps are to add in all of groups attributes to group
    ## And then update linear recruitment to function to call internally rather than need inputs
    ## probably use if statements for input arguments 
            
                
                n.addGroups( [ grpTemp])

    #         probabilityReproducingTemp = logistic( alphaL =  groupRow[1]['alphaR'], betaL =  groupRow[1]['betaR'],
    #                                                      minL =  groupRow[1]['minR'], maxL = groupRow[1]['maxR'])
    #         recruitmentTemp = linearRecruitment(omega = omegaIn,
    #                                                   lengthWeight = lengthWeightUseTemp,
    #                                                   probabilityReproducing = probabilityReproducingTemp,
    #                                                   survival = survivalTemp,
    #                                                   eggTransition = groupRow[1]['eggTransition'],
    #                                                   eggPerkg = groupRow[1]['eggPerkg'],
    #                                                   muJ = np.log(groupRow[1]['muJ']), sigmaJ = np.log(groupRow[1]['sigmaJ']))
    #         try:
    #             pulseIntro = groupRow[1][ 'pulseIntro']
    #         except:
    #             pulseIntro = "No"

    #         try:
    #             groupImpactViability = groupRow[1][ 'groupImpactViability']
    #         except:
    #             groupImpactViability = False

    #         try:
    #             groupOffspringViability = float(groupRow[1]['groupOffspringViability'])
    #         except:
    #             groupOffspringViability = 1.0
                

    #         if 'groupOffspringPfemale' in groupRow[1]:
    #             groupOffspringPfemale = float(groupRow[1]['groupOffspringPfemale'])
    #         else:
    #             groupOffspringPfemale = 0.5

    #         if 'groupImpactSexRatio' in groupRow[1]:
    #             groupImpactSexRatio =  groupRow[1]['groupImpactSexRatio']
    #             if not isinstance(groupImpactSexRatio, bool):
    #                 print groupImpactSexRatio
    #                 sys.exit("groupImpactSexRatio must be True or False")
    #         else:
    #            groupImpactSexRatio = False

    #         groupTemp = group(groupName = groupRow[1][ 'groupName'],
    #                           groupSex =  groupRow[1][ 'groupSex'],
    #                           groupOffspringPfemale = groupOffspringPfemale,
    #                           groupProduceEggs = groupRow[1][ 'groupProduceEggs'], 
    #                           popSize0 = groupRow[1][ 'popSize0'],
    #                           groupImpactViability = groupImpactViability,
    #                           groupOffspringViability = groupOffspringViability,
    #                           popLenDist0 = popLenDist0Temp, 
    #                           omega = omegaIn,
    #                           nYears = dfNetwork['nYears'][0], 
    #                           survival = survivalTemp, 
    #                           growth = growthTemp,
    #                           recruitment = recruitmentTemp,
    #                           density = densityTemp,
    #                           lengthWeight = lengthWeightUseTemp,
    #                           pulseIntroductionString = pulseIntro,
    #                           groupImpactSexRatio = groupImpactSexRatio)
    #         groupsForNodeTemp.append(groupTemp)
    #     ## Add groups to each node and then add nodes to temp node list
    #     nodeTemp.addGroupList(groupsForNodeTemp)
    #     nodes.append( nodeTemp)
    # ## Add nodes to the network and then create the paths 
    # networkOut.addNodeList(nodes)
    # networkOut.initializePaths()

    
