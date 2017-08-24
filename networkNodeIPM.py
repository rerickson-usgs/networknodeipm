import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

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
                 adultSurvivalMultiplier = None,
                 groupSex = None):

        self.groupProduceEggs = groupProduceEggs
        self.groupImpactSexRatio = groupImpactSexRatio
        self.groupImpactViability = groupImpactViability
        self.nYears = nYears
        self.groupSex = groupSex
        self.groupName = groupName
        self.popSize = np.zeros(nYears + 1)
        self.popSize[0] = popSize0
        self.popLenDist = np.zeros( (nYears + 1, len(omega)))
        self.popLenDist[0, :] = popLenDist0 * popSize0
        self.survival = survival
        self.growth = growth
        self.recruitment = recruitment
        self.density = density
        self.lengthWeight = lengthWeight
        self.groupOffspringPfemale =  groupOffspringPfemale 
        self.groupOffspringViability = groupOffspringViability
        self.omega = omega
        self.hWidth = self.omega[1] - self.omega[0]      

        if pulseIntroduction is None:
            self.pulseIntroduction = np.zeros( (nYears + 1, len(omega)))
        else:
            self.pulseIntroduction = pulseIntroduction

        if adultSurvivalMultiplier is None:
            self.adultSurvivalMultiplier = np.ones( (nYears + 1, len(omega)))
        else:
            self.adultSurvivalMultiplier = adultSurvivalMultiplier

            
    def timeStepGroup(self, t,
                      pReferenceGroupBirth = 0.5,
                      offspringViability = 1.0,
                      recruitGroup = None,
                      popLenDistbiomass = None,
                      referenceSex = "female"):
        ''' The annual time step dynamically changes the group's size through time.'''
        ## Kevin, is this the best way to do this?

        self.offspringViability = offspringViability
        ## Hard wire function to calcuate pGroupBirth based upon sex,
        ## remember that pGroupBirth, by defult, referes to females 
        if self.groupSex is referenceSex:
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


        ## Does adult mortality from treatment occur before or after movement? Also, before or after birth?
        self.popLenDist[t + 1, : ] = ( np.dot( self.hWidth * self.growth( self.omega, self.omega),  ## The first dot product is maturation
                                               self.survival( self.omega) * self.popLenDist[t, :]) * self.adultSurvivalMultiplier[t, :] +
                                       np.dot( self.hWidth * self.recruitment( self.omega, self.omega), ## The second dod product is reruitment
                                               self.recruitGroup[t, :]) * decrease * self.pGroupBirth  * self.offspringViability + 
                                       self.pulseIntroduction[t, :]) ## Stocking numbers for group 

        self.popSize[t + 1] =  self.popLenDist[ t + 1, :].sum()


    def movement(self, immigration, emigration):
        ## This function wil require work and thought into the time step 
        if immigration is None:
            self.immigration = np.zeros( (nYears + 1, len(omega)))
        else:
            self.immigration = immigration

        if emigration is None:
            self.emigration = np.zeros( (nYears + 1, len(omega)))
        else:
            self.emigration = emigration          

        self.popLenDist[t + 1, : ] = popLenDist[t + 1, : ] + self.immigration[t, :] - self.emigration[t, :]  
            

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
    def __init__(self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsOut = []
        self.pathsIn = []
        self.nodeBiomass = 0
    
    def listGroups(self):
        return [grp for grp in self.groups]
        
    def describeNodes(self):
        print self.nodeName + "contains the following groups:"
        print "Group name \t Node sex"
        for grp in self.groups:
            print grp.showGroupName() + "\t\t" + grp.showGroupSex()
        
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
        return self.nodePop

    def plotNodePop(self):
        '''Plot the total population size of fish through time'''
        
        plt.plot(np.arange(0, self.nYears + 1, 1),  self.nodeSize)
        plt.title("Population size through time for all groups at " + self.nodeName)
        plt.xlabel("Time (years)")
        plt.ylabel("Population of node (all lengths)")
        plt.show()




    
class networkModel:
    ''' 
    The networkModel class is a collection of nodes and their interactions through time. 
    '''

    ## I think I will want to include omega, nYears, nSizeBins, and sizeBins from the network
    ## Also, I might want to include checks to make sure the popSize0 and popLenDist0 are in the correct format
    def __init__(self, networkName, nYears, omega):
        self.omega = omega
        self.networkName = networkName
        self.nodes = []
        self.timePeriods = [] # need to be in order, enter as a tuple ()
        self.nTimePeriods = []
        self.nYears = nYears
        self.popLenDistbiomass = np.zeros(( nYears, len(omega)))
        self.eggProducingGroupLenDist = np.zeros(( nYears, len(omega)))
        
    def addNodeList(self,  nodeList):
        [ self.nodes.append( node ) for node in nodeList]
        
    def nNodes(self):
        return len(self.nodes)

        
    def runNetworkSimulation(self):
        self.pReferenceGroupBirth = np.zeros(self.nYears)
        self.offspringViabilityReduction = np.ones(self.nYears)

        for node in self.nodes:
            for year in range(0, self.nYears):
                ## add up sum of egg producing groups

                self.eggProducingGroupLenDist[ year, :] = np.sum([ grp.popLenDist[ year, :] for grp in node.groups if grp.showGroupProduceEggs()])

                
                ## Check if any groups have YY-male like treatments on
                if all([grp.showGroupImpactSexRatio() is False for grp in node.groups]) is False:
                    self.pReferenceGroupBirth[year]  = ( np.sum([grp.groupOffspringPfemale * grp.popLenDist[ year, :].sum() for
                                                                 grp in node.groups if grp.showGroupImpactSexRatio()]) /
                                                         np.sum([ grp.popLenDist[ year, :].sum() for grp in node.groups if
                                                                  grp.showGroupImpactSexRatio()]) ) 
                    ## Check if any groups have non-viable offspring 
                if all([grp.showGroupImpactViability() is False for grp in node.groups]) is False:
                    self.offspringViabilityReduction[year]  = ( np.sum([grp.groupOffspringViability * grp.popLenDist[ year, :].sum() for
                                                                        grp in node.groups if grp.showGroupImpactViability()]) /
                                                                np.sum([ grp.popLenDist[ year, :].sum() for grp in node.groups if
                                                                         grp.showGroupImpactViability()]) )
                        
                self.popLenDistbiomass[ year, :] = np.sum([ grp.popLenDist[ year, :] for grp in node.groups], 0)

                [grp.timeStepGroup(year,
                                   pReferenceGroupBirth = self.pReferenceGroupBirth[year],
                                   recruitGroup = self.eggProducingGroupLenDist,
                                   offspringViability = self.offspringViabilityReduction[year],
                                   popLenDistbiomass = self.popLenDistbiomass) for grp in node.groups ]

                ## LONG TERM, have networkNode function population all nodes from parameter table, look into useing Pandas for this.
                ## Possibly as a wrapper function for this funciton 

    ## Next steps:
    ## Get one node system working
    ## Add in annual time step movement
    ## Add in seasonaility
    ## While doing above, add in helper functions such as plot results, etc 


    ## pseudo code for migration
    ## if nodeOut.pathOut == nodefor nodesIn in all Nodes 


    ## ADD in function to calc total population at a node 
