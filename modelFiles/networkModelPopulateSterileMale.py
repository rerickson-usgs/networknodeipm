import networkModelPopulateSex as nmps
import networkModelPopulate as nmp
import numpy as np
import scipy.stats as stats
import sys 
import matplotlib.pyplot as plt
import pandas as pd


class groupWithSexSterileMale( nmps.groupWithSex):
    def __init__(self, groupName):
        self.groupName = groupName
        self.stocking = False
        self.recruitmentGroup = False
        self.recruitmentViabilityMod = 1.0
        
    def addImpactRecruitmentViability(self, impact):
        self.impactRecruitmentViability = impact

    def showImpactRecruitmentViability(self):
        return self.impactRecruitmentViability
    
    def addRecruitmentViabilityMod(self, rvm):
        self.recruitmentViabilityMod = rvm

    def showRecruitmentViabilityMod(self):
        return self.recruitmentViabilityMod
        
class populatedNodeWithSexSterileMale( nmps.populatedNodeWithSex):
    def __init__( self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsIn = []
        self.pathsOut = {}

    def projectGroups(self, year, omega, hWidth, nodeBiomass, nextYear = None):
        '''  projects population using midpoint rule.
             First dotproduct is growth/maturation.
             Second dotproduct is recruitment.
        '''

        if nextYear is None:
            nextYear = year+1
            
        reproducingPopulation  = 0.0

        maleContribution   = np.array([grp.showRecruitmentViabilityMod() for grp in self.groups if grp.showSex() == 'male'])

        malePop = np.array([grp.showPopYear(year)  for grp in self.groups
                            if grp.showSex() == 'male'])

        
        if malePop.sum() == 0.0:
            malePopSum = 1.0
        else:
            malePopSum = malePop.sum()
        
        maleViability = (maleContribution   * malePop / malePopSum ).sum()
        
        for grp in self.groups:
            ## First, sum up reruitment groups
            if grp.showRecruitmentGroup():
                reproducingPopulation += grp.showPopDistYear( year)
            if grp.showSex() == "male":
                if grp.showRecruitmentViabilityMod() < 1.0:
                    grp.addRecruitmentViabilityMod(
                        maleViability
                    )                    
                    
        for grp in self.groups:
            popAdd = ( np.dot( hWidth * grp.growth( omega, omega), 
                                    grp.showPopDistYear( year) *
                                    grp.survival( omega) ) +
                            np.dot(hWidth * grp.recruitment( omega, omega),
                                   reproducingPopulation *  grp.density(nodeBiomass) *
                                   grp.showRecruitmentViabilityMod() )
                            )

            if grp.showStocking():
                grp.updatePopDistYear( nextYear, popAdd + grp.showStockingPopYear(year))
            else:
                grp.updatePopDistYear( nextYear, popAdd)


class createNetworkFromCSVwithSterileMale( nmps.createNetworkFromCSVwithSex):

    def __init__(self, dfNetwork, networkIn = nmp.populatedNetwork):
        self.network = networkIn( dfNetwork['networkName'][0] )
        self.network.setYears( dfNetwork['nYears'][0] )
        self.network.setupNetworkMesh( dfNetwork['nPoints'][0],
                                       dfNetwork['minLength'][0],
                                       dfNetwork['maxLength'][0])

    def addGroupSterileMaleFromCSV( self, dfGroups, groupInIn):
        '''
        First, we use the old function to add in groups from a CSV.
        Second, we update the groups to include the sex attributes.
        '''
        
        self.addGroupSexFromCSV( dfGroups, groupInIn = groupInIn)

        ## Loop through nodes and add in groups
        for n in self.network.nodes:
            for grp in n.groups:
                dfGroupUse = dfGroups.query(
                    str('network == ' + "'" +
                        self.network.networkName + "'" + 
                        ' & node == ' + "'" + 
                        n.showNodeName() + "'" +
                        ' & groupName == ' + "'" +
                        grp.showGroupName() + "'" ))
                grp.addImpactRecruitmentViability( dfGroupUse['recruitmentViability'] )
