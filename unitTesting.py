import unittest
import numpy as np
import scipy.stats as stats
import networkNodeIPM as nnIPM

## Functions that I Need to test
# pathOutListFunction             

class test_densityNegExp(unittest.TestCase):

    def test_zeros(self):
        """Constructor"""
        a = 10.0
        b = 11.0
        biomass = 0.0
        zeroFunc = nnIPM.densityNegExp(a = a, b = b)

        self.assertEqual( zeroFunc(biomass = biomass), 10.0)


class test_densityNone(unittest.TestCase):

    def test_zero(self):
        self.assertEqual( nnIPM.densityNone( 0.0), 1.0)

    def test_nonzero(self):
        self.assertEqual( nnIPM.densityNone( 10.0), 1.0)

class test_lengthWeight(unittest.TestCase):

    def test_zero(self):
        self.lengthWeight = nnIPM.lengthWeight(alphaLW = 1.0,
                                               betaLW  = 2.0)
        self.assertEqual( self.lengthWeight(1.0), 10.0)

    def test_nonzero(self):
        self.lengthWeight = nnIPM.lengthWeight(alphaLW = 1.0,
                                               betaLW  = 2.0)
        self.assertEqual( self.lengthWeight(10.0), 1000.0)



class test_logistic(unittest.TestCase):
    
    def test_one(self):
        self.logistic = nnIPM.logistic( 40.0, -5.0, 0.0, 1.0)
        self.assertEqual( self.logistic(2e8), 1.0)

    def test_inflecitonPoint(self):
        self.logistic = nnIPM.logistic( 40.0, -5.0, 0.0, 1.0)
        self.assertEqual( self.logistic( 40.0), 0.5)

class test_growthVB(unittest.TestCase):

    
    def test_growthVB(self):
        self.growthVB = nnIPM.growthVB( 180.0, 0.16, 10.0)
        self.assertEqual( self.growthVB(180, 180), 0.039894228040143268)

class test_linearRecruitment(unittest.TestCase):


    def test_linearRecruitmentShape(self):
        self.omega = np.linspace( start = 1, stop = 200, num = 200 +2)[1:-1]
        self.linearRecruitment = nnIPM.linearRecruitment(
            omega = self.omega,
            survival = nnIPM.logistic( 40, -5, 0.1, 0.9),
            lengthWeight = nnIPM.lengthWeight( -4.33, 2.77),
            probabilityReproducing = nnIPM.logistic( 40.0, -4.0, 0.0, 1.0),
            eggTransition = 1.0,
            eggPerkg = 5.00E+06,
            muJ = 10, 
            sigmaJ = 2
        )
        self.out = self.linearRecruitment(self.omega, self.omega)
        self.assertEqual(self.out.shape, 
                         (len(self.omega), len(self.omega)))
        

        ## May eventually want another test here


class test_group(unittest.TestCase):

    
    def testGroup(self): 
        #============ Create group so that I can test it ========================#
        ## Setup numerical mesh
        self.minLength = 0
        self.maxLength = 240
        self.nPoints = 200
        self.omega = np.linspace( start = self.minLength, stop = self.maxLength, num = self.nPoints +2)[1:-1]
        
        ## Denisty parameter and distribution 
        self.a = 1
        self.b = 3e-7 # 1e-3
        
        self.density = nnIPM.densityNegExp(a = self.a, b = self.b)
        
        ## Node's survival parameters and function
        self.minS = 0.1
        self.maxS = 0.9
        self.alphaS = 40 # inflection point
        self.betaS  =  -5 # slope
        
        self.survival = nnIPM.logistic( alphaL = self.alphaS, betaL = self.betaS,
                                        minL = self.minS, maxL = self.maxS)
        
        ## Initial population length and size 
        self.initMean = 150
        self.popLenDist0 = (stats.lognorm.pdf(self.omega, loc = 0, s = 0.2, scale = self.initMean) /
                            stats.lognorm.pdf(self.omega, loc = 0, s = 0.2, scale = self.initMean).sum() )
        self.popSize0 = 6.0e3
        
        ## Growth parametesr and function
        self.aG = 180
        self.kG = 0.16
        self.sigmaG = 10
        self.growth = nnIPM.growthVB(aG = self.aG, kG = self.kG, sigmaG = self.sigmaG)
        
        ## the probabilty of reproducing and its function
        self.minR = 0
        self.maxR = 1.0
        self.alphaR = 40
        self.betaR  = -4
        self.probabilityReproducing = nnIPM.logistic( alphaL = self.alphaR, betaL = self.betaR,
                                                      minL = self.minR, maxL = self.maxR)
        
        ## Age-1 length dist
        self.muJ = np.log(10)
        self.sigmaJ = np.log(2)
        
        ## relationship between length and weigth and its function
        self.alphaLW = -4.33
        self.betaLW = 2.77
        self.lengthWeightUse = nnIPM.lengthWeight( self.alphaLW, self.betaLW)
        
        ## Recruitment function and required parameter not previously defined
        self.eggPerkg = 5e3 # default is 5e3
        self.eggTransition = 9e-1  # 3e-3
        self.recruitment = nnIPM.linearRecruitment(omega = self.omega,
                                                   lengthWeight = self.lengthWeightUse,
                                                   probabilityReproducing = self.probabilityReproducing,
                                                   survival = self.survival,
                                                   eggTransition = self.eggTransition,
                                                   eggPerkg = self.eggPerkg, muJ = self.muJ,
        sigmaJ = self.sigmaJ)
        
        ## Simulation parameters
        self.nYears = 300
        
        ## Define node 
        self.testGroup = nnIPM.group(groupName = "node 1", 
                                     popSize0 = self.popSize0, 
                                     popLenDist0 = self.popLenDist0, 
                                     omega = self.omega,
                                     nYears = self.nYears, 
                                     survival = self.survival, 
                                     growth = self.growth,
                                     recruitment = self.recruitment,
                                     density = self.density,
                                     lengthWeight = self.lengthWeightUse)
        
        self.assertEqual( self.testGroup.showGroupName(),  "node 1")
        self.assertEqual( self.testGroup.showGroupProduceEggs(),  False)
        self.assertEqual( self.testGroup.showGroupImpactSexRatio(),  False)
        self.assertEqual( self.testGroup.showGroupImpactViability(),  False)

        ## Don't know hwo to check
        ## group.movement
        ## group.timeStepGroup

if __name__ == '__main__':
    unittest.main()