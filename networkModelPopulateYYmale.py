import networkModelPopulateSex as nmps
import networkModelPopulate as nmp
import numpy as np
import scipy.stats as stats
import sys 
import matplotlib.pyplot as plt
import pandas as pd


class groupWithSexYY( nmps.groupWithSex):
    def __init__(self, groupName):
        self.groupName = groupName
        self.stocking = False
        self.recruitmentGroup = False
        self.recruitmentProportionMod = 0.0
        
    def addImpactOnFemaleRatio(self, impact):
        self.impactOnFemaleRatio = impact
        self.impactOnMaleRatio = 1.0 - impact

    def showImpactOnFemaleRatio(self):
        return self.impactOnFemaleRatio
    
    def showImpactOnMaleRatio(self):
        return self.impactOnMaleRatio

    def addRecruitmentProportionMod(self, rpm):
        self.recruitmentProportionMod = rpm

    def showRecruitmentProportionMod(self):
        return self.recruitmentProportionMod

        
class populatedNodeWithSexYY( nmps.populatedNodeWithSex):
    def __init__( self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsIn = []
        self.pathsOut = {}

    def projectGroups(self, year, omega, hWidth, nodeBiomass):
        '''  projects population using midpoint rule.
             First dotproduct is growth/maturation.
             Second dotproduct is recruitment.
        '''
        reproducingPopulation  = 0.0


        ## NEED TO FIX THIS AREA

        ## Specifically, create a modified recruitment proportion
        ## That is the the recruitmentProportion * group Pop / total pop
        groupsMale   = [grp.showSex() == "male"  for grp in self.groups]
        groupsFemale = [grp.showSex() == "female"  for grp in self.groups]
        groupsPop    = np.array([grp.showPopYear(year)  for grp in self.groups])

        maleContribution   = np.array([grp.showImpactOnMaleRatio()    for grp in self.groups])[ groupsMale]
        femaleContribution = np.array([grp.showImpactOnFemaleRatio()  for grp in self.groups])[ groupsFemale]
        
        malePop   = groupsPop[groupsMale]
        femalePop = groupsPop[groupsFemale]

        maleRatio   = (maleContribution   * malePop / malePop.sum()).sum()
        femaleRatio = (femaleContribution * femalePop / femalePop.sum()).sum()
        
        for grp in self.groups:
            ## First, sum up reruitment groups
            if grp.showRecruitmentGroup():
                reproducingPopulation += grp.showPopDistYear( year)
            if grp.showSex() == "male":
                if grp.showRecruitmentProportion() > 0.0:
                    grp.addRecruitmentProportionMod(
                        maleRatio
                    )                    
                    
            if grp.showSex() == "female":
                if grp.showRecruitmentProportion() > 0.0:
                    grp.addRecruitmentProportionMod(
                        femaleRatio
                    )

        for grp in self.groups:
            popAdd = ( np.dot( hWidth * grp.growth( omega, omega), 
                                    grp.showPopDistYear( year) *
                                    grp.survival( omega) ) +
                            np.dot(hWidth * grp.recruitment( omega, omega),
                                   reproducingPopulation *  grp.density(nodeBiomass) *
                                   grp.showRecruitmentProportionMod() )
                            )

            if grp.showStocking():
                grp.updatePopDistYear( year + 1, popAdd + grp.showStockingPopYear(year))
            else:
                grp.updatePopDistYear( year + 1, popAdd)


class createNetworkFromCSVwithYY( nmps.createNetworkFromCSVwithSex):

    def __init__(self, dfNetwork):
        self.network = nmp.populatedNetwork( dfNetwork['networkName'][0] )
        self.network.setYears( dfNetwork['nYears'][0] )
        self.network.setupNetworkMesh( dfNetwork['nPoints'][0],
                                       dfNetwork['minLength'][0],
                                       dfNetwork['maxLength'][0])

    def addGroupYYFromCSV( self, dfGroups, groupInIn):
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
                grp.addImpactOnFemaleRatio( dfGroupUse['impactOnFemales'].values[0])
