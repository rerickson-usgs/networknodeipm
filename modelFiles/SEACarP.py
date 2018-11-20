import networkModelPopulateSex as nmps
import networkModelPopulate as nmp
import nodeHarvest as nh
import networkModel as nm
import numpy as np
import scipy.stats as stats
import sys 
import pandas as pd


def standarizedLogNormal(omega,  sIn, scaleIn):                     
    return ( stats.lognorm.pdf( omega, loc = 0, s = sIn, scale = scaleIn) /
             stats.lognorm.pdf( omega, loc = 0, s = sIn, scale = scaleIn).sum() )


class seacarpNetwork( nmp.populatedNetwork):
    def __init__(self, networkName):
        self.networkName = networkName
        self.nodes = []
        self.paths = []

class seacarpNode( nmps.populatedNodeWithSex, nmp.populatedHelpers, nh.nodeHarvest):
    def __init__(self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsIn = []
        self.pathsOut = {}
        self.nodeSeason = ''
        self.harvest = 0.0

    def showNodeSeason(self):
        return self.nodeSeason

    def setNodeSeason(self, nodeSeason):
        self.nodeSeason = nodeSeason

    def projectGroups(self, year, omega, hWidth, nodeBiomass, nextYear = None):
        '''  projects population using midpoint rule.
             First dotproduct is growth/maturation.
             Second dotproduct is recruitment.
        '''

        if nextYear is None:
            nextYear = year + 1
            
        reproducingPopulation  = 0.0
        for grp in self.groups:
            if grp.showRecruitmentGroup():
                reproducingPopulation += grp.showPopDistYear( year)
        for grp in self.groups:
            popAdd = ( np.dot( hWidth * grp.growth( omega, omega), 
                               grp.showPopDistYear( year) *
                               grp.survival( omega)  )  +
                            np.dot(hWidth * grp.recruitment( omega, omega),
                                   reproducingPopulation *  grp.density(nodeBiomass) *
                                   grp.showRecruitmentProportion() *
                                   self.probSuccessSpawn.rvs(1))
                            ) 
            popAdd = popAdd * (1.0 - self.showNodeHarvestYear(year))
            if grp.showStocking():
                grp.updatePopDistYear( year + 1, popAdd + grp.showStockingPopYear(year))
            else:
                grp.updatePopDistYear( year + 1, popAdd)


        
#     def projectGroups(self, year, omega, hWidth, nodeBiomass, nextYear = None):
#         '''  projects population using midpoint rule.
#              First dotproduct is growth/maturation.
#              Second dotproduct is recruitment.
#         '''

#         if nextYear is None:
#             nextYear = year + 1
            
#         reproducingPopulation  = 0.0
#         for grp in self.groups:
#             if grp.showRecruitmentGroup():
#                 reproducingPopulation += grp.showPopDistYear( year)
#         for grp in self.groups:
#             popAdd = ( np.dot( hWidth * grp.growth( omega, omega), 
#                                grp.showPopDistYear( year) *
#                                grp.survival( omega)  )  +
#                             np.dot(hWidth * grp.recruitment( omega, omega),
#                                    reproducingPopulation *  grp.density(nodeBiomass) *
#                                    grp.showRecruitmentProportion() )
#                             ) 

#             if grp.showStocking():
#                 grp.updatePopDistYear( year + 1, popAdd + grp.showStockingPopYear(year))
#             else:
#                 grp.updatePopDistYear( year + 1, popAdd)


def selectParameterDF(nodeName,
                      dfLWIn,
                      spp, 
                      colName = 'Pool',
                      sppCol = 'SpeciesFull',
                      hyperName = 'Hyper-parameter'):
    ''' 
    This function extrats parameter coefficients for a specific node and
    a specific species.
        
    If a pool is not present, the hyper parameter is used.
    '''
    dfLWInSpp = dfLWIn[dfLWIn[sppCol] == spp]
        
    if nodeName in dfLWInSpp[colName].unique():
        nodeNameUse = nodeName
    else:
        nodeNameUse = hyperName
        
    return dfLWIn[ (dfLWIn[colName] == nodeNameUse) & (dfLWIn[sppCol] == spp) ]

def convertAndAdjustMort(M, timeAdjust = 1.0):
    '''
    Converts estimated annual mortality to survival for a smaller unit of time 
    (e.g., monthly if timeAdjust = 12.0).
        
    The function also ensures mortality is less than or equal to 1. 
    '''
        
    if M >= 1.0:
        Muse = 1.0
    else:
        Muse = M

    return 1.0 - Muse/timeAdjust

        
        
class createSEACarPNetwork:
    def __init__(self, 
                 inputFolder = "./CSV-SEACarP/",
                 networkFile = "SEACarP_IL_Network.csv",
                 nodeFile = "SEACarP_IL_Nodes.csv",
                 transitionFile = "SEACarP_IL_Transitions.csv",
                 vonBcoefFile = "coefAll_vonB.csv",
                 lwCoefFile = "lengthWeightCoefAll.csv",
                 matCoefFile = "maturityCoefAll.csv",
                 groupDetails = "groupDetails.csv",
                 spp = "Bighead carp",
                 intraAnnualTime = np.linspace(1,12,12)
    ):
        '''
        Build a network model intra-annual time periods.
        This assumes transitions are on monthly time step,
        but inputs are on an annual timestep.
        '''
        # Read in input files 
        networkFilePath = inputFolder + networkFile
        dfNetwork = pd.read_csv(networkFilePath)

        nodeFilePath = inputFolder + nodeFile
        dfNode = pd.read_csv(nodeFilePath)
        
        transitionFilePath = inputFolder + transitionFile
        dfTransitions = pd.read_csv(transitionFilePath)
        
        vonBcoefFilePath = inputFolder + vonBcoefFile
        dfVonB = pd.read_csv(vonBcoefFilePath)
        
        lwCoefFilePath = inputFolder + lwCoefFile
        dfLW = pd.read_csv(lwCoefFilePath)
        
        matCoefFilePath = inputFolder + matCoefFile
        dfMat = pd.read_csv(matCoefFilePath)
        
        groupDetailsFilePath = inputFolder + groupDetails
        dfGroup = pd.read_csv(groupDetailsFilePath)
        
        self.network = seacarpNetwork(dfNetwork['networkName'][0])

        self.network.setYears( dfNetwork['nYears'][0] )
        self.network.setupNetworkMesh( dfNetwork['nPoints'][0], dfNetwork['minLength'][0], dfNetwork['maxLength'][0])
        
        ## Create nodes
        for season in intraAnnualTime:
            ## Create node transition probabilites
            for nd in dfTransitions['start'].unique():
                nodeName = nd
                nodeSeason = season
                dfProb =  dfTransitions[dfTransitions['start'] == nd]
                nodeTemp = seacarpNode( nd)
                nodeTemp.addPathsIn( dfTransitions[dfTransitions['stop'] == nd]['start'])       
                pathOutTemp = {}
                stayProb = 1

                ## Add in node probability of spawning for beta distribution 
                if nd in dfNode['Pool'].unique():
                    dfNodeUse = dfNode[dfNode['Pool'] == nd]
                    nodeTemp.probSuccessSpawn = stats.beta( dfNodeUse['SpawnProbA'].values[0], dfNodeUse['SpawnProbB'].values[0])
                else:
                    print(nd + ' is not in the node input file ' + nodeFilePath)
                    break

                ## Enter in harvest for season
                harvestLevels = np.zeros(self.network.nYears + 1)
                if season in [float(x) for x in dfNodeUse['HarvestMonths'].values[0].split(";")]:
                    harvestLevels[ (int(dfNodeUse['HarvestStart']) - 1):int(dfNodeUse['HarvestEnd']) ] = dfNodeUse[ "HarvestLevel"]
                nodeTemp.setHarvest(harvestLevels)
                

                
                ## enter in transition probability 
                for index, row in dfProb.iterrows():
                    pathOutTemp[row['stop']] = row['prob']
                    stayProb += - row['prob']
                    pathOutTemp[nd] = stayProb
                    nodeTemp.addPathsOut(pathOutTemp)
                    nodeTemp.setNodeSeason(nodeSeason)
                    nodeGroupIn = dfGroup[dfGroup['Node'] == nd]
                    
                ## Enter in Groups     
                for  index, row in nodeGroupIn.iterrows():                                            
                    ## Create group and add parametes
                    tempGroup =  nmps.groupWithSex( nd + ' ' + row['Group'])
                    tempGroup.addSex( row['Group'] ) 
                    tempGroup.addRecruitmentGroup( row['ProduceEggs'] )
                    tempGroup.addRecruitmentProportion( row['RatioAtBirth'] )

                    tempGroup.setEggTransition( row['eggTransition'] )
                    tempGroup.setEggPerkg( row['eggPerkg'] )
                    tempGroup.setSigmaJ( row['sigmaJ'] )
                    tempGroup.setMuJ( row['muJ'] )


                    
                    popSize0temp = standarizedLogNormal(self.network.omega,
                                                        sIn = row['initialMu'], 
                                                        scaleIn = row['initialSD'])  * row['StartPop']         
                    tempGroup.createPopDist( nYears = self.network.nYears,
                                             nPoints = self.network.nPoints,
                                             popDist0 = popSize0temp)
                    dfLWuse = selectParameterDF(nodeName,
                                                dfLWIn = dfLW,
                                                spp = spp,
                                                colName = 'Pool',
                                                sppCol = 'SpeciesFull',
                                                hyperName = 'Hyper-parameter')
                    tempGroup.setLengthWeight(nmp.lengthWeight(alphaLW = dfLWuse[dfLWuse['parameter'] == 'Intercept']['mean'],
                                                               betaLW  = dfLWuse[dfLWuse['parameter'] == 'Slope']['mean']))
                    dfVonBuse = selectParameterDF(nodeName,
                                                  spp = spp,
                                                  dfLWIn = dfVonB,
                                                  colName = 'Pool',
                                                  sppCol = 'Species',
                                                  hyperName = 'Hyper-parameter')
                    tempGroup.setGrowth(nmp.growthVB(aG = dfVonBuse[dfVonBuse['Parameter'] == 'Linfinty']['mean'],
                                                     kG = dfVonBuse[dfVonBuse['Parameter'] == 'K']['mean']/len(intraAnnualTime),
                                                     sigmaG = dfVonBuse[dfVonBuse['Parameter'] == 'K']['sd']))
                    mTemp = convertAndAdjustMort( dfVonBuse[(dfVonBuse['Parameter'] == 'M')]['mean'].values,
                                                  len(intraAnnualTime))
                    
                    tempGroup.setSurvival( mTemp)
                    dfMatuse = dfMat[dfMat['Species'] == spp]
                    tempGroup.setProbabilityOfReproducing(
                        nmp.logistic( alphaL = dfMatuse[(dfMatuse['parameter'] == 'alpha')]['mean'],
                                      betaL  = dfMatuse[(dfMatuse['parameter'] == 'beta')]['mean'],
                                      minL = 0,
                                      maxL = 1))
                    nodeTemp.addGroups( [tempGroup] )
                ## Last line of node for loops 
                self.network.addNodes([nodeTemp])

    def outputNetwork(self):
        return self.network








