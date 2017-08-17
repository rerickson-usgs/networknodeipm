import numpy as np
import scipy.stats as stats
import networkNodeIPM  as nnIPM

## Setup numerical mesh
minLength = 0
maxLength = 240,
nPoints = 200
omega = np.linspace( start = minLength, stop = maxLength, num = nPoints +2)[1:-1]


## Denisty parameter and distribution 
a = 1
b = 3e-7 # 1e-3

density = nnIPM.densityNegExp(a = a, b = b)
# density = densityNone

minS = 0.1
maxS = 0.9
alphaS = 40 # inflection point
betaS  =  -5 # slope

survival = nnIPM.logestic( alphaL = alphaS, betaL = betaS, minL = minS, maxL = maxS)


initMean = 150
popLenDist0 = stats.lognorm.pdf(omega, loc = 0, s = 0.2, scale = initMean) / stats.lognorm.pdf(omega, loc = 0, s = 0.2, scale = initMean).sum()


aG = 180
kG = 0.16
sigmaG = 10
growth = nnIPM.growthVB(aG = aG, kG = kG, sigmaG = sigmaG)

## the probabilty of reproducing
minR = 0
maxR = 1.0
alphaR = 40
betaR  = -4

## Age 1 length dist
muJ = np.log(10)
sigmaJ = np.log(2)

## relationship between length and weigth
alphaLW = -4.33
betaLW = 2.77

## eggs per kg
eggPerkg = 5e3 # default is 5e3
eggTransition = 9e-1  # 3e-3

probabilityReproducing = nnIPM.logestic( alphaL = alphaR, betaL = betaR, minL = minR, maxL = maxR)
lengthWeightUse = nnIPM.lengthWeight( alphaLW, betaLW)

recruitment = nnIPM.linearRecruitment(omega = omega,
                                      lengthWeight = lengthWeightUse,
                                      probabilityReproducing = probabilityReproducing,
                                      survival = survival,
                                      eggTransition = eggTransition, eggPerkg = eggPerkg, muJ = muJ, sigmaJ = sigmaJ)

nYears = 300

immigration = 0
emigration = 0

popSize0 = 8.5e3

testGroup = nnIPM.group(groupName = "node 1", 
                      popSize0 = popSize0, 
                      popLenDist0 = popLenDist0, 
                      omega = omega,
                      nYears = nYears, 
                      survival = survival, 
                      growth = growth,
                      recruitment = recruitment,
                      density = density,
                      lengthWeight = lengthWeightUse,
                      immigration = immigration, 
                      emigration = emigration)

for year in range(0, nYears):
    testGroup.timeStepGroup(year)


testGroup.plotPop()
testGroup.plotLengthTime()
print testGroup.popLenDist.sum(1)
print "Done" 

