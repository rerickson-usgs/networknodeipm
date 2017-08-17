import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

class densityNegExp:
    '''Define a function where density has a negative exponential impact on the system'''
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self, biomass):
        out = self.a * np.exp( -1 *  self.b  * biomass)
        return out 

def densityNone(biomass):
    '''Define a function where density has no impact on the system'''
    return 1 
    
class lengthWeight:
    '''Define a relationship between length and weight'''
    def __init__(self, alphaLW, betaLW):
        self.alphaLW = alphaLW
        self.betaLW  = betaLW
    def __call__(self, omega):
        out = 10 ** (self.alphaLW +
                     np.log10(omega) * self.betaLW)
        return out

class logestic:
    '''Defines a logistic function''' 
    def __init__(self, alphaL, betaL, minL, maxL):
        self.alphaL = alphaL
        self.betaL = betaL
        self.minL = minL
        self.maxL = maxL       

    def __call__(self, z):
        out = self.minL + \
              (self.maxL - self.minL) / \
              ( 1 + np.exp( self.betaL * ( np.log(z) - np.log(self.alphaL))))  
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
            out[ : , index ] = stats.norm.pdf(x = zPrime, \
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
            out[ : , index ] = self.eggTransition * self.eggPerkg * self.survival(omega) * self.probabilityReproducing(omega) * \
                               self.lengthWeight(omega) * self.juvenile
        return(out)
   
class group:
    ''' The group class is the group of inviduals of a give "sex", e.g., males, females, YY-males, sterile males, ect.'''

    ## I think I will want to include omega, nYears, nSizeBins, and sizeBins from the network
    ## Also, I might want to include checks to make sure the popSize0 and popLenDist0 are in the correct format
    def __init__(self, groupName, popSize0, popLenDist0, omega,
                 nYears, survival, growth, recruitment, density, lengthWeight,
                 emigration = None, immigration = None,
                 pulseIntroduction = None,
                 adultSurvivalMultiplier = None,
                 groupSex = None):

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
        self.omega = omega
        self.hWidth = self.omega[1] - self.omega[0]      

        if pulseIntroduction is None:
            self.pulseIntroduction = np.zeros( (nYears + 1, len(omega)))
        else:
            self.pulseIntroduction = pulseIntroduction

        if adultSurvivalMultiplier is None:
            self.adultSurvivalMultiplier = np.ones( nYears + 1)
        else:
            self.adultSurvivalMultiplier = adultSurvivalMultiplier

        if immigration is None:
            self.immigration = np.zeros( (nYears + 1, len(omega)))
        else:
            self.immigration = immigration


        if emigration is None:
            self.emigration = np.zeros( (nYears + 1, len(omega)))
        else:
            self.emigration = emigration
            

            
    def timeStepGroup(self, t,
                      pGroupBirth = 1.0,
                      recruitGroup = None,
                      popLenDistbiomass = None):
        ''' The annual time step dynamically changes the group's size through time.'''
        ## Kevin, is this the best way to do this?
        self.pGroupBirth = pGroupBirth
        
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
                                               self.survival( self.omega) * self.popLenDist[t, :]) * self.adultSurvivalMultiplier[t] +
                                       np.dot( self.hWidth * self.recruitment( self.omega, self.omega), ## The second dod product is reruitment
                                               self.recruitGroup[t, :]) * decrease * self.pGroupBirth  + 
                                       self.pulseIntroduction[t, :] + 
                                       self.immigration[t, :] +
                                       self.emigration[t, :] ) ## These two lines are for natural (i.e., not directly human) movements
        self.popSize[t + 1] =  self.popLenDist[ t + 1, :].sum()

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

    def addGroups(nodes):
        self.groups.append(nodes)

