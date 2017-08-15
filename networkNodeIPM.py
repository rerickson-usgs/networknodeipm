import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

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

class node:
    ## I think I will want to inherit z, nYears, nSizeBins, and sizeBins from the network
    ## Also, I might want to include checks to make sure the popSize0 and popLenDist0 are in the correct format
    def __init__(self, nodeName, popSize0, popLenDist0, z, nYears):
        self.nYears = nYears
        self.nodeName = nodeName
        self.popSize = np.zeros(nYears + 1)
        self.popSize[0] = popSize0
        self.popLenDist = np.zeros( (nYears, len(z)))
        self.popLenDist[0, :] = popLenDist0
        
    def plotPop(self):
        plt.plot(np.arange(0, self.nYears + 1, 1),  self.popSize)
        plt.title("Population size through time for" + self.nodeName)
        plt.xlabel("Time (years)")
        plt.ylabel("Total population at node")
        plt.show()

        
        
## Next steps: 0) Include survival, 1) include growth/with density 2) include 
    
survival = logestic( alphaL = 40, betaL = -5, minL = 0.1, maxL = 0.7)
print survival(0)
            

z = np.arange( 1, 150, 1)
sur = survival(z)
print len(sur)


# plt.plot(z, sur)
# plt.xlabel("Length (cm)")
# plt.ylabel("Survival")
# plt.show()

nYears = 10

testNode = node(nodeName = "node 1", \
                popSize0 = 1000, \
                popLenDist0 = stats.lognorm.pdf(z, loc = 0, s = 0.2, scale = 50), \
                z = z, \
                nYears = nYears)


testNode.plotPop()
