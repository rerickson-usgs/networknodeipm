import unittest
import numpy as np
import scipy.stats as stats
import pandas as pd 
import sys
sys.path.append("../modelFiles")
import SEACarP as sea

## Next steps:
## Add in group parameter values
## [x] create generic group variables
## Look at nmp.addGroupsFromCSV for next steps 
## [ ] add in starting population details
## [ ] add in LW details, no need to adjust for monthly 
## [ ] add in VB details and survival, adjust for monthly
## [ ] add in maturation details, no need to adjust for montly 
## Add in update nodes (if needed)
## Add in harvest option, will need to create table for this step 


def selectParameterDF(dfLWIn = dfLW,
                      colName = 'Pool',
                      sppCol = 'SpeciesFull',
                      nodeName = nd,
                      hyperName = 'Hyper-parameter'):
    ''' 
    This function extrats parameter coefficients for a specific node and
    a specific species.

    If a pool is not present, the hyper parameter is used.
    '''
    if nodeName in dfLW['Pool'].unique():
        nodeName = nodeName
    else:
        nodeName = hyperName
    return dfLW[ (dfLW['Pool'] == nodeName) & (dfLW['SpeciesFull'] == spp) ]

class test_buildNetwork( unittest.TestCase):

    def test_network_construction(self):
        '''
        This funciton tests the construction of the network and
        the paths within the network. 
        '''
        network = sea.createSEACarPNetwork()
        self.assertEqual(network.showNetworkName(), "SEACarpIL")
        self.assertEqual(network.nodes[12].showNodeSeason(), 3.0)
        self.assertEqual(network.nodes[0].showNodeName(), 'Alton')
        self.assertEqual(network.nodes[0].showPathsIn(), ['LaGrange', 'Peoria'] )
        self.assertEqual(network.nodes[0].showPathsOut(),  ['LaGrange', 'Alton'] )
        self.assertEqual(network.nodes[0].pathsOut, {'LaGrange': 0.27, 'Alton':0.73})

## 
        
if __name__ == '__main__':
    unittest.main()
