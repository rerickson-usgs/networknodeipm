import networkModelPopulateSex as nmps
import networkModelPopulate as nmp
import networkModel as nm
import numpy as np
import scipy.stats as stats
import sys 
import pandas as pd


class seacarpNetwork( nmp.populatedNetwork):
    def __init__(self, networkName):
        self.networkName = networkName
        self.nodes = []
        self.paths = []

class seacarpNode( nmps.populatedNodeWithSex, nmp.populatedHelpers):
    def __init__(self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsIn = []
        self.pathsOut = {}
        self.nodeSeason = ''
    def showNodeSeason(self):
        return self.nodeSeason
    def setNodeSeason(self, nodeSeason):
        self.nodeSeason = nodeSeason
    
class createSEACarPNetwork( seacarpNetwork):
    def __init__(self, 
                 inputFolder = "./CSV-SEACarP/",
                 networkFile = "SEACarP_IL_Network.csv",
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

        self.nodes = []
        self.paths = []

        # Read in input files 
        networkFilePath = inputFolder + networkFile
        dfNetwork = pd.read_csv(networkFilePath)

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
        
        self.networkName = dfNetwork['networkName'][0]

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

        
        ## Create nodes 

for season in intraAnnualTime:
    for nd in dfTransitions['start'].unique():
        nodeName = nd
        nodeSeason = season
        dfProb =  dfTransitions[dfTransitions['start'] == nd]
        nodeTemp = seacarpNode( nd)
        nodeTemp.addPathsIn( dfTransitions[dfTransitions['stop'] == nd]['start'])       
        pathOutTemp = {}
        stayProb = 1
        for index, row in dfProb.iterrows():
            pathOutTemp[row['stop']] = row['prob']
            stayProb += - row['prob']
        pathOutTemp[nd] = stayProb
        nodeTemp.addPathsOut(pathOutTemp)
        nodeTemp.setNodeSeason(nodeSeason)

## Move these lines back into for looops 
nodeLWIn =  selectParameterDF(dfLWIn = dfLW,
                              colName = 'Pool',
                              sppCol = 'SpeciesFull',
                              nodeName = nd,
                              hyperName = 'Hyper-parameter')

nodeGroupIn = dfGroup[dfGroup['Node'] == nd]
for  index, row in nodeGroupIn.iterrows():
    ## extract parameters 
    groupName = nd + ' ' + row['Group']
    groupSex = row['Group']
    groupRG = row['ProduceEggs']
    groupRP = row['RatioAtBirth']
    ## Create group and add parameters 
    tempGroup =  nmps.groupWithSex(groupName)
    tempGroup.addSex(groupSex)
    tempGroup.addRecruitmentGroup(groupRG)
    tempGroup.addRecruitmentProportion(groupRP)


    
## Last line of node for loops 
        self.addNodes([nodeTemp])


# class groupWithSex( nmp.group):
#     def __init__(self, groupName):
#         self.groupName = groupName
#         self.stocking = False
#         self.recruitmentGroup = False
        
#     def addSex( self, inputSex):
#         self.sex = inputSex
        
#     def showSex( self ):
#         return self.sex 
    
#     def addRecruitmentGroup(self, rg):
#         self.recruitmentGroup = rg

#     def showRecruitmentGroup(self):
#         return self.recruitmentGroup 

#     def addRecruitmentProportion(self, rp):
#         self.recruitmentProportion = rp

#     def showRecruitmentProportion(self):
#         return self.recruitmentProportion

# class createNetwork( nmp.createNetworkFromCSV):

#     def __init__(self, dfNetwork, networkIn = nmp.populatedNetwork):
#         self.network = networkIn( dfNetwork['networkName'][0] )
#         self.network.setYears( dfNetwork['nYears'][0] )
#         self.network.setupNetworkMesh( dfNetwork['nPoints'][0],
#                                        dfNetwork['minLength'][0],
#                                        dfNetwork['maxLength'][0])

#     def addGroupSexFromCSV( self, dfGroups, groupInIn):
#         '''
#         First, we use the old function to add in groups from a CSV.
#         Second, we update the groups to include the sex attributes.
#         '''
        
#         self.addGroupsFromCSV( dfGroups, groupIn = groupInIn )

#         # ## Loop through nodes and add in groups
#         for n in self.network.nodes:
#             ## Loop through each group in a node and in group sex
#             for grp in n.groups:
#                 dfGroupUse = dfGroups.query(
#                     str('network == ' + "'" +
#                         self.network.networkName + "'" + 
#                         ' & node == ' + "'" + 
#                         n.showNodeName() + "'" +
#                         ' & groupName == ' + "'" +
#                         grp.showGroupName() + "'" ))
#                 grp.addSex( dfGroupUse['groupSex'].values[0] )
#                 grp.addRecruitmentGroup( dfGroupUse['recruitmentGroup'].values[0] )
#                 grp.addRecruitmentProportion( dfGroupUse['recruitmentProportion'].values[0] )
                
# class populatedNodeWithSex( nmp.populatedNode):
#     def __init__( self, nodeName):
#         self.nodeName = nodeName
#         self.groups = []
#         self.pathsIn = []
#         self.pathsOut = {}

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



