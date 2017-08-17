import numpy as np
import scipy.stats as stats
import networkNodeIPM  as nnIPM

## Setup numerical mesh
minLength = 0
maxLength = 300,
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

## Age-1 length dist
muJ = np.log(10)
sigmaJ = np.log(2)

## relationship between length and weigth and its function
alphaLW = -4.33
betaLW = 2.77
lengthWeightUse = nnIPM.lengthWeight( alphaLW, betaLW)

## Recruitment function and required parameter not previously defined
eggPerkg = 5e6 # old default is 5e3
eggTransition = 3e-3  # 3e-3
recruitment = nnIPM.linearRecruitment(omega = omega,
                                      lengthWeight = lengthWeightUse,
                                      probabilityReproducing = probabilityReproducing,
                                      survival = survival,
                                      eggTransition = eggTransition, eggPerkg = eggPerkg, muJ = muJ, sigmaJ = sigmaJ)

## Create a recruitment function that produces no oppsring
recruitment0 = nnIPM.linearRecruitment(omega = omega,
                                      lengthWeight = lengthWeightUse,
                                      probabilityReproducing = probabilityReproducing,
                                      survival = survival,
                                      eggTransition = 0, eggPerkg = 0, muJ = muJ, sigmaJ = sigmaJ)


## Simulation parameters
nYears = 300
immigration = 0
emigration = 0


## Specify stocking of YY-males

## Define groups
node1group1female = nnIPM.group(groupName = "Node 1",
                                groupSex =  "female", 
                                popSize0 = popSize0node1female, 
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

node1group1male =   nnIPM.group(groupName = "Node 1",
                                groupSex =  "male", 
                                popSize0 = popSize0node1male, 
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


## Pulse introdcution details 
pulseIntroduction = np.zeros( (nYears + 1, len(omega)))

releaseYearYYmale =  30
releaseYearStopYYmale = 50
releaseNumberYYmale = 5e3

## Assume same release disrtiubtion as intial population, 
pulseIntroduction[ (releaseYearYYmale - 1):releaseYearStopYYmale, :] = popLenDist0 * releaseNumberYYmale
# pulseIntroduction.sum(1) ## Prints out total stocking numbers per year 

node1group1YYmale =   nnIPM.group(groupName = "Node 1",
                                  groupSex =  "YY-male", 
                                  popSize0 = 0, 
                                  popLenDist0 = popLenDist0, 
                                  omega = omega,
                                  nYears = nYears, 
                                  survival = survival, 
                                  growth = growth,
                                  recruitment = recruitment0,
                                  density = density,
                                  pulseIntroduction = pulseIntroduction,
                                  lengthWeight = lengthWeightUse)

## Functions after here will eventually be wrapped into the node class 
## Iterate through time

## Will need to specify reproducing group as a variable

eggProducingGroupLenDist = node1group1female.popLenDist
popLenDistbiomass = node1group1female.popLenDist + node1group1male.popLenDist + node1group1YYmale.popLenDist

for year in range(0, nYears):
    ## Will want to replace the next lines of code with iterator for loops eventually
    groupPops = np.array([node1group1female.popLenDist[ year, :].sum(),
                          node1group1male.popLenDist[ year, :].sum(),
                          node1group1YYmale.popLenDist[ year, :].sum()])
    pGroupBirth = groupPops/groupPops.sum()
    pGroupBirth[1] = np.sum(pGroupBirth[1:2])
    pGroupBirth[2] = 0
    popLenDistbiomass[ year, :] = (node1group1female.popLenDist[ year, :] +
                                   node1group1male.popLenDist[ year, :] +
                                   node1group1YYmale.popLenDist[ year, :] )
    node1group1female.timeStepGroup(year,
                                    pGroupBirth = pGroupBirth[0],
                                    recruitGroup = eggProducingGroupLenDist,
                                    popLenDistbiomass = popLenDistbiomass)
    node1group1male.timeStepGroup(year,
                                  pGroupBirth = pGroupBirth[1],
                                  recruitGroup = eggProducingGroupLenDist,
                                  popLenDistbiomass = popLenDistbiomass)
    node1group1YYmale.timeStepGroup(year,
                                    pGroupBirth = pGroupBirth[2],
                                    recruitGroup = eggProducingGroupLenDist,
                                    popLenDistbiomass = popLenDistbiomass)
    
## Plot results
node1group1female.plotPop()
node1group1female.plotLengthTime()

node1group1male.plotPop()
node1group1male.plotLengthTime()

node1group1YYmale.plotPop()
node1group1YYmale.plotLengthTime()


print "Done" 

