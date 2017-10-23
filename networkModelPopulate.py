import networkModel as nm
import numpy as np
import scipy.stats as stats

class populatedHelpers:
    ''' Helper funcitons that are coded in one place to avoid repeating'''
    
    def addGroups(self, groups):
        self.groups = groups

    def showGroups(self):
        return self.groups

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
        self.pathsOut = []

class group:
    def __init__(self, groupName):
        self.groupName = groupName
        
    def showGroupName(self):
        return self.groupName

    def createPopDist(self, nYears, nPoints, popDist0 = None):
        if popDist0 is None:
            self.popDist0 = np.zeros(nPoints)
        else:
            self.popDist0 = popDist0
            
        self.popDist = np.zeros( (nYears, nPoints))
        self.popDist[ 0, :] = self.popDist0

    def showPopDist(self):
        return self.popDist

    def showPopDistYear(self, year):
        return self.popDist[ year, :]
    
    def updatePopDistYear(self, year, popAdd):
        self.popDist[ year, :] += popAdd

