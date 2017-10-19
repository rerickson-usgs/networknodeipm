import numpy as np
import scipy.stats as stats
import networkNodeIPM  as nnIPM

## Setup numerical mesh
minLength = 0
maxLength = 430
nPoints = 200
omega = np.linspace( start = minLength, stop = maxLength, num = nPoints +2)[1:-1]

## Denisty parameter and distribution 
a = 1
b = 3e-7 # 1e-3

density = nnIPM.densityNegExp(a = a, b = b)

## Node's survival parameters and function
minS =  0.1
maxS =   0.9
alphaS = 40 # inflection point
betaS  =  -5 # slope

survival = nnIPM.logistic( alphaL = alphaS, betaL = betaS, minL = minS, maxL = maxS)

## Initial population length and size 
initMean = 150
popLenDist0 = (stats.lognorm.pdf(omega, loc = 0, s = 0.2, scale = initMean) /
               stats.lognorm.pdf(omega, loc = 0, s = 0.2, scale = initMean).sum() )
popSize0 = 6.0e3

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
probabilityReproducing = nnIPM.logistic( alphaL = alphaR, betaL = betaR, minL = minR, maxL = maxR)

## Age-1 length dist
muJ = np.log(10)
sigmaJ = np.log(2)

## relationship between length and weigth and its function
alphaLW = -4.33
betaLW = 2.77
lengthWeightUse = nnIPM.lengthWeight( alphaLW, betaLW)

## Recruitment function and required parameter not previously defined
eggPerkg = 5e3 # default is 5e3
eggTransition = 9e-1  # 3e-3
recruitment = nnIPM.linearRecruitment(omega = omega,
                                      lengthWeight = lengthWeightUse,
                                      probabilityReproducing = probabilityReproducing,
                                      survival = survival,
                                      eggTransition = eggTransition, eggPerkg = eggPerkg, muJ = muJ, sigmaJ = sigmaJ)

## Simulation parameters
nYears = 200

## Define node 
testGroup = nnIPM.group(groupName = "node 1", 
                      popSize0 = popSize0, 
                      popLenDist0 = popLenDist0, 
                      omega = omega,
                      nYears = nYears, 
                      survival = survival, 
                      growth = growth,
                      recruitment = recruitment,
                      density = density,
                      lengthWeight = lengthWeightUse)
## Iterate through time 
for year in range(0, nYears):
    testGroup.timeStepGroup(year)


## Plot results
testGroup.plotPop()
testGroup.plotLengthTime()


print("Done" )



