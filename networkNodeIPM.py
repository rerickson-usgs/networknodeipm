import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.gridspec 
import pandas as pd
import sys


def pathOutListFunction( pathsOut, pathsOutProb):
    '''Funciton used to convert path names and probabilities from lists (e.g., from CSV files) into a dictionary for the model.'''
    pathsOutTemp = dict()
    if isinstance(pathsOutProb, float):
        pathsOutTemp[pathsOut] = pathsOutProb
    else:
        pathsOut2 = pathsOut.strip().split(",")
        pathsOutProb2 = [x for x in pathsOutProb.strip().split(",")]
        for index, pth in enumerate(pathsOut2):
            pathsOutTemp[pth] = pathsOutProb2[index]
    return pathsOutTemp


class densityNegExp:
    '''Define a function where density has a negative exponential impact on the system.'''
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self, biomass):
        out = self.a * np.exp( -1 *  self.b  * biomass)
        return out 

def densityNone(biomass):
    '''Define a function where density has no impact on the system.'''
    return 1 
    
class lengthWeight:
    '''Define a relationship between length and weight.'''
    def __init__(self, alphaLW, betaLW):
        self.alphaLW = alphaLW
        self.betaLW  = betaLW
    def __call__(self, omega):
        out = 10 ** (self.alphaLW +
                     np.log10(omega) * self.betaLW)
        return out

class logestic:
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

class linearRecruitment:
    '''Define a function that models the recruitment asa function of fish length.x'''
    def __init__( self, omega, lengthWeight, survival, probabilityReproducing, eggTransition, eggPerkg, muJ, sigmaJ):
        self.juvenile = (stats.lognorm.pdf(omega, loc = 0, s = sigmaJ, scale = muJ) / 
                         stats.lognorm.pdf(omega, loc = 0, s = sigmaJ, scale = muJ).sum())
        self.lengthWeight = lengthWeight
        self.survival = survival
        self.probabilityReproducing = probabilityReproducing
        self.eggTransition = eggTransition
        self.eggPerkg = eggPerkg
        
    def __call__(self, omega, omegaPrime):
        omega      = np.atleast_1d(omega)
        omegaPrime = np.atleast_1d(omegaPrime)
        out = np.zeros( ( len(omegaPrime), len(omega) ))
        for index in range(0, len(omega)):
            out[ : , index ] = ( self.eggTransition * self.eggPerkg * self.survival(omega) * self.probabilityReproducing(omega) * 
                                 self.lengthWeight(omega) * self.juvenile )
        return(out)
   
class group:
    ''' The group class is the group of inviduals of a give "sex", e.g., males, females, YY-males, sterile males, ect.'''

    ## I think I will want to include omega, nYears, nSizeBins, and sizeBins from the network
    ## Also, I might want to include checks to make sure the popSize0 and popLenDist0 are in the correct format
    def __init__(self, groupName, popSize0, popLenDist0, omega,
                 nYears, survival, growth, recruitment, density, lengthWeight,
                 groupProduceEggs = False, 
                 groupImpactSexRatio  = False,
                 groupOffspringPfemale = 0.5,
                 groupImpactViability = False,
                 groupOffspringViability = 1.0, 
                 pulseIntroduction = None,
                 pulseIntroductionString = "No",
                 adultSurvivalMultiplier = None,
                 groupSex = None):

        self.popLenDist0 = popLenDist0
        self.groupProduceEggs = groupProduceEggs
        self.groupImpactSexRatio = groupImpactSexRatio
        self.groupImpactViability = groupImpactViability
        self.nYears = nYears
        self.groupSex = groupSex
        self.groupName = groupName
        self.popSize = np.zeros(nYears + 1)
        self.popSize[0] = popSize0
        self.popLenDist = np.zeros( (nYears + 1, len(omega)))
        self.popLenDist[0, :] = self.popLenDist0 * popSize0
        self.survival = survival
        self.growth = growth
        self.recruitment = recruitment
        self.density = density
        self.lengthWeight = lengthWeight
        self.groupOffspringPfemale =  groupOffspringPfemale 
        self.groupOffspringViability = groupOffspringViability
        self.omega = omega
        self.hWidth = self.omega[1] - self.omega[0]      
        self.pulseIntroductionString = pulseIntroductionString

        
        ## Go through options for pulse introduction
        ## Neither method is used, use all zeros
        if self.pulseIntroductionString == "No" and pulseIntroduction is None:           
            self.pulseIntroduction = np.zeros( (nYears + 1, len(self.omega)))
        ## String not used, use pulseIntroduction value
        elif pulseIntroductionString == "No":          
            self.pulseIntroduction = pulseIntroduction
        ## input no specified, used string
        elif pulseIntroduction is None:
            nRelease, startRelease, stopRelease = [int(x) for x in  self.pulseIntroductionString.split(',')]
            self.pulseIntroduction = np.zeros( (nYears + 1, len(self.omega)))
            self.pulseIntroduction[ (startRelease - 1):stopRelease, :] = nRelease * self.popLenDist0

        ## Go include adult mortality
        if adultSurvivalMultiplier is None:
            self.adultSurvivalMultiplier = np.ones( (nYears + 1, len(self.omega)))
        else:
            self.adultSurvivalMultiplier = adultSurvivalMultiplier

            
    def timeStepGroup(self, t,
                      tPlusOne = None,
                      pReferenceGroupBirth = 0.5,
                      offspringViability = 1.0,
                      recruitGroup = None,
                      popLenDistbiomass = None,
                      referenceSex = "female"):
        ''' The annual time step dynamically changes the group's size through time.'''
        ## Kevin, is this the best way to do this?

        if tPlusOne is None:
            tPlusOne = t + 1
            
        self.offspringViability = offspringViability
        ## Hard wire function to calcuate pGroupBirth based upon sex,
        ## remember that pGroupBirth, by defult, referes to females 
        if self.groupSex == referenceSex:
            self.pGroupBirth = pReferenceGroupBirth
        else:
            self.pGroupBirth = 1 - pReferenceGroupBirth

        if recruitGroup is None:
            self.recruitGroup = self.popLenDist
        else:
            self.recruitGroup = recruitGroup     

        if popLenDistbiomass is None:
            self.popLenDistBiomass = self.popLenDist 
        else:
            self.popLenDistBiomass = popLenDistbiomass

        biomass = np.sum(self.popLenDistBiomass[ t, :] * self.lengthWeight(self.omega))
        decrease = self.density(biomass)

        self.popLenDist[ tPlusOne, : ] = ( np.dot( self.hWidth * self.growth( self.omega, self.omega),  ## The first dot product is maturation
                                               self.survival( self.omega) * self.popLenDist[t, :]) * self.adultSurvivalMultiplier[t, :] +
                                       np.dot( self.hWidth * self.recruitment( self.omega, self.omega), ## The second dod product is reruitment
                                               self.recruitGroup[t, :]) * decrease * self.pGroupBirth  * self.offspringViability + 
                                       self.pulseIntroduction[t, :]) ## Stocking numbers for group 

        self.popSize[ tPlusOne ] =  self.popLenDist[ tPlusOne, :].sum() ## May need to move this at some point


    def movement(self, immigration, emigration, t):        
        if immigration is None:
            self.immigration = np.zeros( (1, len(self.omega)))
        else:
            self.immigration = immigration

        if emigration is None:
            self.emigration = np.zeros( ( 1, len(self.omega)))
        else:
            self.emigration = emigration
            
        self.popLenDist[t, : ] = self.popLenDist[t, : ] + self.immigration - self.emigration              
        

        
    def showGroupPopSize(self):
        return self.popSize
    
    def showGroupProduceEggs(self):
        return self.groupProduceEggs
    
    def showGroupName(self):
        return self.groupName

    def showGroupImpactSexRatio(self):
        return self.groupImpactSexRatio

    def showGroupImpactViability(self):
        return self.groupImpactViability
    
    def showGroupSex(self):
        return self.groupSex
    
    def plotLengthTime(self):
        '''Plot the length of fish in a group through time'''
        if self.groupSex is None:
            self.groupSex = ""
                
        fig, ax = plt.subplots()
        for index in range(0, self.popLenDist.shape[0]):
            ax.plot(self.omega, self.popLenDist[ index, :])      
        plt.title("Length distributions " + self.groupName + " " + self.groupSex)
        plt.xlabel("Length")
        plt.ylabel("Population in size class")
        plt.show()

    def plotPop(self):
        '''Plot the total population size of fish through time'''
        if self.groupSex is None:
            self.groupSex = ""

        plt.plot(np.arange(0, self.nYears + 1, 1),  self.popSize)
        plt.title("Population size through time for " + self.groupName + " " + self.groupSex)
        plt.xlabel("Time (years)")
        plt.ylabel("Population of group (all lengths)")
        plt.show()

class node:
    ''' 
    The node class is a collection of groups that use the same spatial habitat (i.e., "node") at the same time.
    '''
    ## I think I will want to include omega, nYears, nSizeBins, and sizeBins from the network
    ## Also, I might want to include checks to make sure the popSize0 and popLenDist0 are in the correct format
    def __init__(self, nodeName, timePeriod = "All"):
        self.nodeName = nodeName
        self.groups = []
        self.pathsOut = {}
        self.pathsIn = []
        self.nodeBiomass = 0.0
        self.timePeriod = timePeriod

    def showTimePeriod(self):
        return self.timePeriod
    
    def listGroups(self):
        return [grp for grp in self.groups]
   
    def describeNodes(self):
        print self.nodeName + " contains the following groups:"
        print "Group name \t\t Node sex"
        for grp in self.groups:
            print grp.showGroupName() + "\t\t" + grp.showGroupSex()
            
    def addPathsOut(self, pathsOut):
        self.pathsOut.update(pathsOut)

    def addPathsIn(self, pathsIn):
        [ self.pathsIn.append( pI ) for pI in pathsIn]
        
    def addGroup(self,  groupName ):
        self.groups.append( groupName )

    def addGroupList(self,  groupList):
        [ self.groups.append( grp ) for grp in groupList]
        
    def nGroups(self):
        return len(self.groups)

    def showNodeName(self):
        return self.nodeName

    def calculateNodePopulaiton(self):
        self.nodePop =  np.sum([ grp.popLenDist.sum(1) for grp in self.groups], 0)

    def plotNodePop(self, nYears):
        '''Plot the total population size of fish through time'''
        self.nYears = nYears
                
        plt.plot(np.arange(0, self.nYears + 1, 1),  self.nodePop)
        plt.title("Population size through time for all groups at " + self.nodeName)
        plt.xlabel("Time (years)")
        plt.ylabel("Population of node (all lengths)")
        plt.show()

    
    def plotNodeGroups(self, nYears):
        '''Plot the population sizes of node and groups in node'''
        self.nYears = nYears 
        fig, ax = plt.subplots()
        ax.plot(np.arange(0, self.nYears + 1, 1),  self.nodePop)
        for grp in self.groups:
            ax.plot( np.arange(0, self.nYears + 1, 1), grp.popSize)      
        plt.title("Population size through time for all groups at " + self.nodeName)
        plt.xlabel("Time (years)")
        plt.ylabel("Population of node (all lengths)")
        plt.show()


class path:
    '''
    Paths are used in nodes to hold transitory popualtions.
    '''
    def __init__(self, start, end, startTimePeriod = "All", endTimePeriod = "All"):
        self.start = start
        self.end = end
        self.groups = []
        self.startTimePeriod = startTimePeriod 
        self.endTimePeriod   = endTimePeriod
        
    def showEnd(self):
        return self.end

    def showEndTimePeriod(self):
        return self.endTimePeriod

    def showStart(self):
        return self.start

    def showStartTimePeriod(self):
        return self.startTimePeriod

    def describePath(self):
        print "This path starts at " + self.start + " and ends at " + self.end + ". The time period transition (e.g., season) is " + self.showStartTimePeriod() + " to " + self.showEndTimePeriod()
        
class networkModel:
    ''' 
    The networkModel class is a collection of nodes and their interactions through time. 
    '''
    ## I think I will want to include omega, nYears, nSizeBins, and sizeBins from the network
    ## Also, I might want to include checks to make sure the popSize0 and popLenDist0 are in the correct format
    def __init__(self, networkName, nYears, omega, timePeriods = ["All"]):
        self.omega = omega
        self.networkName = networkName
        self.nodes = []
        self.paths = []
        self.timePeriods = timePeriods 
        self.nTimePeriods = len(self.timePeriods)
        self.nYears = nYears
        self.popLenDistbiomass = np.zeros(( nYears, len(omega)))
        self.eggProducingGroupLenDist = np.zeros(( nYears, len(omega)))

    def initializePaths(self):
        for nodeStart in self.nodes:
            for pathOut in nodeStart.pathsOut:
                for nodeEnd in self.nodes:
                    if pathOut == nodeEnd.showNodeName():
                        self.paths.append( path( start = nodeStart.showNodeName(),
                                                 end = nodeEnd.showNodeName(),
                                                 startTimePeriod = nodeStart.showTimePeriod(),
                                                 endTimePeriod   = nodeEnd.showTimePeriod()))

    def describePaths(self):
        [p.describePath() for p in self.paths]
        
    def addNodeList(self,  nodeList):
        [ self.nodes.append( node ) for node in nodeList]
        
    def nNodes(self):
        return len(self.nodes)
        
    def runNetworkSimulation(self):
        self.pReferenceGroupBirth = np.zeros(self.nYears) + 0.5
        self.offspringViabilityReduction = np.ones(self.nYears)

        ## Loop through all years
        for year in range(0, self.nYears):

            ## Loop through time periods (e.g., seasons)
            for tpIndex, tp in enumerate(self.timePeriods):
                print "year " + str(year) + " season " + tp
                pathsUse = [p for p in self.paths if p.showEndTimePeriod() == tp] ## Only use thats that end in current season
                for p in self.paths:
                    print p.showEndTimePeriod() == tp
                #####################
                ## Run migraiton in three steps
                ## First, copy individuals onto a path
                for p in pathsUse:
                    for nodeStart in self.nodes:
                        if nodeStart.showNodeName() is p.showStart():
                            p.groups = [ nodeStart.pathsOut[p.showEnd()] * grp.popLenDist[ year, :] for grp in nodeStart.groups]
                            
                # ## Second, unload paths
                for p in pathsUse:
                    for nodeEnd in self.nodes:
                        if nodeEnd.showNodeName() is p.showEnd():
                            if len(nodeEnd.groups) != len(p.groups):
                                sys.exit("There are not the same number of groups in the node as there is in the pathway")
                            else:
                                for index in range(0, len(nodeEnd.groups)):
                                    nodeEnd.groups[index].popLenDist[ year, :] += p.groups[index] 
            
                # ## Third, remove migrants from their original nodes 
                for p in pathsUse:
                    for nodeStart in self.nodes:
                        if nodeStart.showNodeName() is p.showStart():
                            if len(nodeStart.groups) != len(p.groups):
                                sys.exit("There are not the same number of groups in the node as there is in the pathway")
                            else:
                                for index in range(0, len(nodeStart.groups)):
                                    nodeStart.groups[index].popLenDist[ year, :] += -1.0 * p.groups[index] 

                ## Run through each node for population projection
                for node in self.nodes:
                    ## add up sum of egg producing groups
                    self.eggProducingGroupLenDist[ year, :] = np.sum([ grp.popLenDist[ year, :] for grp in node.groups if grp.showGroupProduceEggs()], 0)
                    
                    ## Check if any groups have YY-male like treatments
                    if all([grp.showGroupImpactSexRatio() is False for grp in node.groups]) is False:
                        self.pReferenceGroupBirth[year]  = ( np.sum([grp.groupOffspringPfemale *
                                                                     grp.popLenDist[ year, :].sum() for
                                                                     grp in node.groups if grp.showGroupImpactSexRatio()]) /
                                                             np.sum([ grp.popLenDist[ year, :].sum() for grp in node.groups if
                                                                      grp.showGroupImpactSexRatio()]) )
                        
                    # ## Check if any groups have non-viable offspring
                    if all([grp.showGroupImpactViability() is False for grp in node.groups]) is False:
                        self.offspringViabilityReduction[year]  = ( np.sum([grp.groupOffspringViability *
                                                                            grp.popLenDist[ year, :].sum() for
                                                                            grp in node.groups if grp.showGroupImpactViability()]) /
                                                                    np.sum([ grp.popLenDist[ year, :].sum() for grp in node.groups if
                                                                             grp.showGroupImpactViability()]) )
                        
                    self.popLenDistbiomass[ year, :] = np.sum([ grp.popLenDist[ year, :] for grp in node.groups], 0)

                    if tp == self.timePeriods[-1]:
                        tPlusOne = year + 1
                    else:
                        tPlusOne = year
                    
                    [ grp.timeStepGroup(t = year,
                                        tPlusOne = tPlusOne,
                                        pReferenceGroupBirth = self.pReferenceGroupBirth[year],
                                        recruitGroup = self.eggProducingGroupLenDist,
                                        offspringViability = self.offspringViabilityReduction[year],
                                        popLenDistbiomass = self.popLenDistbiomass) for grp in node.groups ]
    

    def describeNetwork(self):
        print str(self.networkName) + ' is a network with ' + str(self.nNodes()) + ' nodes.'
        print 'The network nodes include:'
        for node in self.nodes:
            node.describeNodes()
            if all([grp.showGroupImpactSexRatio() is False for grp in node.groups]) is False:
                print "Groups impact on sex ratio (first True/False), second impact:"
                print [grp.showGroupImpactSexRatio() is False for grp in node.groups]       
                print [grp.groupOffspringPfemale for grp in node.groups]
        print "The network includes the following paths"
        self.describePaths()

    def plotAllNode(self, outName = None, showPlot = True, showGroups = False):
        self.runNetworkSimulation()      
        nCol =  np.ceil(np.sqrt(self.nNodes()))
        nRow = np.floor(np.sqrt(self.nNodes()))

        tPlot, ax = plt.subplots(
            nrows=1, ncols= 2, sharex=True, sharey=True
        )

        for index in xrange(self.nNodes()):
            self.nodes[index].calculateNodePopulaiton()
            ax[index].plot(np.arange(0,  self.nYears + 1, 1),  self.nodes[index].nodePop)
            if showGroups:
                for grp in self.nodes[index].groups:
                    ax[index].plot( np.arange(0, self.nYears + 1, 1), grp.popSize)      
            ax[index].set_title(self.nodes[index].nodeName)
            ax[index].set_xlabel("Time (years)")
            ax[index].set_ylabel("Population")    

        if showPlot:
            plt.show()

        if outName is not None:
            plt.savefig( outName )

        
    def plotAllNodeGroups(self):
        '''plot all groups in all nodes'''
        ## Calculate the populaiton at each node
        # [ node.calculateNodePopulaiton() for node in self.nodes]
        ncols, nrows =  [ np.ceil(np.sqrt(self.nNodes())), np.floor(np.sqrt(self.nNodes()))]
        print ncols
        fig, axs = plt.subplots(nrows = self.nNodes(), sharex=True, sharey=True)
        # axs = [node.plotNodeGroups(self.nYears) for node in self.NEED]
        ## nodes TO CLEAN UP THIS FUNCTION, After I better understand it 
        print "done with plotallNodeGroups"
        

def initalizeModelFromCSVs( dfNetwork, dfNode, dfGroups):
    ''' 
    This function reads in 3 CSVs and creates a network model using their parameter values.
    '''

   
    ## Create Network
    omegaIn = np.linspace( start = dfNetwork['minLength'],
                           stop = dfNetwork['maxLength'],
                           num = dfNetwork['nPoints'] +2)[1:-1]

    try:
        timePeriods = dfNetwork[ 'timePeriods'][0].split(",")
    except:
        timePeriods = ["All"]

    networkOut = networkModel(dfNetwork['networkName'][0],
                              nYears = dfNetwork['nYears'][0],
                              timePeriods = timePeriods,
                              omega = omegaIn)

    ## Extract out nodes from the network we are using
    ## (this allows a yet to be implement function for generating multiple networks from one set of files)
    nodes = []
    dfNodeUse = dfNode.query(str('network == ' + "'" + networkOut.networkName + "'"))

    ## Loop through each node in the network and generate it
    for nodeRow in dfNodeUse.iterrows():
        nodeName = nodeRow[1]['nodeName']

        try:
            timePeriod = nodeRow[1]['timePeriod']
        except:
            timePeriod = "All"

        nodeTemp =  node( nodeName = nodeName,
                          timePeriod = timePeriod)
        pathsOutTemp = pathOutListFunction( pathsOut = nodeRow[1]['pathsOut'],
                                            pathsOutProb = float(nodeRow[1]['pathsOutProb']))
        nodeTemp.addPathsOut(pathsOutTemp)
        nodeTemp.addPathsIn( nodeRow[1]['pathsIn'].split(","))
        dfGroupsUse = dfGroups.query(str('network == ' + "'" +
                                         networkOut.networkName + "'" + 
                                         ' & node == ' + "'" + 
                                         nodeRow[1]['nodeName'] + "'" ))
        groupsForNodeTemp = []
        ## Loop through each group in a node and generate it
        for groupRow in dfGroupsUse.iterrows():        
            lengthWeightUseTemp = lengthWeight(groupRow[1]['alphaLW'], groupRow[1]['betaLW'])
            densityTemp = densityNegExp(a = groupRow[1]['densityA'], b = groupRow[1]['densityB'])
            survivalTemp = logestic( alphaL = groupRow[1]['alphaS'], betaL = groupRow[1]['betaS'],
                                           minL = groupRow[1]['minS'], maxL = groupRow[1]['maxS'])
            popLenDist0Temp = (stats.lognorm.pdf(omegaIn, loc = 0, s = groupRow[1]['initS'], scale = groupRow[1]['initMean']) /
                               stats.lognorm.pdf(omegaIn, loc = 0, s = groupRow[1]['initS'], scale = groupRow[1]['initMean']).sum() )
            growthTemp = growthVB(aG = groupRow[1]['aG'], kG = groupRow[1]['kG'], sigmaG = groupRow[1]['sigmaG'])
            probabilityReproducingTemp = logestic( alphaL =  groupRow[1]['alphaR'], betaL =  groupRow[1]['betaR'],
                                                         minL =  groupRow[1]['minR'], maxL = groupRow[1]['maxR'])
            recruitmentTemp = linearRecruitment(omega = omegaIn,
                                                      lengthWeight = lengthWeightUseTemp,
                                                      probabilityReproducing = probabilityReproducingTemp,
                                                      survival = survivalTemp,
                                                      eggTransition = groupRow[1]['eggTransition'],
                                                      eggPerkg = groupRow[1]['eggPerkg'],
                                                      muJ = np.log(groupRow[1]['muJ']), sigmaJ = np.log(groupRow[1]['sigmaJ']))
            try:
                pulseIntro = groupRow[1][ 'pulseIntro']
            except:
                pulseIntro = "No"

            try:
                groupImpactViability = groupRow[1][ 'groupImpactViability']
            except:
                groupImpactViability = False

            try:
                groupOffspringViability = float(groupRow[1]['groupOffspringViability'])
            except:
                groupOffspringViability = 1.0
                

            if 'groupOffspringPfemale' in groupRow[1]:
                groupOffspringPfemale = float(groupRow[1]['groupOffspringPfemale'])
            else:
                groupOffspringPfemale = 0.5

            if 'groupImpactSexRatio' in groupRow[1]:
                groupImpactSexRatio =  groupRow[1]['groupImpactSexRatio']
                if not isinstance(groupImpactSexRatio, bool):
                    print groupImpactSexRatio
                    sys.exit("groupImpactSexRatio must be True or False")
            else:
               groupImpactSexRatio = False

            groupTemp = group(groupName = groupRow[1][ 'groupName'],
                              groupSex =  groupRow[1][ 'groupSex'],
                              groupOffspringPfemale = groupOffspringPfemale,
                              groupProduceEggs = groupRow[1][ 'groupProduceEggs'], 
                              popSize0 = groupRow[1][ 'popSize0'],
                              groupImpactViability = groupImpactViability,
                              groupOffspringViability = groupOffspringViability,
                              popLenDist0 = popLenDist0Temp, 
                              omega = omegaIn,
                              nYears = dfNetwork['nYears'][0], 
                              survival = survivalTemp, 
                              growth = growthTemp,
                              recruitment = recruitmentTemp,
                              density = densityTemp,
                              lengthWeight = lengthWeightUseTemp,
                              pulseIntroductionString = pulseIntro,
                              groupImpactSexRatio = groupImpactSexRatio)
            groupsForNodeTemp.append(groupTemp)
        ## Add groups to each node and then add nodes to temp node list
        nodeTemp.addGroupList(groupsForNodeTemp)
        nodes.append( nodeTemp)
    ## Add nodes to the network and then create the paths 
    networkOut.addNodeList(nodes)
    networkOut.initializePaths()
    
    return networkOut
