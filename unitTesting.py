import unittest

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

# class test_linearRecruitment(unittest.TestCase):

#     self.omega = np.linspace( start = 1, stop = 200, num = 200 +2)[1:-1]
#     linearRecruitment = nnIPM.linearRecruitment(
#         omega = range(1, 100),
#         survival = nnIPM.logistic(40, -5, 0.1, 0.9),
#         lengthWeight = nnIPM.lengthWeight( -4.33, 2.77),
#         probabilityReproducing = 1.0,
#         eggTransition = 1.0,
#         eggPerkg = 5.00E+06,
#         muJ = 10, 
#         sigmaJ = 2
#     )


if __name__ == '__main__':
    unittest.main()
