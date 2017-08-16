import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

class densityNegExp:  
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self, biomass):
        out = self.a * np.exp( -1 *  self.b  * biomass)
        return out 

def densityNone(biomass):
    return 1 
    
class lengthWeight:
    def __init__(self, alphaLW, betaLW):
        self.alphaLW = alphaLW
        self.betaLW  = betaLW
    def __call__(self, omega):
        out = 10 ** (self.alphaLW +
                     np.log10(omega) * self.betaLW)
        return out

class logestic:
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
   
class node:
    ## I think I will want to include omega, nYears, nSizeBins, and sizeBins from the network
    ## Also, I might want to include checks to make sure the popSize0 and popLenDist0 are in the correct format
    def __init__(self, nodeName, popSize0, popLenDist0, omega,
                 nYears, survival, growth, recruitment, density, lengthWeight,  emigration, immigration):
        self.nYears = nYears
        self.nodeName = nodeName
        self.popSize = np.zeros(nYears + 1)
        self.popSize[0] = popSize0
        self.popLenDist = np.zeros( (nYears + 1, len(omega)))
        self.popLenDist[0, :] = popLenDist0 * popSize0
        self.survival = survival
        self.growth = growth
        self.recruitment = recruitment
        self.density = density
        self.lengthWeight = lengthWeight 
        self.immigration = immigration
        self.emigration = emigration
        self.omega = omega
        self.hWidth = self.omega[1] - self.omega[0]      


        
    def annualTimeStep(self, t):
        ## Kevin, is this the best way to do this?
        biomass = np.sum(self.popLenDist[ t, :] * self.lengthWeight(self.omega))
        decrease = self.density(biomass)
        
        self.popLenDist[t + 1, : ] = ( np.dot( self.hWidth * self.growth( self.omega, self.omega),
                                               self.survival( self.omega) * self.popLenDist[t, :]) +
                                       np.dot( self.hWidth * self.recruitment( self.omega, self.omega),
                                               self.popLenDist[t, :]) * decrease +    
                                       self.immigration - self.emigration)
        self.popSize[t + 1] =  self.popLenDist[ t + 1, :].sum()

    def plotLengthTime(self):
        fig, ax = plt.subplots()
        for index in range(0, self.popLenDist.shape[0]):
            ax.plot(self.omega, self.popLenDist[ index, :])      
        plt.title("Length distributions " + self.nodeName)
        plt.xlabel("Length")
        plt.ylabel("Population in size class")
        plt.show()

    def plotPop(self):
        plt.plot(np.arange(0, self.nYears + 1, 1),  self.popSize)
        plt.title("Population size through time for " + self.nodeName)
        plt.xlabel("Time (years)")
        plt.ylabel("Total population at node")
        plt.show()


